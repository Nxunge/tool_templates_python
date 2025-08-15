import json
import os

# 配置文件路径
CONFIG_FILE = "config.json"

# 默认配置
DEFAULT_CONFIG = {
    "port" : 13001
}

# 全局配置变量
config = None


def load_config():
    global config
    # 如果配置文件不存在，先创建
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        print(f"已创建默认配置文件: {CONFIG_FILE}")

    # 读取配置文件
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        config = json.load(f)
    print("配置已加载:", config)
