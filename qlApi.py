# 青龙面板 接口
import os

import requests

# 青龙面板地址
ql_path = os.environ.get('QL_PATH')
ql_url = 'http://127.0.0.1:5700'
if ql_path:
    # 拼接青龙面板地址 ql_url + ql_path
    ql_url = ql_url + ql_path

# 青龙面板授权码
ql_key = os.environ.get('QL_KEY')
ql_secret = os.environ.get('QL_SECRET')

# 获取青龙面板 Token
ql_token = \
    requests.get(f'{ql_url}/open/auth/token?client_id={ql_key}&client_secret={ql_secret}').json()['data']['data'][
        'token']

# 请求头
headers = {
    "Authorization": f"Bearer {ql_token}"
}


# 导出青龙面板环境变量 函数
def export_envs():
    # 获取青龙面板环境变量
    envs = requests.get(f'{ql_url}/open/envs', headers=headers).json()['data']['data']
    print(envs)
    # 青龙面板环境变量字典
    envs_dict = {}
    for env in envs:
        envs_dict[env['name']] = env['value']
    return envs_dict
