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

QL_HEADERS = None


def get_authorization():
    """
    获取Token
    """
    global QL_HEADERS
    logging.info("[青龙] 刷新授权码")
    url = f'{OPEN_URL}/auth/token?client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
    res = requests.get(url, timeout=60)
    if res.status_code != 200:
        logging.info("[青龙] 请检查网络配置, 状态码：{}".format(res.status_code))
        exit(1)
    resp_data = res.json()
    if resp_data['code'] != 200:
        logging.info("[青龙] 获取授权码失败, 响应：{}".format(resp_data))
        exit(1)
    QL_HEADERS = {
        "Authorization": f"Bearer {res.json()['data']['token']}"
    }
    logging.info("[青龙] 授权码：{}".format(QL_HEADERS['Authorization']))

    return QL_HEADERS


get_authorization()

logging.info('[青龙] 加载配置文件完成')
