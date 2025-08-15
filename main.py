import warnings
import getpass
from utils.config_manager import config,load_config
from utils.log_manager import setup_logger
import logging
import pkgutil
import importlib
import plugins

warnings.filterwarnings(
    "ignore",
    message="You are using cryptography on a 32-bit Python on a 64-bit Windows Operating System."
)

# 要执行的函数名
target_func_name = "run"

def runPlugins():
    for _, module_name, _ in pkgutil.iter_modules(plugins.__path__):
        full_name = f"{plugins.__name__}.{module_name}"
        module = importlib.import_module(full_name)

        if hasattr(module, target_func_name):
            func = getattr(module, target_func_name)
            if callable(func):
                print(f"执行 {full_name}.{target_func_name}()...")
                func()

def main():
    setup_logger()
    load_config()
    logging.info("程序启动")
    runPlugins()
    password = getpass.getpass("运行结束,按任意键退出程序")

if __name__ == "__main__":
    main()