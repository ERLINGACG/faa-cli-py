import socket
import time

from src.send.send_data import Response
from src.send.send_servcie import SendService


def wgc_request():
    service=SendService()
    service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
    data2={
        "route_operation":"route",
        "name_str":"arknights_0",
        "detail": {
            # "operation":"get_async_task",
            "operation":"async_ocr",
            "id":4,
            # "operation":"wgc"
        }
    }
    start_time=time.time()
    res_str=service.requestV2(
        data2
    )
    end_time=time.time()
    print(f"耗时: {end_time-start_time} 秒")
    json_str = res_str.decode('utf-8')

    response=Response()
    response.unserialize(json_str)


    print(response.info)
    print(response.state)
# pass
if __name__ == '__main__':
    wgc_request()
    pass
