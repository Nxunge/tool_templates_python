import warnings
import getpass
from utils.config_manager import config, load_config
from utils.log_manager import setup_logger
import logging
import pkgutil
import importlib
import plugins
import tests
import threading
import signal
import sys
import requests
import time
import http.server
import ctypes

warnings.filterwarnings(
    "ignore",
    message="You are using cryptography on a 32-bit Python on a 64-bit Windows Operating System."
)

def is_admin():
    """检测是否管理员权限"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """如果不是管理员，重新以管理员身份启动自己"""
    if not is_admin():
        print("当前不是管理员，正在请求管理员权限...")
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        )
        sys.exit(0)

def runModules(package, target_func_name):
    """执行指定包下的所有模块里的目标函数"""
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        full_name = f"{package.__name__}.{module_name}"
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
    run_as_admin()  # 👈 入口处检查并申请管理员权限
    setup_logger()
    logging.info("程序启动")

    # 先运行 plugins 下的 run()
    runModules(plugins, "run")

    # 如果命令行参数包含 --test，则执行 test 包下的 test()
    if "--test" in sys.argv:
        runModules(tests, "test")

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
