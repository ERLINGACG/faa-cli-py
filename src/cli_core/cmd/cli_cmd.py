import argparse


class CliCmd:

    parser = argparse.ArgumentParser()

    mapper = [
    ]
    subparsers = parser.add_subparsers(dest="command")
    def register(self, cmd: str,args,func):

        parser = self.subparsers.add_parser(cmd)

        if len(args)>0:
            for arg in args:
                parser.add_argument(arg["name"],type=arg["type"])

        self.mapper.append({
            "cmd":cmd,
            "func":func,
        })
        return self

    def run(self, cmd: str):
        try:
            namespace, unknown = self.parser.parse_known_args(cmd.split())
            if unknown:
                print(f"未知命令或参数: {unknown}")
                return
            args_dict = vars(namespace)
            command = args_dict.get('command')  # 假设子命令dest为'command'
            if command is None:
                print("未提供命令")
                return
            for item in self.mapper:
                if command == item["cmd"]:
                    func = item["func"]
                    # 需要提取其他参数，注意排除'command'
                    params = [v for k, v in args_dict.items() if k != 'command']
                    func(*params)
                    break
            else:
                print(f"未知命令: {command}")
        except SystemExit:
            # 以防parse_known_args仍然因为某些原因退出（例如错误参数格式）
            pass

        except Exception as e:
            print(f"错误: {e}")


                # func()


