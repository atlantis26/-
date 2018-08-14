# coding:utf-8
from core.handler import Handler


class UserView(object):
    def __init__(self, user_id):
        self.user_id = user_id
        self.console()

    def console(self):
        while True:
            msg = u"""
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.通过主机列表选择主机         <\033[36;1m2\033[0m>.通过主机组选择主机
                    <\033[36;1m3\033[0m>.退出系统
            """
            print(msg)
            actions = {"1": Handler.select_host_by_list,
                       "2": Handler.select_host_by_group}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num in actions:
                rsp = actions[num](self.user_id)
                print(rsp.msg)
                if rsp.code == 200:
                    host_id = rsp.data
                    Handler.start_host_session(self.user_id, host_id)
            elif num == "3":
                print("您已退出登录，欢迎再次访问本系统")
                break
            else:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
