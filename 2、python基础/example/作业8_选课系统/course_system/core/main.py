# coding:utf-8
from core.orm import School, Course
from core.view import StudentView, TeacherView, MangerView


def init_system():
    beijing = School()
    shanghai = School()

    linux = Course(cycle=365, price=5000)
    python = Course(cycle=365, price=6000)
    go = Course(cycle=365, price=6000)

    beijing.classes.extend([linux, python])
    shanghai.classes.append(go)


def console_help():
    msg = """*****欢迎访问无忧选课系统*****
            请先选择您的身份类型：
            1.学员
            2.讲师
            3.管理员
    """
    print(msg)


def system(view, name, password):
    pass


def console():
    init_system()
    console_help()
    views = {"1": StudentView,
             "2": TeacherView,
             "3": MangerView}
    role_id = input(u"请输入身份类型编号：").strip()
    name = input(u"请输入姓名：").strip()
    password = input(u"请输入密码：").strip()
    system(views[role_id], name, password)
