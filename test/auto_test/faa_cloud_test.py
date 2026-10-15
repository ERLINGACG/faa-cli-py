import json
import socket
import time
import unittest

from src.send.send_servcie import SendService


class TestFaaCloud(unittest.TestCase):



    def __init__(self, methodName='runTest'):   # 必须接收 methodName 参数
        super().__init__(methodName)            # 务必调用父类 __init__
        self.service=SendService()
        self.service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))

        pass

    def close(self):
        self.service.close()


    def test_input_move(self):

        data2={
            "route_operation":"route",
            "name_str":"arknights_0",
            "detail": {
                "operation":"win32_input",
                "inputs":[
                    {
                        "type":"move_mouse",
                        "x":997,
                        "y":103,
                    },
                    # {
                    #
                    #     "type":"send_input",
                    #     "duration":100,
                    #     "key":"ESC"
                    # }
                ],

            }
        }
        start_time=time.time()
        res_str=self.service.requestV2(
            data2
        )
        end_time=time.time()
        print(f"耗时: {end_time-start_time} 秒")
        json_str = res_str.decode('utf-8')
        print(json_str)
        self.close()
        self.assertEqual(True, True)  # add assertion here

    # def test_input_rotate(self):
    #
    #     data2={
    #         "route_operation":"route",
    #         "id_str":"arknights_0",
    #         "detail": {
    #             "operation":"win32_input",
    #             "inputs":[
    #                 {
    #                     "type":"move_mouse",
    #                     "move_x":100,
    #                     "move_y":100,
    #                 },
    #                 {
    #                     "type":"rotate_mouse",
    #                     "angleX":180.0,
    #                     "angleY":100.0,
    #                     "step":50,
    #                     "duration":50,
    #                 }
    #             ],
    #
    #         }
    #     }
    #     start_time=time.time()
    #     res_str=self.service.requestV2(
    #         data2
    #     )
    #     end_time=time.time()
    #     print(f"耗时: {end_time-start_time} 秒")
    #     json_str = res_str.decode('utf-8')
    #     print(json_str)
    #     self.close()
    #     self.assertEqual(True, True)  # add assertion here
    #     pass
    #
    # def test_input_click(self):
    #     data2={
    #         "route_operation":"route",
    #         "id_str":"arknights_0",
    #         "detail": {
    #             "operation":"win32_input",
    #             "inputs":[
    #                 {
    #                     "type":"move_mouse",
    #                     "move_x":100,
    #                     "move_y":100,
    #                 },
    #                 {
    #                     "type":"click_mouse",
    #                     "click_name":"left_click",
    #                     "duration":100,
    #                     "count":10
    #                 }
    #             ],
    #
    #         }
    #     }
    #     start_time=time.time()
    #     res_str=self.service.requestV2(
    #         data2
    #     )
    #     end_time=time.time()
    #     print(f"耗时: {end_time-start_time} 秒")
    #     json_str = res_str.decode('utf-8')
    #     print(json_str)
    #     self.close()
    #     self.assertEqual(True, True)  # add assertion here
    #     pass

    # def test_input_ocr(self):
    #     data2={
    #         "route_operation":"route",
    #         "name_str":"arknights_0",
    #         "detail": {
    #             "operation":"wgc",
    #         }
    #     }
    #     start_time=time.time()
    #     res_str=self.service.requestV2(
    #         data2
    #     )
    #     end_time=time.time()
    #     print(f"耗时: {end_time-start_time} 秒")
    #     json_str = res_str.decode('utf-8')
    #     print(json_str)
    #     self.close()
    #     self.assertEqual(True, True)  # add assertion here
    #     pass





if __name__ == '__main__':
    unittest.main()
