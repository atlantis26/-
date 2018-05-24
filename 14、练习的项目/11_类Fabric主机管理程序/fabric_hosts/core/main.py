# coding:utf-8
from core.host_handler import HostHandler
from core.host_group_handler import HostGroupHandler
import os


class _FabricHost(object):
    @staticmethod
    def console():
        while True:
            info = u"""你可以选择如下操作：
                        1.新增主机信息                    2.删除主机信息
                        3.修改主机信息                    4.查询主机详细信息
                        5.退出视图
            """
            print(info)
            action = input(u"请输入操作编号：").strip()
            actions = {"1": _FabricHost.create,
                       "2": _FabricHost.delete,
                       "3": _FabricHost.modify,
                       "4": _FabricHost.detail}
            if action in actions:
                actions[action]()
            elif action == "5":
                print("退出主机信息管理视图，返回主页面")
                break
            else:
                print(u"输入的操作编号不存在，请核对后再试")
            print("----------------------------------------------------")

    @staticmethod
    def create():
        ip = input(u"请输入主机的ip地址：").strip()
        port = input(u"请输入主机的通信端口：").strip()
        username = input(u"请输入主机的登录用户：").strip()
        password = input(u"请输入主机的登录密码：").strip()
        rsp = HostHandler.create(ip, port, username, password)
        print(rsp.msg)

    @staticmethod
    def delete():
        host_id = input(u"请输入主机的id编号：").strip()
        rsp = HostHandler.delete(host_id)
        print(rsp.msg)

    @staticmethod
    def modify():
        host_id = input(u"请输入主机的id编号：").strip()
        ip = input(u"请输入主机的ip地址：").strip()
        port = input(u"请输入主机的通信端口：").strip()
        username = input(u"请输入主机的登录用户：").strip()
        password = input(u"请输入主机的登录密码：").strip()
        rsp = HostHandler.modify(host_id, ip, port, username, password)
        print(rsp.msg)

    @staticmethod
    def detail():
        host_id = input(u"请输入主机的编号id：").strip()
        rsp = HostHandler.detail(host_id)
        print(rsp.msg)

    @staticmethod
    def list():
        rsp = HostHandler.list()
        if rsp.code == 200:
            host_list = rsp.data
            if not host_list:
                print(u"系统中还未录入任何主机信息")
            else:
                print(u"主机列表: ")
                for host in host_list:
                    print("主机编号：{0}       主机ip：{1}        主机端口号：{2}"
                          .format(host["host_id"], host["ip"], host["port"]))
        else:
            print(rsp.msg)

    @staticmethod
    def execute():
        host_id = input(u"请输入远程目标主机的id：").strip()
        commands = input(u"请输入需要执行的命令（可执行多个命令，命令以逗号连接）：").strip()
        rsp = HostHandler.detail(host_id)
        if rsp.code == 200:
            host = rsp.data
            client = HostHandler.create_session(host["ip"], host["port"], host["username"], host["password"])
            rsp = client.execute(commands)
            client.close()
            print(rsp.msg)
            if rsp.code == 200:
                print(rsp.data)
        else:
            print(u"主机id编号{0}不存在，请核对后再试".format(host_id))

    @staticmethod
    def put():
        host_id = input(u"请输入远程目标主机的id：").strip()
        local_path = input(u"请输入本地上传文件的路径：").strip()
        remote_dir = input(u"请输入远程主机存放文件的目录路径：").strip()
        file_name = os.path.split(local_path)[-1]
        sep = "/" if "/" in remote_dir else "\\"
        remote_path = sep.join([remote_dir, file_name])
        rsp = HostHandler.detail(host_id)
        if rsp.code == 200:
            host = rsp.data
            client = HostHandler.create_sftp_session(host["ip"], host["port"], host["username"], host["password"])
            rsp = client.put(local_path, remote_path)
            client.close()
            print(rsp.msg)
        else:
            print(u"主机id编号{0}不存在，请核对后再试".format(host_id))

    @staticmethod
    def get():
        host_id = input(u"请输入远程目标主机的id：").strip()
        remote_path = input(u"请输入远程主机上文件的路径：").strip()
        local_dir = input(u"请输入本地存放文件的目录路径：").strip()
        file_name = os.path.split(remote_path)[-1]
        local_path = os.path.join(local_dir, file_name)
        rsp = HostHandler.detail(host_id)
        if rsp.code == 200:
            host = rsp.data
            client = HostHandler.create_sftp_session(host["ip"], host["port"], host["username"], host["password"])
            rsp = client.get(remote_path, local_path)
            client.close()
            print(rsp.msg)
        else:
            print(u"主机id编号{0}不存在，请核对后再试".format(host_id))


