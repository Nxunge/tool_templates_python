import warnings
import getpass
from utils.config_manager import config,load_config
from utils.log_manager import setup_logger
import logging
import pkgutil
import importlib
import plugins
import threading
import signal
import sys
import requests
import time
import http.server


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
            if callable(func) and not getattr(func, "skip", False):
                print(f"执行 {full_name}.{target_func_name}()...")
                func()
            else:
                print(f"跳过 {full_name}.{target_func_name}()")

def handle_exit(signum, frame):
    print(f"退出: {signum}, 正在退出")
    sys.exit(0)

def main():
    setup_logger()
    logging.info("程序启动")
    runPlugins()
    logging.info("运行成功")
    # 捕获信号
    signal.signal(signal.SIGINT, handle_exit)   # Ctrl+C
    signal.signal(signal.SIGTERM, handle_exit)  # kill
    try:
        while True:
            time.sleep(3600)  # 无限阻塞，但不会占用 CPU
    except KeyboardInterrupt:
        print("KeyboardInterrupt 捕获，退出")

if __name__ == "__main__":
    main()