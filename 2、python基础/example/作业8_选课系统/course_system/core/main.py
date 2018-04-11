# coding:utf-8
from core.orm import School, Course
from core.view import StudentView, TeacherView, MangerView


def init_system():
    beijing = School("beijing")
    beijing.create_course("linux", 365, 5000)
    beijing.create_course("python", 365, 6000)
    alex_rsp = beijing.create_teacher("alex", "123456")
    jack_rsp = beijing.create_teacher("jack", "123456")
    beijing.create_class(u"1班", "linux", alex_rsp.data.emp_id)
    beijing.create_class(u"2班", "python", jack_rsp.data.emp_id)

    shanghai = School("beijing")
    shanghai.create_course("go", 365, 6000)
    mike_rsp = beijing.create_teacher("mike", "123456")
    shanghai.create_class("1班", "go", mike_rsp.data.emp_id)


def console_help():
    msg = u"""-------------------------------------------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.用户注册                      <\033[36;1m2\033[0m>.用户登录
            <\033[36;1m3\033[0m>.用户登出                     <\033[36;1m7\033[0m>.查询用户信息                  <\033[36;1m8\033[0m>.重置密码
    """
    print(msg)


def system(view, name, password):
    pass


def console():
    msg = """*****欢迎访问无忧选课系统*****"""
    init_system()
    console_help()
    views = {"1": StudentView,
             "2": TeacherView,
             "3": MangerView}
    role_id = input(u"请输入身份类型编号：").strip()
    name = input(u"请输入姓名：").strip()
    password = input(u"请输入密码：").strip()
    system(views[role_id], name, password)
