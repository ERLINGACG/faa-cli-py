import time

from src.data.ack_call import EventAck
import json

from src.send.send_load import LoadHead, SendLoad


class SendService:

    _socket=None


    def __init__(self):
        pass
        # self.socket = None

    def socket(self,sock):
        self._socket=sock
        return self

    def close(self):

        if self._socket is not None:
            self._socket.close()
            self._socket=None
        pass

        pass

    def setTimeout(self,timeout=300):
        self._socket.settimeout(timeout)
        return self

    def request(self,message,ip="127.0.0.1",port=8080,timeout=300,recv_size=65535)->EventAck:

        if self._socket is None:
            raise RuntimeError("socket is None")

        message = json.dumps(message)

        self._socket.sendto(message.encode(), (ip, port))
        self._socket.settimeout(timeout)
        result,addr= self._socket.recvfrom(recv_size)

        result=result.decode()
        result=json.loads(result)

        return EventAck().build(result)

    def requestV2(self,message,ip="127.0.0.1",port=8080,timeout=300,recv_size=65535):

        if self._socket is None:
            raise RuntimeError("socket is None")

        message = json.dumps(message)

        self._socket.sendto(message.encode(), (ip, port))
        self._socket.settimeout(timeout)
        result,addr= self._socket.recvfrom(recv_size)

        return result
    def requestV3(self, message, ip="127.0.0.1", port=8080, recv_size=65535):

        if self._socket is None:
            raise RuntimeError("socket is None")


        message = json.dumps(message)


        self._socket.sendto(message.encode(), (ip, port))
        result,addr= self._socket.recvfrom(recv_size)


        load = SendLoad()
        load.serialize(json.loads(result))
        print(load.get_head().slice_len)


        if load.head.slice_len>0:
            load.body.list()
        for _ in range(load.head.slice_len):
            result,addr= self._socket.recvfrom(recv_size)
            load.slices(json.loads(result))


        return load

    def recv(self,recv_size=65535):
        if self._socket is None:
            raise RuntimeError("socket is None")
        result=self._socket.recvfrom(recv_size)
        return result





