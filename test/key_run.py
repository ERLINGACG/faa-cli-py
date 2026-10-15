import socket
import json
# 服务器地址和端口（与你 C++ 服务绑定的保持一致）
SERVER_IP = "127.0.0.1"   # 如果服务跑在本机，就用 127.0.0.1
SERVER_PORT = 8080        # 与你 config.start_port 一致

def udp_test():
    # 创建 UDP 套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # 发送测试消息
        data = {
            "target": "Endfield",
            "task_type" : "list",
            "task_list": [
                {
                    "task_type": "win32_no_det",
                    "input_list": [
                        {
                            "delay_time": 1000,
                            "mouse_x": -1,
                            "mouse_y": -1,
                            "key": "W"
                        },{
                            "delay_time": 1000,
                            "key": "A"
                        },{
                            "delay_time": 1000,
                            "key": "ESC"
                        }
                    ]
                }
            ]
        }
        message = json.dumps(data)
        sock.sendto(message.encode(), (SERVER_IP, SERVER_PORT))
        print(f"发送消息: {message}")

        # 设置超时（防止一直等待回复）
        sock.settimeout(30)

        # 尝试接收回复（最多 1024 字节）
        data, addr = sock.recvfrom(65535)
        print(f"收到回复: {data.decode()} 来自 {addr}")

    except socket.timeout:
        print("等待回复超时（服务器可能没有回复逻辑）")
    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    udp_test()