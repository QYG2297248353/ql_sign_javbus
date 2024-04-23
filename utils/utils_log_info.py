# -*- coding: utf-8 -*-

def task_start():
    """
    打印任务开始信息
    1. 调用者信息
    2. 任务开始时间
    :return:
    """
    import logging
    import inspect
    import datetime

    caller = inspect.stack()[1]
    logging.info('Caller: %s.%s', caller.filename, caller.function)
    logging.info('Start at: %s', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


def task_end():
    """
    打印任务结束信息
    1. 任务结束时间
    :return:
    """
    import logging
    import datetime

    logging.info('End at: %s', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    logging.info('Done!')


def random_sign_time():
    """
    随机签到时间 分钟/秒钟
    :return: 延迟签到时间 15分钟之内
    """
    import logging
    import random
    import time

    minute = random.randint(0, 6)
    second = random.randint(0, 59)

    logging.info('Random sign time: %s minute %s second', minute, second)
    time.sleep(minute * 60 + second)
    logging.info('Start sign')
