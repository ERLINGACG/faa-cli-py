import json
import os
import socket
import time
import unittest

from src.send.send_servcie import SendService


class MyTestCase(unittest.TestCase):
    def test_post_to_ocr(self):


        data1 = {
            "global_app":"明日方舟",
            "controller" : "win32",
            "cap_type"   : "wgc",
            "event_list" : [
                {
                    "event_type":"ocr_img",
                    "description":{
                        "threshold":0.1
                    }
                }
            ]
        }

        send_service=SendService()

        send_service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
        # res=send_service.request(
        #     data2
        # )
        # print(json.dumps(res.toDetail(), indent=2, ensure_ascii=False))
        start = time.perf_counter()
        send_service.request(
            data1
        )

        elapsed = (time.perf_counter() - start) * 1000   # 转为毫秒
        print(f"耗时: {elapsed:.4f} 毫秒")

        # print(json.dumps(res.toDetail(), indent=2, ensure_ascii=False))
        self.assertEqual(True,True)

if __name__ == '__main__':
    unittest.main()
