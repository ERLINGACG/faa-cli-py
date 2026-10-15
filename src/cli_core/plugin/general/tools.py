from src.cli_core.llm.llm_skills import FaaLLmSkills
from langchain_core.tools import tool

import json
import socket

from langchain_core.tools import tool

from src.send.send_servcie import SendService
skills = FaaLLmSkills()
skills.load()


service=SendService()
service.socket(socket.socket(socket.AF_INET, socket.SOCK_DGRAM))
DPI= 1.25


@tool(description="发送请求 参数为json字符串")
def send_request(request:str) -> str:
    """发送请求 参数为json字符串"""
    res_str=service.requestV3(
        json.loads(request)
    )
    return json.dumps(res_str.unserialize().get("body"))


@tool(description= "获取所有skill")
def get_all_skill():
    return skills.get_all_skill()


@tool(description= "加载一个skill")
def load_skill(skill_name:str):
    return skills.load_skill(skill_name)
