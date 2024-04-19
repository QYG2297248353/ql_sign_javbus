# -*- coding: utf-8 -*-
import logging

from utils.utils_log_info import task_start, task_end

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    task_start()
    logging.info("测试信息打印")
    task_end()
