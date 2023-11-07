# Base Url
import os
import time

import requests as requests
from bs4 import BeautifulSoup

from qlApi import export_envs

base_url = 'https://www.javbus.com/forum/'

# 通过环境变量获取Cookie 用于登录
saltkey = os.environ.get('4fJN_2132_saltkey')
auth = os.environ.get('4fJN_2132_auth')
username = os.environ.get('javbus_username')

# 请求页面
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
    'Cookie': f'saltkey={saltkey};auth={auth};'
}

# 签到次数
sign_err_count = 0


# 签到
def sign(sign_count=0):
    url = base_url
    response = requests.get(url, headers=headers)
    #
    if response.status_code == 200:
        print('解析签到结果')
        soup = BeautifulSoup(response.text, 'html.parser')
        # 解析页面title是否存在包含 “登錄”
        title = soup.find('title').text
        if '登錄' in title:
            print('Tip：账户未登录，请设定环境变量！')
            return
        # 在 a 标签中查找包含 “username” 的标签
        a = soup.find('a', text=username)
        # 如果存在则表示签到成功
        if a:
            print('Tip：今日已签到！')
        # 如果不存在则表示未签到
        else:
            print('Tip：签到失败')
    else:
        print('Tip：签到失败，尝试重新签到')
        # 倒计时 5 秒 并打印日志
        for i in range(5, 0, -1):
            print(f'重新签到倒计时：{i} 秒')
            time.sleep(1)
        # 重新签到 10 次 如果失败则退出
        if sign_count < 10:
            sign_count += 1
            sign(sign_count)
        else:
            print('Tip：签到失败，退出程序！')
            exit()


# 程序入口
if __name__ == '__main__':
    # 获取青龙面板环境变量
    envs = export_envs()
    print('导出变量：' + envs)

    sign(sign_err_count)
