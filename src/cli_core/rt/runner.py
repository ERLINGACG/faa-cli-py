import queue
import threading
import time
from queue import Queue

from langchain_core.messages import HumanMessage
from prompt_toolkit import PromptSession
from pyexpat.errors import messages
from rich.console import Console

from src.cli_core.cmd.cli_cmd import CliCmd
from src.cli_core.llm.llm_model import FaaLLmModel
from src.cli_core.llm.llm_token import FaaLLmToken
from src.cli_core.rt.runner_event import RunnerEvent, EventEnum


class Runner:


    def __init__(self):

        self.console = Console()
        self.cmd : CliCmd = CliCmd()
        self.isRunning = True
        self.faaModel = None
        self.event_queue_list : dict = {

            "sleep"    : queue.Queue(),
            "user_call": queue.Queue(),
        }
        self.cli_status = RunnerEvent(
            event=EventEnum.USER_INPUT,
            data={},
            name="user_input",
        )
        # self.test_loop_thread : threading.Thread = threading.Thread(target=self.test_loop)
        self.llm_loop_thread  : threading.Thread = threading.Thread(target=self.llm_loop)
        self.user_loop_thread : threading.Thread = threading.Thread(target=self.user_loop)
        self.session = PromptSession()



    def build(self,faaModel:FaaLLmModel=None):
        self.isRunning=True
        self.cmd = CliCmd()
        self.console = Console()
        self.faaModel = faaModel

        pass



    def build_cmd(self):

        self.cmd.register(
            "/exit",
            [],
            self.exit,
        ).register(
            "/sleep",
            [],
            self.sleep,
        ).register(
            "/wake",
            [],
            self.wake,
        )




        pass

    def sleep(self):
        self.event_queue_list["sleep"].put(
            RunnerEvent(
                event=EventEnum.SLEEP,
                data={
                    "duration": 10,
                },
                name="sleep"
            )
        )




    def wake(self):
        self.event_queue_list["sleep"].put(
            RunnerEvent(
                event=EventEnum.WAKE,
                data={},
                name= "wake",
                )
        )

    def exit(self):
        self.console.print("[bold red]exit[/bold red]")
        self.isRunning=False
        self.event_queue_list["sleep"].put(RunnerEvent(
            event=EventEnum.EXIT,
            data={},
            name= "exit",
            )
        )

    def call(self,message:str):
        self.event_queue_list["user_call"].put(
            RunnerEvent(
                event=EventEnum.USER_CALL,
                data={
                    "message": HumanMessage(content=message),
                },
                name= "user_call",
                )
        )


    def test_loop(self):
        while self.isRunning:
            try:
                event = self.event_queue_list["sleep"].get()

                if event.event == EventEnum.SLEEP:
                    duration = event.data["duration"]
                    start_time = time.time()
                    self.console.print("[bold yellow]sleep is running[/bold yellow]")
                    while time.time() - start_time < duration:
                        try:
                            event = self.event_queue_list["sleep"].get(timeout=0.1)
                        except queue.Empty:
                            pass
                        if event.event == EventEnum.WAKE:
                            self.console.print("[bold yellow]wake is running[/bold yellow]")
                            break
                        pass
                    self.console.print("[bold yellow]sleep is done[/bold yellow]")

                elif event.event == EventEnum.EXIT:
                    self.isRunning=False
            except queue.Empty:
                pass

    def user_loop(self):
        while self.isRunning :



            if self.cli_status.event == EventEnum.USER_INPUT:
                message=self.console.input("[green]○ | user -> [/green]")

                if message == "":
                    continue
                if not message.startswith("/"):
                    self.call(message)
                    self.cli_status = RunnerEvent(
                        event=EventEnum.ASSI_OUTPUT,
                        data={},
                        name="assi_output",
                    )
                else:
                    self.cmd.run(message)
            else :
                time.sleep(0.02)
                continue

            if not self.isRunning:
                break
            pass

    def llm_call(self,token:FaaLLmToken):
        self.console.print(f"[grey50]{token.token}[/grey50]", end='')



    def llm_loop(self):
         if self.faaModel is None:
            return

         while self.isRunning:
             try:
                event = self.event_queue_list["user_call"].get(timeout=0.1)
                message = event.data["message"]
                token = FaaLLmToken()
                self.console.print("[yellow]○ | assistant -> [/yellow]",end='')
                try:
                    self.faaModel.streamV2(message, token, self.llm_call)
                except Exception as e:
                    self.console.print(f"[bold red]error: {e}[/bold red]")
                    continue
                self.console.print("\n")
                self.cli_status = RunnerEvent(
                    event=EventEnum.USER_INPUT,
                    data={},
                    name="user_input",
                )
             except queue.Empty:
                pass



         pass

    def start(self):

        self.user_loop_thread.start()
        self.llm_loop_thread.start()


    def join(self):

        self.user_loop_thread.join()
        self.llm_loop_thread.join()


