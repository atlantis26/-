# coding:utf-8
from core.orm import School
from core.views import StudentView, TeacherView, MangerView


def init_system():
    beijing = School("beijing")
    beijing.create_course("linux", 365, 5000)
    beijing.create_course("python", 365, 6000)
    rsp1 = beijing.create_teacher("alex", "123456")
    rsp2 = beijing.create_teacher("jack", "123456")
    beijing.create_class(u"1班", "linux", rsp1.data.emp_id)
    beijing.create_class(u"2班", "python", rsp2.data.emp_id)

    shanghai = School("beijing")
    shanghai.create_course("go", 365, 6000)
    rsp3 = beijing.create_teacher("mike", "123456")
    shanghai.create_class("1班", "go", rsp3.data.emp_id)


def console_help():
    msg = u"""------------欢迎访问无忧选课系统---------------
        您可以选择如下操作：
            <\033[36;1m1\033[0m>.用户注册                      
            <\033[36;1m2\033[0m>.用户登录
    """
    print(msg)


def system(view, name, password):
    pass


def console():
    init_system()
    while True:
        console_help()
        views = {"1": StudentView,
                 "2": TeacherView,
                 "3": MangerView}
        role_id = input(u"请输入用户身份类型编号（1.学员；2.讲师；3.管理员）： ").strip()
        if role_id not in views:
            msg = u"输入身份类型{0}不存在，请核对后再试".format(role_id)
            print(msg)
        name = input(u"请输入姓名：").strip()
        password = input(u"请输入密码：").strip()
        system(views[role_id], name, password)


if __name__ == "__main__":
    console()
