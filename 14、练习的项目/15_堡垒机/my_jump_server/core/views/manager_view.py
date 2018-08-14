# coding:utf-8
from core.handler import Handler


class ManagerView(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.console()

    def console(self):
        while True:
            msg = u"""
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.新增主机                     <\033[36;1m2\033[0m>.新增主机组
                    <\033[36;1m3\033[0m>.新增本地系统用户             <\033[36;1m4\033[0m>.新增远程登录账号
                    <\033[36;1m5\033[0m>.新增主机映射关系             <\033[36;1m6\033[0m>.通过主机列表选择主机
                    <\033[36;1m7\033[0m>.通过主机组选择主机           <\033[36;1m8\033[0m>.退出系统
            """
            print(msg)
            actions = {"1": self.create_hosts,
                       "2": self.create_groups,
                       "3": self.create_users,
                       "4": self.create_remoteusers,
                       "5": self.create_bindhosts,
                       "6": Handler.select_host_by_list,
                       "7": Handler.select_host_by_group}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num in actions:
                if num in ["6", "7"]:
                    rsp = actions[num](self.user_id)
                    print(rsp.msg)
                    if rsp.code == 200:
                        host_id = rsp.data
                        Handler.start_host_session(self.user_id, host_id)
                else:
                    actions[num](self.user_id)
            elif num == "8":
                print("您已退出登录，欢迎再次访问本系统")
                break
            else:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue

    @staticmethod
    def create_hosts():
        file_path = input(u"请输入配置文件的路径：").strip()
        rsp = Handler.create_hosts(file_path)
        print(rsp.msg)

    @staticmethod
    def create_groups():
        file_path = input(u"请输入配置文件的路径：").strip()
        rsp = Handler.create_groups(file_path)
        print(rsp.msg)

    @staticmethod
    def create_users():
        file_path = input(u"请输入配置文件的路径：").strip()
        rsp = Handler.create_users(file_path)
        print(rsp.msg)

    @staticmethod
    def create_remoteusers():
        file_path = input(u"请输入配置文件的路径：").strip()
        rsp = Handler.create_remoteusers(file_path)
        print(rsp.msg)

    @staticmethod
    def create_bindhosts():
        file_path = input(u"请输入配置文件的路径：").strip()
        rsp = Handler.create_bindhosts(file_path)
        print(rsp.msg)
