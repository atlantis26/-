# coding:utf-8
from conf.settings import MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD, MQ_QUEUE_DICT
from core.rpc_client import RpcClient
import pika


class HostManager(object):
    def __init__(self):
        self.client = RpcClient(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD)

    def show_host(self):
        print("支持的主机列表：")
        for host in MQ_QUEUE_DICT:
            print(host)

    def console(self):
        try:
            while True:
                cmds = input("请输入指令：>  ")
                args = cmds.split(" ")
                if args[0] == "run":
                    cmd = args[1]
                    hosts = args[2].split(",")
                    not_exist_host = [host for host in hosts if host not in MQ_QUEUE_DICT]
                    if not_exist_host:
                        print("参数有误，指定的主机{0}不存在".format(not_exist_host))
                    else:
                        for host in hosts:
                            task_id = self.client.request(cmd, host)
                            print("task_id：{0}".format(task_id))
                elif args[0] == "check_task":
                    task_id = args[1]
                    data = self.client.response(task_id)
                    print(data)
                else:
                    print("{0}命令不支持".format(args[0]))
        except pika.exceptions.ConnectionClosed:
                print("客户端连接超时，连接已断开，请重新建立连接")

