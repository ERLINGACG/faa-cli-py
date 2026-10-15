import socket
import json
# 服务器地址和端口（与你 C++ 服务绑定的保持一致）
SERVER_IP = "127.0.0.1"   # 如果服务跑在本机，就用 127.0.0.1
SERVER_PORT = 8080        # 与你 config.start_port 一致
import time
def udp_test():
    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 发送测试消息
        data = {
            "target": "Endfield",
            "task_type" : "list",
             "task_list": [ {
                     "task_type": "get_ocr",
                      "ocr_params": {
                           "threshold":0.01,
                           "unclip_ratio": 2.00,
                           "pad":1
                      }
                }
             ]
        }
        start_time = time.time()
        message = json.dumps(data)
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        print(f"发送消息: {message}")

        # 设置超时（防止一直等待回复）
        sock.settimeout(30)

        # 尝试接收回复（最多 1024 字节）
        data, addr = sock.recvfrom(65535)
        end_time = time.time()
        print(f"耗时: {end_time - start_time} 秒")
        print(f"收到回复: {data.decode()} 来自 {addr}")

        response = json.loads(data.decode())
        target_text = "行动手册"
        for item in response.get("keys", []):
            if item.get("text") == target_text:
                rect = item["rect"]
                cx = rect["x"]
                cy = rect["y"]
                print(f"点击坐标: ({cx}, {cy})")
                # click_at(cx, cy)
                data2={
                    "target": "Endfield",
                    "task_type" : "list",
                    "task_list": [
                        {
                            "task_type": "win32_no_det",
                            "input_list": [
                                {
                                    "delay_time": 3000,
                                    "mouse_x": cx/1.25,
                                    "mouse_y": cy/1.25,
                                    "click":   True,
                                    "click_type": 1
                                }
                            ]
                        }
                    ]
                }
                message = json.dumps(data2)
                # sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
                break
        else:
            print("未找到目标文本，不执行点击")
        # print(response)

    except socket.timeout:
        print("等待回复超时（服务器可能没有回复逻辑）")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_test()