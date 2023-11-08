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

import requests as requests
from bs4 import BeautifulSoup

from qlApi import init, get_env, add_env, update_env

base_url = 'https://www.javbus.com/forum/'

# 通过环境变量获取Cookie 用于登录
salt_key = os.environ.get('javbus_saltkey')
auth = os.environ.get('javbus_auth')
username = os.environ.get('javbus_username')

# 请求页面
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Cookie': f'saltkey={salt_key};auth={auth};'
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
    if cookie:
        headers['Cookie'] = cookie
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('开始解析: 签到结果')
        soup = BeautifulSoup(response.text, 'html.parser')
        title = soup.find('title').text
        if '登錄' in title:
            print('Tip：账户未登录，请设定环境变量！')
            return
        a = soup.find('a', text=username)
        if a:
            cookies_envs = response.cookies
            add_env('javbus_cookie', cookies_envs)
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


def validation_initialization_parameters():
    init()
    if not salt_key or not auth or not username:
        print('请设置环境变量!!!')
        print('请参考文档: https://github.com/QYG2297248353/ql_sign_javbus')
        exit()
    # 尝试恢复cookie
    global cookie
    # 读取环境变量
    javbus_cookie = get_env('javbus_cookie')
    if javbus_cookie:
        cookie = javbus_cookie
        headers['Cookie'] = cookie


if __name__ == '__main__':
    validation_initialization_parameters()
    javbus_sign = get_env('javbus_sign')
    if javbus_sign == None:
        javbus_sign_data = {
            'sign': False,
            'date': f'{time.strftime("%Y-%m-%d", time.localtime())}'
        }
        add_env('javbus_sign', json.dumps(javbus_sign_data))
    else:
        javbus_sign_data = json.loads(javbus_sign)
        if javbus_sign_data['date'] == f'{time.strftime("%Y-%m-%d", time.localtime())}':
            print('Tip：今天已经签到过了！')
            exit()
    sign()
