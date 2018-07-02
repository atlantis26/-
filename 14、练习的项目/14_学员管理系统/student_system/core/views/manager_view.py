# coding:utf-8
from core.utils import SomeError, ResponseData
from settings import Is_Authenticated
import logging

logger = logging.getLogger("system.manager_view")


class MangerView(object):
    """管理员视图"""
    def __init__(self, username, password, role_id):
        self.username = username
        self.password = password
        self.role_id = role_id

    def console(self):
        """ 管理员视图主页，可创建、修改、删除、查询用户"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.创建用户                   <\033[36;1m2\033[0m>.修改用户
                    <\033[36;1m3\033[0m>.删除用户                   <\033[36;1m4\033[0m>.查询用户
                    <\033[36;1m4\033[0m>.查询所有用户信息           <\033[36;1m4\033[0m>.退出视图
            """
            print(msg)
            actions = {"1": self.create_user,
                       "2": self.modify_user,
                       "3": self.delete_user,
                       "4": self.detail_user,
                       "5": self.list_user,
                       "6": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            ret = actions[num]()
            print(ret.msg)

    def create_user(self):
        try:
            name = input(u"请输入用户姓名：").strip()
            account = input(u"请输入登录账号：").strip()
            password1 = input(u"请输入登录密码：").strip()
            password2 = input(u"请重复输入登录密码：").strip()
            qq = input(u"请输入用户qq账号：").strip()
            role = input(u"请输入编号设置用户角色（1：老师；2：学员；3：管理员）：").strip()
            rsp = create_user(name, account, password1, qq, role)
            code = 200

        except SomeError as e

        print(rsp.msg)


    def delete_user(self):
        pass


    def modify_user(self):
        pass


    def detail_user(self):
        pass


    def list_user(self):
        pass

    def logout(self):
        pass

class Manager(object):
    @staticmethod
    def create_user(name, account, password1, password2, qq, role):
        if