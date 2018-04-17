# coding:utf-8
from core.views.student_view import StudentView
from core.views.teacher_view import TeacherView
from core.views.manager_view import MangerView
from core.users import create_user


def register_user():
    """创建新账户"""
    username = input(u"请输入新建用户名：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = create_user(username, password1, password2)

    print(rsp.msg)


def user_views():
    views = {"1": StudentView,
             "2": TeacherView,
             "3": MangerView}
    num = input(u"请输入用户身份类型编号（1.学员；2.讲师；3.管理员）： ").strip()
    if num not in views:
        print(u"输入身份类型{0}不存在，请核对后再试".format(num))
        return
    name = input(u"请输入账号：").strip()
    password = input(u"请输入密码：").strip()
    views[num](name, password)


def console_help():
    msg = u"""------------欢迎访问无忧选课系统---------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.用户注册                     <\033[36;1m2\033[0m>.用户登录
    """
    print(msg)


def console():
    while True:
        console_help()
        actions = {"1": register_user,
                   "2": user_views}
        num = input(u"请输入您选择的操作编号：").strip()
        if num not in actions:
            print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))
            return
        actions[num]()


if __name__ == "__main__":
    console()
