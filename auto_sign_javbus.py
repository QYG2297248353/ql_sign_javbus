# -*- coding: utf-8 -*-
"""
File: auto_sign_javbus.py
Author: 萌森工作室
Date: 2023/11/08
cron: 0 2 * * *
new Env('JavBus论坛签到');
Description: 论坛自动签到-每天签到获取里程和积分
Update: 2023/11/08
"""
import json
import logging
import time

import requests
from bs4 import BeautifulSoup

from core.core_javbus import auto_sign_javbus

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    auto_sign_javbus()
