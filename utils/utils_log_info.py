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
