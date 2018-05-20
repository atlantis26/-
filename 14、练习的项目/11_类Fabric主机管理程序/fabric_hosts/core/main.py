# coding:utf-8
from core.manager import _Host, _HostGroup
from core.db_handler import create_host, query_host, list_hosts
from core.db_handler import create_host_group, query_host_group, list_host_groups
from core.orm import SomeError


class Fabric(object):
    @staticmethod
    def show_hosts():
        host_list = list_hosts()
        if not host_list:
            print(u"系统中还未录入任何主机信息")
        else:
            print(u"主机列表: ")
            for host in host_list:
                print("{0}       {1}        {2}".format(host.host_id, host.username, host.ip))

    @staticmethod
    def show_host_groups():
        host_group_list = list_host_groups()
        if not host_group_list:
            print(u"系统中还未录入任何主机组信息")
        else:
            print(u"主机组列表: ")
            for group in host_group_list:
                print("{0}       {1}        {2}".format(group.id))

    @staticmethod
    def show():
        key = input(u"请输入你的选项编号（1.主机；2：主机组）： ").strip()
        if key in 

    @staticmethod
    def host_execute():
        host_id = input(u"请输入远程目标主机的id：")
        cmd = input(u"请输入需要执行的命令：")
        host = query_host(host_id)
        client = _Host.create_session(host.ip, host.port, host.username, host.password)
        rsp = client.execute(cmd)
        client.close()
        print(rsp.msg)

    @staticmethod
    def host_group_execute():
        host_id = input(u"请输入远程目标主机组的id：")
        cmd = input(u"请输入需要执行的命令：")
        rsp = _HostGroup.execute_cmd(host_id, cmd)
        print(rsp.msg)

    @staticmethod
    def host_put():
        host_id = input(u"请输入远程目标主机的id：")
        local_path = input(u"请输入本地上传文件的路径")
        remote_path = input(u"请输入远程主机存放文件的路径")
        host = query_host(host_id)
        client = _Host.create_sftp_session(host.ip, host.port, host.username, host.password)
        rsp = client.put(local_path, remote_path)
        client.close()
        print(rsp.msg)

    @staticmethod
    def host_group_put():
        host_id = input(u"请输入目标主机组的id：")
        local_path = input(u"请输入本地上传文件的路径")
        remote_path = input(u"请输入远程主机存放文件的路径")
        rsp = _HostGroup.put(host_id, local_path, remote_path)
        print(rsp.msg)

    @staticmethod
    def host_get():
        host_id = input(u"请输入远程目标主机的id：")
        remote_path = input(u"请输入远程主机上文件的路径")
        local_path = input(u"请输入本地存放文件的路径")
        host = query_host(host_id)
        client = _Host.create_sftp_session(host.ip, host.port, host.username, host.password)
        rsp = client.get(remote_path, local_path)
        client.close()
        print(rsp.msg)

    @staticmethod
    def host_group_get():
        group_id = input(u"请输入目标主机组的id：")
        remote_path = input(u"请输入远程主机上文件的路径")
        local_path = input(u"请输入本地存放文件的路径")
        rsp = _HostGroup.put(group_id, remote_path, local_path)
        print(rsp.msg)

    @staticmethod
    def detail():
        host_id = input(u"请输入目标主机的id：")
        rsp = _Host.detail(host_id)
        print(rsp.msg)

    @staticmethod
    def host_create():
        host_id = input(u"请输入主机的编号：")
        ip = input(u"请输入主机的ip地址：")
        port = input(u"请输入主机的通信端口：")
        username = input(u"请输入主机的登录用户：")
        password = input(u"请输入主机的登录密码：")
        rsp = _Host.create(host_id, ip, port, username, password)
        print(rsp.msg)

    @staticmethod
    def host_group_create():
        group_id = input(u"请输入主机组的编号：")
        group_id = input(u"请输入主机的通信端口：")
        rsp = _HostGroup.create(group_id, group_id)
        print(rsp.msg)

    @staticmethod
    def console():
        while True:
            info = u"""---------欢迎使用Fabric运维管理系统---------
            你可以选择如下操作：
                1.新增主机/主机组信息             2.查询主机/主机组列表
                3.执行命令                       4.上传文件
                5.下载文件                       6.退出系统
            """
            print(info)
            action = input(u"请输入操作编号：").strip()
            actions = {"1": Fabric.execute,
                       "2": Fabric.put,
                       "3": Fabric.get,
                       "4": Fabric.create,
                       "5": Fabric.detail}
            if action == "8":
                break
            elif action in actions:
                actions[action]()
            else:
                print(u"输入的操作编号不存在，请核对后再试")
