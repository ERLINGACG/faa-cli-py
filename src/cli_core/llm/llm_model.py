import json

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_openai import ChatOpenAI

from src.cli_core.llm.llm_histroy import FaaLLmHistory
from src.cli_core.llm.llm_token import FaaLLmToken
from src.iconfig.config import Config


class FaaLLmModel:

    _model = None
    _config: Config = Config()
    _history: FaaLLmHistory = FaaLLmHistory()
    _tools = []
    _bundle = None
    _sys_prompt = ""

    def __init__(self):
        pass

    def config(self, config: Config):
        self._config = config
        return self

    def build(self):
        self._model = ChatOpenAI(
            model=self._config.model,
            api_key=self._config.api_key,
            base_url=self._config.api_url,
            reasoning=None  # 明确禁用
        )
        return self

    def bind_tools(self, tools: list):
        self._tools = tools
        self._bundle = self._model.bind_tools(tools)
        return self

    def chat(self, message: str):
        return self._model.invoke(message)

    def load(self, session_id: str):
        self._history.load(session_id)

    # ------------------------------------------------------------------ #
    #  streamV2 —— 支持多个工具调用                                        #
    # ------------------------------------------------------------------ #
    def streamV2(self, message: HumanMessage, token: FaaLLmToken, callback=None):

        self._history.user(message)

        # FIX: 按 index 分别累积每个工具调用的 id / name / args
        def getCall(stream):
            _ask = ""
            tool_calls_map = {}  # index -> {"id": ..., "name": ..., "args": ...}

            for chunk in stream:
                if callback is not None:
                    token.token = chunk.content
                    callback(token)

                _ask += chunk.content or ""

                if chunk.tool_call_chunks:
                    for tc in chunk.tool_call_chunks:
                        idx = tc.get("index", 0)
                        if idx not in tool_calls_map:
                            tool_calls_map[idx] = {"id": "", "name": "", "args": ""}

                        if tc.get("id"):
                            tool_calls_map[idx]["id"] = tc["id"]
                        if tc.get("name"):
                            # FIX: 用 += 而不是 =，防止分片覆盖
                            tool_calls_map[idx]["name"] += tc["name"]
                        if tc.get("args"):
                            # FIX: 同一个 index 的 args 才累加，不同的分开存
                            tool_calls_map[idx]["args"] += tc["args"]

            return {
                "ask": _ask,
                "tool_calls": list(tool_calls_map.values()),  # [{id,name,args}, ...]
            }

        while True:
            stream = self._bundle.stream(self._history.message())
            call = getCall(stream)

            ask = call["ask"]
            tool_calls_ = call["tool_calls"]

            # FIX: 没有任何工具调用 -> 收尾退出
            #      （不再用 `name=="" or call_str==""` 判断，
            #        否则无参数工具会被误判为没有调用）
            if not tool_calls_:
                self._history.assistant(message=ask, tool_call=[])
                break

            # FIX: 先把 assistant 的 tool_call 全部写进历史，保证消息序列一致
            history_tool_calls = [{
                "id": tc["id"],
                "type": "function",
                "function": {
                    "name": tc["name"],
                    "arguments": tc["args"],
                }
            } for tc in tool_calls_]
            self._history.assistant(message=ask, tool_call=history_tool_calls)

            # FIX: 依次执行每个工具调用
            for tc in tool_calls_:
                name = tc["name"]
                tool_id = tc["id"]
                call_str = tc["args"]

                target_tool = next((t for t in self._tools if t.name == name), None)

                try:
                    args_dict = json.loads(call_str) if call_str else {}
                    if target_tool is None:
                        result = f"[error] unknown tool: {name}"
                    else:
                        result = target_tool.invoke(args_dict)

                except Exception as e:
                    # 不抛出，转成 tool 消息回灌给 LLM 让它重试
                    result = f"[tool error] {type(e).__name__}: {e}"

                self._history.tool(
                    ToolMessage(content=str(result), tool_call_id=tool_id)
                )

    # ------------------------------------------------------------------ #
    #  stream —— 单次问答（保留原逻辑，顺手修了 bug）                       #
    # ------------------------------------------------------------------ #
    def stream(self, message: HumanMessage, token: FaaLLmToken, callback=None):
        # 1. 用户消息
        if message.content != "":
            self._history.user(message)

        # 2. 第一次流式请求
        stream = self._bundle.stream(self._history.message())
        ask = ""
        name = ""
        tool_id = ""
        call_str = ""

        for chunk in stream:
            # 文本内容
            if chunk.content:
                ask += chunk.content
                token.token = chunk.content
                if callback is not None:
                    callback(token)

            # 工具调用片段
            if chunk.tool_call_chunks:
                for tc in chunk.tool_call_chunks:
                    if tc.get("name"):
                        # FIX: 用 += 避免分片覆盖
                        name += tc["name"]
                    if tc.get("id"):
                        tool_id = tc["id"]
                    if tc.get("args"):
                        call_str += tc["args"]

        # 3. 处理工具调用
        if name and call_str:
            try:
                args_dict = json.loads(call_str)
            except json.JSONDecodeError as e:
                self._history.assistant(message=ask)
                err = f"[tool error] invalid JSON args: {e}\nraw={call_str!r}"
                token.token = err
                if callback is not None:
                    callback(token)
                return

            # 查找工具
            target_tool = next((t for t in self._tools if t.name == name), None)

            if target_tool:
                result = target_tool.invoke(args_dict)

                tool_calls = [{
                    "id": tool_id,
                    "type": "function",
                    "function": {
                        "name": name,
                        "arguments": call_str,
                    }
                }]
                self._history.assistant(message=ask, tool_call=tool_calls)

                # 添加 tool 消息
                self._history.tool(
                    ToolMessage(content=str(result), tool_call_id=tool_id)
                )

                final_response = self._bundle.invoke(self._history.message())
                final_content = final_response.content
                self._history.assistant(message=final_content)

                # 输出最终回答
                token.token = final_content
                if callback is not None:
                    callback(token)

            else:
                # 工具未找到
                self._history.assistant(message=ask)
                error_msg = f"工具 {name} 未找到"
                # FIX: 原来是 callback(error_msg)，callback 期望的是 token 对象
                token.token = error_msg
                if callback is not None:
                    callback(token)

        else:
            # 没有工具调用，直接保存回答
            self._history.assistant(message=ask)
            # ask 已经在流式循环中输出过，这里不再重复

    def dump(self):
        print(json.dumps(self._history.history, indent=2, ensure_ascii=False))

    def save(self, session_id: str):
        self._history.save(session_id)

    def clear(self):
        self._history.clear()