# -*- coding: utf-8 -*-
import json
import logging
import os

import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

logging.info('[JavBus] 开始加载配置文件')

JAVBUS_BASE_URL = 'https://www.javbus.com/forum/'

JAVBUS_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Accept': '*/*',
    'Host': 'www.javbus.com',
    'Connection': 'keep-alive'
}

JAVBUS_COOKIES = None

JAVBUS_COOKIE = bool(os.environ.get('javbus_cookie', True))
if JAVBUS_COOKIE:
    env_cookie = os.environ.get('javbus_auto_cookie', None)
    if env_cookie:
        logging.info('[JavBus] 检测到历史Cookie')
        javbus_cookie = json.loads(env_cookie)
        if '4fJN_2132_saltkey' in javbus_cookie.keys() and '4fJN_2132_auth' in javbus_cookie.keys():
            JAVBUS_COOKIES = requests.utils.cookiejar_from_dict(javbus_cookie)
            logging.info('[JavBus] 恢复历史Cookie完成')
        else:
            logging.error('[JavBus] Cookie 效验失败')

env_base_url = os.environ.get('javbus_sign_url', None)
if env_base_url:
    JAVBUS_BASE_URL = env_base_url

SALT_KEY = os.environ.get('javbus_saltkey', None)
AUTH = os.environ.get('javbus_auth', None)
# 存在 SALT_KEY and AUTH 且 不存在 JAVBUS_COOKIES
if SALT_KEY and AUTH and not JAVBUS_COOKIES:
    JAVBUS_HEADERS['Cookie'] = f'4fJN_2132_saltkey={SALT_KEY}; 4fJN_2132_auth={AUTH}'
    logging.info('[JavBus] 配置密钥 cookie：4fJN_2132_saltkey {} 4fJN_2132_auth {}'.format(SALT_KEY, AUTH))

USERNAME = os.environ.get('javbus_username', None)

PROXY_ENABLE = bool(os.environ.get('proxy_enable', False))
PROXIES = None
if PROXY_ENABLE:
    logging.info('[JavBus] 检测到代理配置')
    proxy_host = os.environ.get('proxy_host', None)
    proxy_port = os.environ.get('proxy_port', None)
    proxy_username = os.environ.get('proxy_username', None)
    proxy_password = os.environ.get('proxy_password', None)
    if proxy_username and proxy_password:
        PROXIES = {
            'http': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}',
            'https': f'http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}'
        }
    else:
        PROXIES = {
            'http': f'http://{proxy_host}:{proxy_port}',
            'https': f'http://{proxy_host}:{proxy_port}'
        }
    logging.info('[JavBus] 代理配置完成 Host: {} Port: {}'.format(proxy_host, proxy_port))

JAVBUS_RECORD_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'record')

logging.info('[JavBus] 配置文件加载完成')
