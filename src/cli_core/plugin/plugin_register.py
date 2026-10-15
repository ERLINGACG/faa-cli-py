import pkgutil
import importlib

from langchain_core.tools import BaseTool

from src.cli_core import plugin
class PluginRegister:

    tools_list=[]

    def scan(self):
        self._scan_package(plugin, plugin.__name__)

    def _scan_package(self, pkg, pkg_name):
        """递归扫描包及其所有子模块"""
        for module_info in pkgutil.iter_modules(pkg.__path__, prefix=pkg_name + "."):
            full_name = module_info.name
            try:
                mod = importlib.import_module(full_name)
            except Exception as e:
                print(f"导入 {full_name} 失败: {e}")
                continue

            # 提取工具
            module_tools = [
                obj for _, obj in vars(mod).items()
                if isinstance(obj, BaseTool)
            ]
            if module_tools:
                self.tools_list.extend(module_tools)
                # print(f"从 {full_name} 找到 {len(module_tools)} 个工具")

            # 如果是子包，递归进入
            if module_info.ispkg:
                self._scan_package(mod, full_name)

    def register(self,tools):
        self.tools_list=tools
        pass

    def list(self):
        return self.tools_list
    pass


if __name__ == "__main__":
    register=PluginRegister()
    register.scan()
    print(register.list())
