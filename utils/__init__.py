# -*- coding: utf-8 -*-
import logging
import os

import requests

logging.info('[青龙] 开始加载配置文件')
OPEN_URL = ''

API_URL = ''

QLHost = None

ql_host = os.environ.get('ql_host')
if ql_host:
    QLHost = ql_host
    OPEN_URL = f'{ql_host}/open'
    API_URL = f'{ql_host}/api'
else:
    OPEN_URL = 'http://127.0.0.1:5700/open'
    API_URL = 'http://127.0.0.1:5700/api'

QlBaseUrl = None

ql_base_url = os.environ.get('QlBaseUrl')
if ql_base_url:
    QlBaseUrl = ql_base_url
    QlBaseUrl = QlBaseUrl.strip('/')
    if QlBaseUrl:
        OPEN_URL = OPEN_URL.replace('/open', f'/{QlBaseUrl}/open')
        API_URL = API_URL.replace('/api', f'/{QlBaseUrl}/api')

CLIENT_ID = os.environ.get('javbus_client_id')
CLIENT_SECRET = os.environ.get('javbus_client_secret')

logging.info('[青龙] 加载配置文件完成')
