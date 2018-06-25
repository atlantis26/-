# coding:utf-8
from conf.settings import MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD, MQ_QUEUE_DICT
from core.rpc_client import RpcClient
from core.db_handler import load_task


class HostManager(object):
    def __init__(self):
        pass

    def show_host(self):
        print("支持的主机列表：")
        for host in MQ_QUEUE_DICT:
            print(host)

    def console(self):
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
                        queue_name = MQ_QUEUE_DICT[host]
                        client = RpcClient(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD, queue_name)
                        task_id = client.run_cmd(cmd)
                        print("task_id: {0}".format(task_id))
            elif args[0] == "check_task":
                task_id = args[1]
                queue_name = load_task(task_id)["queue"]
                client = RpcClient(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD, queue_name)
                data = client.check_task(task_id)
                print(data)
            else:
                print("{0}命令不支持".format(args[0]))
