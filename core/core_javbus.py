import json
import logging
import os
import time

import requests
from bs4 import BeautifulSoup

from core import SALT_KEY, AUTH, USERNAME, JAVBUS_RECORD_PATH, JAVBUS_COOKIES, JAVBUS_BASE_URL, JAVBUS_HEADERS, PROXIES, \
    JAVBUS_COOKIE
from notify import send
from utils.utils_ql_api import add_update_env

cookies = None


def init_record_dir():
    year = time.strftime('%Y', time.localtime())
    month = time.strftime('%m', time.localtime())
    record_dir = os.path.join(JAVBUS_RECORD_PATH, year, month)
    if not os.path.exists(record_dir):
        os.makedirs(record_dir)
        with open(os.path.join(record_dir, 'record.json'), 'w') as f:
            f.write(json.dumps({}, indent=4, ensure_ascii=False))
    return record_dir


def has_signed():
    record_dir = init_record_dir()
    record_file = os.path.join(record_dir, 'record.json')
    with open(record_file, 'r') as f:
        record = json.load(f)
    today = time.strftime('%Y-%m-%d', time.localtime())
    return record.get(today, False)


def sign_today(results=True):
    if JAVBUS_COOKIE:
        record_dir = init_record_dir()
        record_file = os.path.join(record_dir, 'record.json')
        with open(record_file, 'r') as f:
            record = json.load(f)
            f.close()
        today = time.strftime('%Y-%m-%d', time.localtime())
        if record.get(today, False):
            logging.info('[JavBus] 今日已签到')
            return
        record[today] = results
        with open(record_file, 'w') as f:
            f.write(json.dumps(record, indent=4, ensure_ascii=False))
            f.close()
        if results:
            send('[青龙] JavBus论坛签到', '签到成功，本月累计签到: %s 天' % count_mouth_signed())
        else:
            send('[青龙] JavBus论坛签到', '签到失败')


def count_mouth_signed():
    record_dir = init_record_dir()
    record_file = os.path.join(record_dir, 'record.json')
    with open(record_file, 'r') as f:
        record = json.load(f)
    today = time.strftime('%Y-%m', time.localtime())
    count = 0
    for key in record.keys():
        if key.startswith(today):
            count += 1
    return count


def init_env_param():
    logging.info('[JavBus] 初始化环境变量')
    if not SALT_KEY or not AUTH or not USERNAME:
        print('[JavBus] 无法读取环境变量, 请参考文档: https://github.com/QYG2297248353/ql_sign_javbus')
        exit(1)
    logging.info('[JavBus] 初始化完成')


def sign(retry=10):
    global response
    if retry == 0:
        logging.error('[JavBus] 签到失败')
        sign_today(False)
        return
    try:
        if JAVBUS_COOKIES:
            response = requests.get(JAVBUS_BASE_URL, headers=JAVBUS_HEADERS, cookies=JAVBUS_COOKIES, proxies=PROXIES,
                                    timeout=60)
        else:
            response = requests.get(JAVBUS_BASE_URL, headers=JAVBUS_HEADERS, proxies=PROXIES, timeout=60)
    except Exception as e:
        logging.warning(f'[JavBus] 请求异常： {e}')
        for i in range(5, 0, -1):
            print(f'[JavBus] 重新等待：{i} 秒')
            time.sleep(1)
        sign(retry - 1)

    if response.status_code == 200:
        print('[JavBus] 结果解析')
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        if '登錄' in title:
            logging.error('[JavBus] Cookie 失效，请重新获取')
            sign_today(False)
            return
        has_username = soup.find('a', string=USERNAME)
        if has_username:
            cookies_envs = json.dumps(requests.utils.dict_from_cookiejar(response.cookies))
            add_update_env('javbus_auto_cookie', cookies_envs)
            sign_today()
            logging.info('[JavBus] 签到成功')
        else:
            sign_today(False)
            logging.warning('[JavBus] 签到失败')
    else:
        logging.warning(f'[JavBus] 请求状态码异常： {response.status_code}')
        for i in range(5, 0, -1):
            print(f'[JavBus] 重新等待：{i} 秒')
            time.sleep(1)
        sign(retry - 1)


def auto_sign_javbus():
    """
    自动签到
    """
    init_env_param()
    logging.info('[JavBus] 开始签到')
    sign()
    logging.info('[JavBus] 签到完成')
