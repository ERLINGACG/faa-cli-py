from langchain_core.messages import HumanMessage
from rich.console import Console

from src.cli_core.cmd.cli_cmd import CliCmd
from src.cli_core.llm.llm_model import FaaLLmModel
from src.cli_core.llm.llm_token import FaaLLmToken
from src.cli_core.plugin.plugin_register import PluginRegister
from src.cli_core.rt.runner import Runner
from src.iconfig.config import Config
import src.cli_core.rt.runner

runner = Runner()
config=Config()
register=PluginRegister()
register.scan()
faa_llm= (
    FaaLLmModel().
    config(config).
    build().
    bind_tools(register.list())
)
faa_llm.load("default")
if __name__ == "__main__":
    runner.build(faa_llm)
    runner.build_cmd()
    runner.start()
    runner.join()
