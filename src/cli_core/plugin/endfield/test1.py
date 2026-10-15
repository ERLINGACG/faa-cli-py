import json
import socket
from time import sleep

from langchain_core.tools import tool

from src.send.send_servcie import SendService

service=SendService()
service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

# @tool(description="获取OCR识别结果")
def get_ocr():
    res=service.request(
        {
            "global_app": "Endfield",
            "controller" : "win32",
            "cap_type"   : "wgc",
            "event_list" : [
                {
                    "event_type":"ocr_img"
                }
            ]
        }
    )
    return json.dumps(res.toDetail(), indent=2, ensure_ascii=False)

# @tool(description="发送按键,字母仅支持大写")
def send_key( key: str, sleep_time: int=0, delay_time: int=500):
    """
   发送一个按键。
   Args:
       sleep_time: 进行操作前等待的时间,默认0ms。（毫秒）
       key: 要发送的按键，字母必须为大写 A-Z。
       delay_time: 持续按下按键的时间，默认 500ms（毫秒）。
   """

    print(f"等待时间{sleep_time},发送按键: {key}, 延迟时间: {delay_time}ms")
    sleep(sleep_time/1000)
    send_data = {
        "global_app": "Endfield",
        "controller" : "win32",
        "cap_type"   : "wgc_",
        "event_list" : [
            {
                "event_type":"send_input",
                "description":{
                    "input":[
                        {
                            "key":key,
                            "delay_time":delay_time
                        }
                    ]
                }
            }
        ]
    }
    res=service.request(send_data)
    return json.dumps(res.toDetail(), indent=2, ensure_ascii=False)
    pass
