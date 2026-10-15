from langchain_core.messages import HumanMessage
from rich.console import Console

from src.cli_core.cmd.cli_cmd import CliCmd
from src.cli_core.llm.llm_model import FaaLLmModel
from src.cli_core.llm.llm_token import FaaLLmToken
from src.cli_core.plugin.plugin_register import PluginRegister
from src.iconfig.config import Config

console = Console()

def call(token:FaaLLmToken):
    console.print(f"[grey50]{token.token}[/grey50]", end='')




def run():
    config=Config()
    register=PluginRegister()
    register.scan()

    faa_llm= (
        FaaLLmModel().
              config(config).
               build().
              bind_tools(register.list())
    )
    token=FaaLLmToken()
    faa_llm.load("default")
    running=True

    def exit_cmd():
        nonlocal running
        running=False

    def dump_cmd():
        faa_llm.dump()

    def clear_cmd():
        console.clear()

    def history_clear():
        faa_llm.clear()
        pass


    cmd=(CliCmd().
        register(
            "/exit",[],
            exit_cmd,
        ).register(
            "/dump",[],
            dump_cmd,
        ).register(
            "/clear",[],
            clear_cmd,
        ).register(
            "/history_clear",[],
            history_clear,
        )
    )



    while True:
        message= console.input("[green]○ | user -> [/green]")
        if not message:
            continue
        if message[0]!='/':
            console.print("[yellow]○ | assistant -> [/yellow]",end='')
            faa_llm.streamV2(HumanMessage(content=message),token,call)
            console.print("\n")
        else:
            cmd.run(message)

        if not running:
            console.print("[red]bye[/red]")
            faa_llm.save("default")
            break
        pass

    pass


if __name__ == '__main__':
    run()
    pass