from src.cli_core.cmd.cli_cmd import CliCmd

cmd=CliCmd()


def list_cmd(args):
    print(args)

def exit_cmd():
    print("exit")
if __name__ == "__main__":
    cmd.register(
        "/list",[
        {
            "name":"-t1",
            "type":int,
        }
    ],list_cmd
    ).register("/exit",[],exit_cmd)
    cmd.run("/list -t1 123")
    cmd.run("/exit")
