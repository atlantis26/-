# coding:utf-8
from core.views.student_view import StudentView
from core.views.teacher_view import TeacherView
from core.views.manager_view import MangerView
from core.orm import School, ResponseData
from core.users import create_user
import logging

logger = logging.getLogger("atm.auth")


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

    beijing.create_teacher("alex", [u"1班"])
    beijing.create_teacher("jack", [u"2班"])
    shanghai.create_teacher("lucy", [u"1班"])

    code = 200
    msg = u"初始化完成学校等资源创建或重塑"
    logger.debug(ResponseData(code, msg, [beijing, shanghai]).__dict__)

    return [beijing, shanghai]


def register_user():
    """创建新账户"""
    username = input(u"请输入新建用户名：")
    password1 = input(u"请输入设置密码：")
    password2 = input(u"请再次输入设置密码：")
    rsp = create_user(username, password1, password2)
    logger.debug(rsp.__dict__)

    print(rsp.msg)


def user_views():
    school_resources = init_system()
    views = {"1": StudentView,
             "2": TeacherView,
             "3": MangerView}
    num = input(u"请输入用户身份类型编号（1.学员；2.讲师；3.管理员）： ").strip()
    if num not in views:
        print(u"输入身份类型{0}不存在，请核对后再试".format(num))
        return
    name = input(u"请输入账号：").strip()
    password = input(u"请输入密码：").strip()
    views[num](name, password, school_resources)


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
