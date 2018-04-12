# coding:utf-8
from core.orm import School
from core.views import StudentView, TeacherView, MangerView


def init_system():
    """初始化系统，新建学校等对象，如果对象已被创建保存，则通过pickle重构对象"""
    beijing = School("beijing")
    beijing.create_course("linux", 365, 5000)
    beijing.create_course("python", 365, 6000)
    beijing.create_class(u"1班", "linux")
    beijing.create_class(u"2班", "python")

    shanghai = School("beijing")
    shanghai.create_course("go", 365, 6000)
    shanghai.create_class(u"1班", "go")

    beijing.create_teacher("alex", "25", "man", [u"1班"])
    beijing.create_teacher("jack", "30", "man", [u"2班"])
    shanghai.create_teacher("lucy", "27", "woman", [u"1班"])

    return [beijing, shanghai]


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
    while True:
        init_system()
        console_help()
        views = {"1": StudentView,
                 "2": TeacherView,
                 "3": MangerView}
        num = input(u"请输入用户身份类型编号（1.学员；2.讲师；3.管理员）： ").strip()
        if num not in views:
            print(u"输入身份类型{0}不存在，请核对后再试".format(num))
        name = input(u"请输入账号：").strip()
        password = input(u"请输入密码：").strip()
        system(views[num](name, password))


if __name__ == "__main__":
    console()
