from dataclasses import dataclass
from enum import Enum



class EventEnum(Enum):
    USER_CALL = "user_call"
    SLEEP = "sleep"
    WAKE  = "wake"
    EXIT  = "exit"
    USER_INPUT  = "user_input"
    ASSI_OUTPUT = "assi_output"



@dataclass
class RunnerEvent:
    event: EventEnum
    data: dict = None
    name: str = None

