import socket
import time
from time import sleep

from src.send.send_data import Response
from src.send.send_servcie import SendService


router_to="general_0"
requests_data = {
    "router_to":router_to,
    "operation":"request",
    "slice_len":0,
    "body":{}
}
requests_get_yolo_data = {
    "router_to":router_to,
    "operation":"get_yolo_model",
    "slice_len":0,
    "body":{

    }
}
request_wgc_data={
    "router_to":router_to,
    "operation":"wgc",
    "slice_len":0,
    "body":{
        "target" :"明日方舟"
    }
}
request_ocr_data = {

    "router_to":router_to,
    "operation":"ocr",
    "slice_len":0,
    "body":{
        "threshold":0.8,
        # "KeepX":597,
        # "KeepY":524,
        # "KeepW":1024,
        # "KeepH":1024,
        # "key_word":"前往上一次作战"
    }
}

request_win32_data={
    "router_to":router_to,
    "operation":"win32_input",
    "slice_len":0,
    "body":{
        "target":"明日方舟",
        "inputs":[
            {
                "type":"move_mouse",
                "x":1173,
                "y":600,
            },
            {
                "type":"click_mouse",
                "click_name":"left_click",
                "count":1,
            },
            {
                "type":"drag_mouse",
                "x":-400,
                "y":-291,
                "click_name":"left_click",
                "step":10,
            }

        ]
    }
}
request_yolo_ui_data={
    "router_to":router_to,
    "operation":"yolo",
    "slice_len":0,
    "body":{
        "model_name":"ui_test1",

    }
}
requests_sen_key = {
    "router_to":router_to,
    "operation":"win32_input",
    "slice_len":0,
    "body":{
        "target":"明日方舟",
        "inputs":[
            {
                "type":"move_mouse",
                "x":1173,
                "y":600,
            },
            {
                "type":"send_input",
                "key":"ESC",
                "duration":1000,
            }
        ]
    }
}
service=SendService()
service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
def res_request():

    res_str1 = service.requestV3(requests_sen_key)
    print(res_str1.unserialize())
    # sleep(1)
    # for _ in range(1):
    #     start = time.perf_counter()
    #     res_str1 = service.requestV3(request_yolo_ui_data)
    #     end = time.perf_counter()
    #     print(f"耗时: {(end - start) * 1000:.3f} ms")
    #
    #     import json
    #     print(json.dumps(res_str1.unserialize().get("body"), indent=4, ensure_ascii=False))



# pass
if __name__ == '__main__':
    res_request()
    pass
