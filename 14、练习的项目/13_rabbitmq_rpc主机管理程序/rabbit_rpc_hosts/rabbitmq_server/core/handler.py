# coding:utf-8
from core.orm import ResponseData
import os
import logging

logger = logging.getLogger("rabbit_mq.task")


def run_cmd(task_id, commands):
    data = dict()
    cmd_list = commands.split(",")
    for cmd in cmd_list:
        data[cmd] = os.popen(cmd).read()
    msg = "任务(task_id={0})执行完成。".format(task_id)
    logger.debug(ResponseData(200, msg, data).__dict__)

    return ResponseData(200, msg, data)
