#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os

import requests

from notify import print

app_headers = {}

# 环境变量
client_id = os.environ.get('CLIENT_ID')  # 获取client_id
client_secret = os.environ.get('CLIENT_SECRET')  # 获取client_secret

# api地址
open_url = 'http://10.95.182.221:5700/open'
api_url = 'http://10.95.182.221:5700/api'


# 获取Token
def get_token():
    global app_headers
    print("获取授权码")
    url = f'{open_url}/auth/token?client_id={client_id}&client_secret={client_secret}'
    print("请求地址：" + url)
    res = requests.get(url)
    if res.status_code != 200:
        print("请求失败：请检查网络配置")
        print(res.json())
        exit()
    resp_data = res.json()
    if resp_data['code'] != 200:
        print("获取授权码失败")
        print(resp_data)
        exit()
    app_headers = {
        "Authorization": f"Bearer {res.json()['data']['token']}"
    }
    print("获取授权码成功")
    print(app_headers)


# Get请求
def get(url):
    res = requests.get(url, headers=app_headers)
    json = res.json()
    if json['code'] == 200:
        return json
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        get_token()
        return get(url)
    else:
        print(json)
        exit()


# Post请求
def post(url, data):
    res = requests.post(url, headers=app_headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        get_token()
        return post(url, data)
    else:
        print(json)
        exit()


# Put请求
def put(url, data):
    res = requests.put(url, headers=app_headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        get_token()
        return put(url, data)
    else:
        print(json)
        exit()


# Delete请求
def delete(url):
    res = requests.delete(url, headers=app_headers)
    json = res.json()
    if json['code'] == 200:
        return json
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        get_token()
        return delete(url)
    else:
        print(json)
        exit()


def delete_data(url, data):
    res = requests.delete(url, headers=app_headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        get_token()
        return delete_data(url, data)
    else:
        print(json)
        exit()


# 获取全部环境变量
def get_envs():
    url = f'{open_url}/envs'
    res = get(url)
    return res['data']


# 获取单个环境变量
def get_env(name):
    url = f'{open_url}/envs?searchValue={name}'
    res = get(url)
    data = res['data']
    if len(data) == 0:
        return None
    else:
        return data[0]


# 更新单个环境变量
def update_env(name, value):
    url = f'{open_url}/envs'
    data = {
        "id": get_env(name)['id'],
        "name": name,
        "value": value
    }
    res = put(url, data)
    return res


# 添加环境变量
def add_env(name, value):
    url = f'{open_url}/envs'
    data = [
        {
            "name": name,
            "value": value
        }
    ]
    res = post(url, data)
    return res


# 添加环境变量
def add_full_env(name, value, remarks):
    url = f'{open_url}/envs'
    data = [
        {
            "name": name,
            "value": value,
            "remarks": remarks
        }
    ]
    res = post(url, data)
    return res


# 删除环境变量
def delete_env(name):
    url = f'{open_url}/envs'
    data = [
        get_env(name)['id']
    ]
    res = delete_data(url, data)
    return res
