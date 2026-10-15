import json
import socket

from langchain_core.tools import tool

from src.send.send_servcie import SendService

service=SendService()
service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
DPI= 1.25


# @tool(description="发送请求 参数为json字符串")
def send_request(request:str) -> str:
    """发送请求 参数为json字符串"""
    res_str=service.requestV3(
        json.loads(request)
    )

    return json.dumps(res_str.unserialize().get("body"))



# @tool(description="获取所有微服务信息")
def query_ms_info() -> str:
    """查询微服务信息"""
    data2={
        "route_operation":"query"
    }
    res_str=service.requestV2(
        data2
    )
    json_str = res_str.decode('utf-8')
    return json_str


# @tool(description="启动 wgc 屏幕捕获")
def start_wgc_capture(name: str) -> str:
    """启动 wgc 屏幕捕获 参数为微服务的name"""
    data2={
        "route_operation":"route",
        "id_str":name,
        "detail": {
            "operation":"wgc",
        }
    }
    res_str=service.requestV2(
        data2
    )
    json_str = res_str.decode('utf-8')
    return json_str
    pass


# @tool(description="异步提交OCR任务")
def submit_ocr_task(name: str) -> str:
    """异步提交OCR任务 参数为微服务的name"""
    data2={
        "route_operation":"route",
        "id_str":name,
        "detail": {
            "operation":"async_ocr",
        }
    }
    res_str=service.requestV2(
        data2
    )
    json_str = res_str.decode('utf-8')
    return json_str


# @tool(description="获取OCR识别结果")
def get_ocr_result(name: str, task_id: int) -> str:
    """获取OCR识别结果 参数为微服务的name和任务id"""
    data2={
        "route_operation":"route",
        "id_str":name,
        "detail": {
            "operation":"get_async_task",
            "id":task_id,
        }
    }
    res_str=service.requestV2(
        data2
    )
    json_str = res_str.decode('utf-8')
    return json_str
