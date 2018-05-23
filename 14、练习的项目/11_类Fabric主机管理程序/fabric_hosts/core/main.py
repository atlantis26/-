# coding:utf-8
from core.host_handler import HostHandler
from core.host_group_handler import HostGroupHandler
import os


class _FabricHost(object):
    @staticmethod
    def console():
        info = u"""你可以选择如下操作：
                    1.新增                    2.删除
                    3.修改                    4.查询
        """
        print(info)
        action = input(u"请输入操作编号：").strip()
        actions = {"1": _FabricHost.create,
                   "2": _FabricHost.delete,
                   "3": _FabricHost.modify,
                   "4": _FabricHost.show}
        if action in actions:
            actions[action]()
        else:
            print(u"输入的操作编号不存在，请核对后再试")

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
    def show():
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
        cmd = input(u"请输入需要执行的命令：").strip()
        rsp = HostHandler.detail(host_id)
        if rsp.code == 200:
            host = rsp.data
            client = HostHandler.create_session(host["ip"], host["port"], host["username"], host["password"])
            rsp = client.execute(cmd)
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
        remote_path = os.path.join(remote_dir, file_name)
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
        info = u"""你可以选择如下操作：
                    1.新增                    2.删除
                    3.修改                    4.查询
        """
        print(info)
        action = input(u"请输入操作编号：").strip()
        actions = {"1": _FabricHostGroup.create,
                   "2": _FabricHostGroup.delete,
                   "3": _FabricHostGroup.modify,
                   "4": _FabricHostGroup.show}
        if action in actions:
            actions[action]()
        else:
            print(u"输入的操作编号不存在，请核对后再试")

    @staticmethod
    def create():
        pass

    @staticmethod
    def delete():
        pass

    @staticmethod
    def modify():
        pass

    @staticmethod
    def show():
        host_group_list = HostGroupHandler.list()
        if not host_group_list:
            print(u"系统中还未录入任何主机组信息")
        else:
            print(u"主机组列表: ")
            for group in host_group_list:
                print("{0}".format(group.id))

    @staticmethod
    def execute():
        pass

    @staticmethod
    def get():
        pass

    @staticmethod
    def put():
        pass


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
            info = u"""---------欢迎使用Fabric运维管理系统---------
            你可以选择如下操作：
                1.主机视图                   2.主机组视图
                3.退出系统
            """
            print(info)
            action = input(u"请输入操作编号：").strip()
            actions = {"1": _FabricHost.console,
                       "2": _FabricHostGroup.console}
            if action == "3":
                break
            elif action in actions:
                actions[action]()
            else:
                print(u"输入的操作编号不存在，请核对后再试")
