import asyncio
import socket

from src.send.send_servcie import SendService
import json

DPI=1.25
def test():
    print("hello world")

data2 = {
    "global_app": "明日方舟",
    "controller" : "win32",
    "cap_type"   : "wgc",
    "event_list" : [
        {
            "event_type":"send_input",
            "description":{
                "input":[
                    {

                        # "is_post":False,
                        # "key":"S",
                        # "delay_time":3000
                        "move_x":123/DPI,
                        "move_y":661/DPI,
                        # "click":"left_click",
                    }
                ]
            }
        }
    ]
}
data4 = {
    "global_app": "Endfield",
    "controller" : "win32",
    "cap_type"   : "wgc_",
    "event_list" : [
        {
            "event_type":"send_input",
            "description":{
                "input":[
                    {
                        # "keys":[
                        #     {
                        #         "key":"A",
                        #         "delay_time":5000
                        #     },
                        #     {
                        #         "key":"W",
                        #         "delay_time":3000
                        #     }
                        # ]
                    },
                    {
                        "click":"left_click",
                        "delay_time":300,
                        "count":5
                    },
                    {
                        "key":"SHIFT"
                    }
                ]
            }
        }
    ]
}



data1 = {
        "global_app":"明日方舟",
        "controller" : "win32",
        "cap_type"   : "wgc",
        "event_list" : [
            {
                "event_type":"ocr_img"
            }
        ]
    }

def test_win32_controller_1():
    send_service=SendService()

    send_service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    res=send_service.request(
        data1
    )
    print(json.dumps(res.toDetail(), indent=2, ensure_ascii=False))




if __name__ == '__main__':
     # test()

     test_win32_controller_1()
     # asyncio.run(main())