class _FabricHostGroup(object):
    @staticmethod
    def console():
        while True:
            info = u"""你可以选择如下操作：
                        1.新增主机组信息                    2.删除主机组信息
                        3.修改主机组信息                    4.查询主机组详细信息
                        5.退出视图
            """
            print(info)
            action = input(u"请输入操作编号：").strip()
            actions = {"1": _FabricHostGroup.create,
                       "2": _FabricHostGroup.delete,
                       "3": _FabricHostGroup.modify,
                       "4": _FabricHostGroup.detail}
            if action in actions:
                actions[action]()
            elif action == "5":
                print("退出主机组信息管理视图，返回主页面")
                break
            else:
                print(u"输入的操作编号不存在，请核对后再试")
            print("----------------------------------------------------")

    @staticmethod
    def create():
        group_name = input(u"请输入新主机组的名称：").strip()
        group_ids = input(u"请输入添加为成员的主机的编号id（多个主机id以逗号连接）：").strip()
        rsp = HostGroupHandler.create(group_name, group_ids)
        print(rsp.msg)

    @staticmethod
    def delete():
        group_id = input(u"请输入主机组的编号id：").strip()
        rsp = HostGroupHandler.delete(group_id)
        print(rsp.msg)

    @staticmethod
    def modify():
        group_id = input(u"请输入主机组的编号id：").strip()
        group_name = input(u"请输入主机组的名称：").strip()
        group_ids = input(u"请输入成员主机的编号id（多个主机id以逗号连接）：").strip()
        rsp = HostGroupHandler.modify(group_id, group_name, group_ids)
        print(rsp.msg)

    @staticmethod
    def detail():
        group_id = input(u"请输入主机组的编号id：").strip()
        rsp = HostGroupHandler.detail(group_id)
        print(rsp.msg)

    @staticmethod
    def list():
        rsp = HostGroupHandler.list()
        if rsp.code == 200:
            host_group_list = rsp.data
            if not host_group_list:
                print(u"系统中还未录入任何主机组信息")
            else:
                print(u"主机组列表: ")
                for group in host_group_list:
                    print("编号：{0}     名称：{1}   成员列表：{2}"
                          .format(group["group_id"], group["group_name"], group["host_id_list"]))
        else:
            print(rsp.msg)

    @staticmethod
    def execute():
        group_id = input(u"请输入目标主机组的编号id：").strip()
        commands = input(u"请输入需要执行的命令（可执行多个命令，命令以逗号连接）：").strip()
        rsp = HostGroupHandler.detail(group_id)
        if rsp.code == 200:
            result = HostGroupHandler.execute_cmd(group_id, commands)
            print(result)
        else:
            print(u"主机组id编号{0}不存在，请核对后再试".format(group_id))

    @staticmethod
    def get():
        group_id = input(u"请输入目标主机组的编号id：").strip()
        remote_path = input(u"请输入远程主机上下载的文件的路径：").strip()
        local_dir = input(u"请输入本地存放文件的目录路径：").strip()
        rsp = HostGroupHandler.detail(group_id)
        if rsp.code == 200:
            result = HostGroupHandler.get(group_id, remote_path, local_dir)
            print(result)
        else:
            print(u"主机组id编号{0}不存在，请核对后再试".format(group_id))

    @staticmethod
    def put():
        group_id = input(u"请输入目标主机组的编号id：").strip()
        local_path = input(u"请输入本地上传文件的路径：").strip()
        remote_dir = input(u"请输入远程主机存放文件的目录路径：").strip()
        file_name = os.path.split(local_path)[-1]
        sep = "/" if "/" in remote_dir else "\\"
        remote_path = sep.join([remote_dir, file_name])
        rsp = HostGroupHandler.detail(group_id)
        if rsp.code == 200:
            result = HostGroupHandler.put(group_id, local_path, remote_path)
            print(result)
        else:
            print(u"主机组id编号{0}不存在，请核对后再试".format(group_id))


class Fabric(object):
    @staticmethod
    def execute():
        key = input(u"请输入操作对象的类型编号（1.主机；2：主机组）： ").strip()
        if key == "1":
            _FabricHost.execute()
        elif key == "2":
            _FabricHostGroup.execute()
        else:
            print(u"输入的选项编号不存在，请核对再试")

    @staticmethod
    def get():
        key = input(u"请输入操作对象的类型编号（1.主机；2：主机组）： ").strip()
        if key == "1":
            _FabricHost.get()
        elif key == "2":
            _FabricHostGroup.get()
        else:
            print(u"输入的选项编号不存在，请核对再试")

    @staticmethod
    def put():
        key = input(u"请输入操作对象的类型编号（1.主机；2：主机组）： ").strip()
        if key == "1":
            _FabricHost.put()
        elif key == "2":
            _FabricHostGroup.put()
        else:
            print(u"输入的选项编号不存在，请核对再试")

    @staticmethod
    def console():
        while True:
            info = u"""------------------欢迎使用Fabric运维管理系统-----------------
            你可以选择如下操作：
                1.显示主机列表                           2.显示主机组列表
                2.进入主机信息管理视图                   4.进入主机组信息管理视图
                5.执行命令                               6.上传文件
                7.下载文件                               8.退出系统
            """
            print(info)
            print("----------------------------------------------------")
            action = input(u"请输入操作编号：").strip()
            actions = {"1": _FabricHost.list,
                       "2": _FabricHostGroup.list,
                       "3": _FabricHost.console,
                       "4": _FabricHostGroup.console,
                       "5": Fabric.execute,
                       "6": Fabric.put,
                       "7": Fabric.get}
            if action == "8":
                print(u"您退出了系统，欢迎再次使用")
                break
            elif action in actions:
                actions[action]()
            else:
                print(u"输入的操作编号不存在，请核对后再试")
