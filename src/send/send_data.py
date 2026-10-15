
import json

# auto head(int Sharding,sockaddr_in& addr){
#
#     char ip_str[INET_ADDRSTRLEN];
# const std::string requester_ip(inet_ntop(AF_INET,&(addr.sin_addr), ip_str,INET_ADDRSTRLEN));
# const uint16_t requester_port = ntohs(addr.sin_port);
#
# data["sharding"]  =Sharding;
# data["request_ip"]=requester_ip;
# data["request_port"] =requester_port;
# data["key"]="";
# }
class Response:


    def __init__(self):
        self.data  = None
        self.info  = None
        self.state = None

    def unserialize(self, str_data):
        self.data  = json.loads(str_data)
        self.info  = self.data.get('info', None)
        self.state = self.data.get('state', None)
        pass


