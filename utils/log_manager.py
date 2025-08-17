import os
import time
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from utils.config_manager import config



def setup_logger():
    LOG_DIR = config.get("logdir")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # 文件日志（按天分割）
    log_file = os.path.join(LOG_DIR, "runtime.log")
    file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    file_handler.suffix = "%Y-%m-%d"
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    # 控制台日志
    console_handler = logging.StreamHandler()
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
