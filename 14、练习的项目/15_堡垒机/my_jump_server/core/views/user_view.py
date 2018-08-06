# coding:utf-8
from core.handler import BaseHandler


class UserView(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.console()

    def console(self):
        while True:
            msg = u"""
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.展示主机及主机组信息         <\033[36;1m2\033[0m>.登录目标主机
                    <\033[36;1m3\033[0m>.退出系统
            """
            print(msg)
            actions = {"1": self.show_hosts,
                       "2": self.login_host}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num in actions:
                actions[num]()
            elif num == "3":
                print("您已退出登录，欢迎再次访问本系统")
                break
            else:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue

    def show_hosts(self):
        """显示用户具有操作权限的主机以及主机组"""
        pass

    def login_host(self):
        """用户登录目标主机进行操作"""
        host_id = input(u"请输入目标主机的id：").strip()
        rsp = BaseHandler.start_session(self.user_id, host_id)
        print(rsp.msg)

