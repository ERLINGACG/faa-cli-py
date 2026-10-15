
# struct Ack{
#     int32_t     code{0};
#     std::string starts{};
#     std::string error_info{};
# }
class EventAck:
    code=0
    starts=""
    error_info=""
    detail={}

    def __init__(self):
        pass

    def build(self, result):
        self.code=result["code"]
        self.starts=result["starts"]
        self.error_info=result["error_info"]
        self.detail=result["detail"]

        return self



    def toDetail(self):
        return {
            "code":self.code,
            "starts":self.starts,
            "error_info":self.error_info,
            "detail":self.detail
        }
    pass

