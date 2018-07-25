# coding:utf-8
from core.handler import Handler


class MangerView(object):
    def __init__(self, username):
        self.username = username
        self.console()

    def console(self):
        """ 学员视图主页"""
        print(u"欢迎管理员‘{0}’登录本学员管理系统...".format(self.username))
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.创建用户                   <\033[36;1m2\033[0m>.删除用户
                    <\033[36;1m3\033[0m>.修改用户                   <\033[36;1m4\033[0m>.查询用户详情
                    <\033[36;1m5\033[0m>.查询用户列表               <\033[36;1m6\033[0m>.注销登出
                    
            """
            print(msg)
            actions = {"1": self.create_user,
                       "2": self.delete_user,
                       "3": self.modify_user,
                       "4": self.detail_user,
                       "5": self.list_user}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num in actions:
                actions[num]()
            elif num == "6":
                print("您已注销登录，欢迎您再次访问本系统")
                break
            else:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue

    @staticmethod
    def create_user():
        name = input(u"请输入用户姓名：").strip()
        account = input(u"请输入登录账号：").strip()
        password1 = input(u"请输入登录密码：").strip()
        password2 = input(u"请重复输入登录密码：").strip()
        qq = input(u"请输入用户qq账号：").strip()
        role = input(u"请输入设置用户角色类型（student、teacher或者manager）：").strip()
        rsp = Handler.create_user(name, account, password1, password2, qq, role)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    @staticmethod
    def delete_user():
        user_id = input(u"请输入用户id：").strip()
        rsp = Handler.delete_user(user_id)
        print(rsp.msg)

    @staticmethod
    def modify_user():
        user_id = input(u"请输入用户id：").strip()
        name = input(u"请输入用户姓名：").strip()
        password = input(u"请输入登录密码：").strip()
        qq = input(u"请输入用户qq账号：").strip()
        role = input(u"请输入设置用户角色类型（student、teacher或者manager）：").strip()
        rsp = Handler.update_user(user_id, name, password, qq, role)
        print(rsp.msg)

    @staticmethod
    def detail_user():
        user_id = input(u"请输入用户id：").strip()
        rsp = Handler.query_user(user_id)
        if rsp.code == 200:
            print(rsp.data)
        print(rsp.msg)

    @staticmethod
    def list_user():
        rsp = Handler.list_user()
        if rsp.code == 200:
            for user in rsp.data:
                print(user)
        print(rsp.msg)

