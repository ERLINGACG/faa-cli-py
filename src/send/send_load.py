import json

from dataclasses import dataclass, asdict, field

from requests import head


@dataclass
class LoadHead:
    operation:    str = ""
    router_to:    str = ""
    request_ip:   str = ""
    request_port: int = 0
    slice_len:    int = 0

    def serialize(self, data: dict):
        # 只取已知字段，未知字段忽略
        for k in self.__dataclass_fields__:
            if k in data:
                setattr(self, k, data[k])

    def unserialize(self) -> str:
        return json.dumps(asdict(self))


# @dataclass
class LoadBody:


    def __init__(self):
        self.body = list()

    def serialize(self,data : dict):
        self.body = dict()
        self.body = data.get("body", dict())

    def list(self):
        self.body=list()
    def slices(self,data:dict):
        self.body.append(data)


    def to_string(self):
        return json.dumps(self.body, ensure_ascii=False, indent=2) if len(self.body) else "[]"



class SendLoad:

    head: LoadHead
    body: LoadBody
    load: dict


    def __init__(self):
        self.head = LoadHead()
        self.body = LoadBody()
        self.load = dict()


    def serialize(self, data: dict):
        self.head.serialize(data)
        self.body.serialize(data)
        self.load = data

    def unserialize(self) :
        return {
            **asdict(self.head),
            "body":self.body.body,
        }

    def slices(self,data:dict):
        self.body.slices(data)

    def get_head(self):
        return self.head

    def get_body(self):
        return self.body


    pass
