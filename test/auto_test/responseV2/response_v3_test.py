import socket
import time
from time import sleep

from src.send.send_data import Response
from src.send.send_servcie import SendService

router_to = "general_0"
requests_data = {
    "router_to":router_to,
    "operation":"request",
    "slice_len":0,
    "body":{}
}

service=SendService()
service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
service.setTimeout(3)
def res_request():
    response = service.requestV3(requests_data)
    print(response.unserialize())
    pass

if __name__ == "__main__":
    res_request()
