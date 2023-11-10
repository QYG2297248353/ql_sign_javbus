#!/usr/bin/env python3
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
import os
import time

import requests
from bs4 import BeautifulSoup

from qlApi import get_env, add_env, update_env, get_token, add_update_env
from notify import print

base_url = 'https://www.javbus.com/forum/'

# 通过环境变量获取Cookie 用于登录
salt_key = os.environ.get('javbus_saltkey')
auth = os.environ.get('javbus_auth')
username = os.environ.get('javbus_username')

# 请求页面
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'
}

cookie = ''

# 签到次数
sign_err_count = 0


# 签到
def sign():
    # 全局变量
    global sign_err_count
    url = base_url
    # cookies 存在则使用cookies
    headers['Cookie'] = f'4fJN_2132_saltkey={salt_key};4fJN_2132_auth={auth}'
    if cookie:
        response = requests.get(url, headers=headers, cookies=cookie)
    else:
        response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('开始解析: 签到结果')
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        if '登錄' in title:
            print('Tip：账户未登录，请设定环境变量！')
            return
        a = soup.find('a', string=username)
        if a:
            # cookie 处理 解析为字典 用于保存 不能使用utils.dict_from_cookiejar
            cookies_envs = json.dumps(requests.utils.dict_from_cookiejar(response.cookies))
            add_update_env('javbus_cookie', cookies_envs)
            print('Tip：账户已登录，签到中...')
            javbus_sign_data = {
                'sign': True,
                'date': f'{time.strftime("%Y-%m-%d", time.localtime())}'
            }
            update_env('javbus_sign', json.dumps(javbus_sign_data))
            print('Tip：签到成功！')
        else:
            print('Tip：签到失败')
    else:
        print('Tip：签到失败，尝试重新签到')
        for i in range(5, 0, -1):
            print(f'重新签到倒计时：{i} 秒')
            time.sleep(1)
        if sign_err_count < 10:
            sign_err_count += 1
            sign()
        else:
            print('Tip：签到失败，退出程序！')
            exit()


# 环境变量
client_id = os.environ.get('CLIENT_ID')  # 获取client_id
client_secret = os.environ.get('CLIENT_SECRET')  # 获取client_secret

# api地址
open_url = 'http://10.95.182.221:5700/open'
api_url = 'http://10.95.182.221:5700/api'

app_headers = {}


def validation_initialization_parameters():
    global cookie
    get_token()
    if not salt_key or not auth or not username:
        print('请设置环境变量!!!')
        print('请参考文档: https://github.com/QYG2297248353/ql_sign_javbus')
        exit()
    print("==========环境检查通过==========")
    # 读取环境变量
    javbus_cookie = get_env('javbus_cookie')
    if javbus_cookie:
        javbus_cookie = json.loads(javbus_cookie['value'])
        # dict 转 cookiejar
        cookie = requests.utils.cookiejar_from_dict(javbus_cookie)
        print("==========历史 Cookie 恢复完成==========")


print('初始化: 环境检查')
validation_initialization_parameters()
javbus_sign = get_env('javbus_sign')
if javbus_sign == None:
    javbus_sign_data = {
        'sign': False,
        'date': f'{time.strftime("%Y-%m-%d", time.localtime())}'
    }
    add_env('javbus_sign', json.dumps(javbus_sign_data))
    print("Tip：首次使用，添加默认记录，签到中...")
else:
    javbus_sign_save = json.loads(javbus_sign['value'])
    if javbus_sign_save['date'] == f'{time.strftime("%Y-%m-%d", time.localtime())}':
        if javbus_sign_save['sign']:
            print("Tip：今日已签到，无需重复签到")
            exit()
    print("Tip：今日未签到，开始签到...")
    sign()
