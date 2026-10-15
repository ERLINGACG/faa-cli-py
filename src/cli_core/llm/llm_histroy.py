import os

from langchain_core.messages import HumanMessage, ToolMessage
import json


class FaaLLmHistory:

    history={}
    history_dir=[]

    read_path=""

    def __init__(self,read_path:str="./history"):
        self.read_path=read_path
        self.history_dir=os.listdir(self.read_path)
        pass

    def load(self,session_id:str):
        if session_id not in self.history_dir:
            os.makedirs(os.path.join(self.read_path,session_id))
            self.history_dir.append(session_id)

        self.history={
            "session_id":session_id,
            "messages":[]
        }

        save_path = self.read_path + "/" + session_id + "/history.json"
        try:
            with open(save_path, "r", encoding="utf-8") as f:   # 指定 UTF-8
                self.history = json.load(f)

        except FileNotFoundError as e:
            self.history={
                "session_id":session_id,
                "messages":[]
            }
            pass
        pass

    def add(self, session_id:str):

        pass

    def user(self,message:HumanMessage):

        self.history["messages"].append({
            "role":"user",
            "content":message.content
        })
        pass



    def assistant(self, message: str, tool_call=None):
        msg = {"role": "assistant", "content": message}
        if tool_call is not None:
            # 如果传的是单个字典，自动包装成列表
            if isinstance(tool_call, dict):
                # 如果字典里已经有 "type" 和 "function"，说明是标准格式，直接包装
                if "type" in tool_call and "function" in tool_call:
                    tool_call = [tool_call]
                else:
                    # 否则按你的旧格式重新构造
                    tool_call = [{
                        "id": tool_call.get("id", ""),
                        "type": "function",
                        "function": {
                            "name": tool_call.get("name", ""),
                            "arguments": tool_call.get("args", "{}")
                        }
                    }]
            # 如果传的是列表，确保每个元素都符合标准
            elif isinstance(tool_call, list):
                tool_call = [
                    {
                        "id": tc.get("id", ""),
                        "type": "function",
                        "function": {
                            "name": tc.get("function", {}).get("name", tc.get("name", "")),
                            "arguments": tc.get("function", {}).get("arguments", tc.get("args", "{}"))
                        }
                    }
                    for tc in tool_call
                ]
            msg["tool_calls"] = tool_call
        self.history["messages"].append(msg)

    def tool(self,message:ToolMessage):
        self.history["messages"].append({
            "role": "tool",
            "tool_call_id": message.tool_call_id,
            "content": message.content
        })
        pass

    def message(self):
        return self.history["messages"]



    def clear(self):
        self.history["messages"]=[]
        pass

    def save(self,session_id:str):
        save_path = self.read_path + "/" + session_id + "/history.json"
        with open(save_path, "w", encoding="utf-8") as f:   # 指定 UTF-8
            json.dump(self.history, f, indent=2, ensure_ascii=False)


