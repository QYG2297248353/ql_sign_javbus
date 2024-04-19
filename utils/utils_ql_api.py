# _*_ coding:utf-8 _*_
import logging

import requests

from utils import QL_HEADERS, get_authorization, OPEN_URL


def get(url):
    """
    Get请求
    """
    res = requests.get(url, headers=QL_HEADERS, timeout=60)
    if res.status_code != 200:
        logging.error(f"请求失败，状态码：{res.status_code}")
        exit(1)
    json = res.json()
    if json['code'] == 200:
        return json
    elif json['code'] == 401:
        get_authorization()
        return get(url)
    else:
        logging.error('请求失败: {}'.format(json))
        exit(1)


def post(url, data):
    """
    Post请求
    """
    res = requests.post(url, headers=QL_HEADERS, json=data, timeout=60)
    if res.status_code != 200:
        logging.error(f"请求失败，状态码：{res.status_code}")
        exit(1)
    json = res.json()
    if json['code'] == 200:
        return json
    elif json['code'] == 401:
        get_authorization()
        return post(url, data)
    else:
        logging.error('请求失败: {}'.format(json))
        exit(1)


def put(url, data):
    """
    Put请求
    """
    res = requests.put(url, headers=QL_HEADERS, json=data, timeout=60)
    if res.status_code != 200:
        logging.error(f"请求失败，状态码：{res.status_code}")
        exit(1)
    json = res.json()
    if json['code'] == 200:
        return json
    elif json['code'] == 401:
        get_authorization()
        return put(url, data)
    else:
        logging.error('请求失败: {}'.format(json))
        exit(1)


def delete(url):
    """
    Delete请求
    """
    res = requests.delete(url, headers=QL_HEADERS, timeout=60)
    if res.status_code != 200:
        logging.error(f"请求失败，状态码：{res.status_code}")
        exit(1)
    json = res.json()
    if json['code'] == 200:
        return json
    elif json['code'] == 401:
        get_authorization()
        return delete(url)
    else:
        logging.error('请求失败: {}'.format(json))
        exit(1)


def delete_data(url, data):
    """
    Delete请求
    """
    res = requests.delete(url, headers=QL_HEADERS, json=data, timeout=60     )
    if res.status_code != 200:
        logging.error(f"请求失败，状态码：{res.status_code}")
        exit(1)
    json = res.json()
    if json['code'] == 200:
        return json
    elif json['code'] == 401:
        get_authorization()
        return delete_data(url, data)
    else:
        logging.error('请求失败: {}'.format(json))
        exit(1)


def get_envs():
    """
    获取全部环境变量
    """
    url = f'{OPEN_URL}/envs'
    res = get(url)
    return res['data']


def get_env(name):
    """
    获取单个环境变量
    """
    url = f'{OPEN_URL}/envs?searchValue={name}'
    res = get(url)
    data = res['data']
    if len(data) == 0:
        return None
    else:
        return data[0]


def update_env(name, value):
    """
    更新单个环境变量
    """
    url = f'{OPEN_URL}/envs'
    data = {
        "id": get_env(name)['id'],
        "name": name,
        "value": value
    }
    res = put(url, data)
    return res


def add_env(name, value):
    """
    添加环境变量
    """
    url = f'{OPEN_URL}/envs'
    data = [
        {
            "name": name,
            "value": value
        }
    ]
    res = post(url, data)
    return res


def add_update_env(name, value):
    """
    添加或更新环境变量
    """
    if get_env(name):
        update_env(name, value)
    else:
        add_env(name, value)


def add_full_env(name, value, remarks):
    """
    添加环境变量
    """
    url = f'{OPEN_URL}/envs'
    data = [
        {
            "name": name,
            "value": value,
            "remarks": remarks
        }
    ]
    res = post(url, data)
    return res


def delete_env(name):
    """
    删除环境变量
    """
    url = f'{OPEN_URL}/envs'
    data = [
        get_env(name)['id']
    ]
    res = delete_data(url, data)
    return res
