# coding:utf-8
from conf.settings import MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD, MQ_QUEUE_DICT
from core.rpc_client import RpcClient
from core.orm import SomeError
import pika
import re


class HostManager(object):
    def __init__(self):
        self.client = RpcClient(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD)

    def show(self):
        print("支持的主机列表：")
        for host in MQ_QUEUE_DICT:
            print(host)

    def console(self):
        try:
            while True:
                cmd_args = input("请输入指令：>  ").strip()
                if cmd_args == "show":
                    self.show()
                elif cmd_args.startswith("run"):
                    p1 = r'run\s+"*\'*(?P<cmd>.*?)"*\'*\s+--hosts\s+(?P<hosts>.*?)$'
                    result = re.search(p1, cmd_args)
                    if not result:
                        print("run命令语法有误，请核对后再试")
                    else:
                        cmd = result.group("cmd")
                        hosts = result.group("hosts").split(",")
                        not_exist_host = [host for host in hosts if host not in MQ_QUEUE_DICT]
                        if not_exist_host:
                            print("参数有误，指定的主机{0}不存在".format(not_exist_host))
                        else:
                            for host in hosts:
                                task_id = self.client.request(cmd, host)
                                print("task_id：{0}".format(task_id))
                elif cmd_args.startswith("check_task"):
                    p2 = r'check_task\s+(?P<task_id>.+)$'
                    result = re.search(p2, cmd_args)
                    if not result:
                        print("check_task命令语法有误，请核对后再试")
                    else:
                        task_id = result.group("task_id")
                        data = self.client.response(task_id)
                        print(data)
                else:
                    print("不支持'{0}'命令".format(cmd_args))
        except pika.exceptions.ConnectionClosed:
                print("客户端连接超时，连接已断开，请重新建立连接")
