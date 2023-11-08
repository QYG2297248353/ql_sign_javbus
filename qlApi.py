#!/usr/bin/env python3
# _*_ coding:utf-8 _*_
import os

import requests

# 环境变量
client_id = os.environ.get('CLIENT_ID')  # 获取client_id
client_secret = os.environ.get('CLIENT_SECRET')  # 获取client_secret

# api地址
open_url = 'http://10.95.182.221:5700/open'
api_url = 'http://10.95.182.221:5700/api'


# 获取Token
def get_token():
    url = f'{open_url}/auth/token?client_id={client_id}&client_secret={client_secret}'
    res = requests.get(url)
    return res.json()['data']['token']


# 初始化
def init():
    # 检查环境变量
    if not client_id or not client_secret:
        print('请设置环境变量')
        exit()
    # 获取token
    token = get_token()
    # 设置请求头
    headers = {
        "Authorization": f"Bearer {token}"
    }
    return headers


# headers
headers = init()


# Get请求
def get(url):
    res = requests.get(url, headers=headers)
    json = res.json()
    if json['code'] == 200:
        return json['data']
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        headers['Authorization'] = f"Bearer {get_token()}"
        return get(url)
    else:
        print(json)
        exit()


# Post请求
def post(url, data):
    res = requests.post(url, headers=headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json['data']
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        headers['Authorization'] = f"Bearer {get_token()}"
        return post(url, data)
    else:
        print(json)
        exit()


# Put请求
def put(url, data):
    res = requests.put(url, headers=headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json['data']
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        headers['Authorization'] = f"Bearer {get_token()}"
        return put(url, data)
    else:
        print(json)
        exit()


# Delete请求
def delete(url):
    res = requests.delete(url, headers=headers)
    json = res.json()
    if json['code'] == 200:
        return json['data']
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        headers['Authorization'] = f"Bearer {get_token()}"
        return delete(url)
    else:
        print(json)
        exit()


def delete(url, data):
    res = requests.delete(url, headers=headers, json=data)
    json = res.json()
    if json['code'] == 200:
        return json['data']
    # 如果token过期则重新获取token
    elif json['code'] == 401:
        headers['Authorization'] = f"Bearer {get_token()}"
        return delete(url)
    else:
        print(json)
        exit()


# 获取全部环境变量
def get_envs():
    url = f'{api_url}/envs'
    res = get(url)
    return res.json()['data']


# envs
envs = get_envs()


# 获取单个环境变量
def get_env(name):
    url = f'{api_url}/envs?searchValue={name}'
    res = get(url)
    data = res.json()['data']
    if len(data) == 0:
        return None
    else:
        return data[0]


# 更新单个环境变量
def update_env(name, value):
    url = f'{api_url}/envs'
    data = {
        "id": get_env(name)['id'],
        "name": name,
        "value": value
    }
    res = put(url, data)
    return res.json()


# 添加环境变量
def add_env(name, value):
    url = f'{api_url}/envs'
    data = [
        {
            "name": name,
            "value": value
        }
    ]
    res = post(url, data)
    return res.json()


# 添加环境变量
def add_env(name, value, remarks):
    url = f'{api_url}/envs'
    data = [
        {
            "name": name,
            "value": value,
            "remarks": remarks
        }
    ]
    res = post(url, data)
    return res.json()


# 删除环境变量
def delete_env(name):
    url = f'{api_url}/envs'
    data = [
        get_env(name)['id']
    ]
    res = delete(url, data)
    return res.json()
