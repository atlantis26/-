# coding:utf-8
from core.views.student_view import StudentView
from core.views.teacher_view import TeacherView
from core.views.manager_view import MangerView, Manager
from conf.settings import RP, USERNAME, PASSWORD
from core.users import init_manager, create_user
from core.db_handler import save_resources_pool

def register_user():
    """创建新学员用户账号"""
    try:
        name = input(u"请输入您的真实姓名：")
        username = input(u"请输入系统登录用户名：")
        password1 = input(u"请输入设置密码：")
        password2 = input(u"请再次输入设置密码：")
        create_user(name, username, password1, password2, u"学员")
        msg = u"创建用户{0}成功".format(username)
    except Exception as e:
        msg = u"创建用户失败，原因：{0}".format(str(e))

    print(msg)


def user_views():
    try:
        views = {"1": StudentView,
                 "2": TeacherView,
                 "3": MangerView}
        role_id = input(u"请输入用户身份类型编号（1.学员；2.讲师；3.管理员）： ").strip()
        if role_id not in views:
            raise Exception(u"输入身份类型{0}不存在，请核对后再试".format(role_id))
        name = input(u"请输入账号：").strip()
        password = input(u"请输入密码：").strip()
        views[role_id](name, password, role_id)
    except Exception as e:
        print(str(e))


def system_init_resources():
    """如果系统未有教学资源时，初始化创建教学资源"""
    init_manager(USERNAME, PASSWORD)
    if not RP.schools:
        beijing = Manager.create_school("beijing")
        linux = Manager.create_course(beijing.name, "linux", 365, 5000)
        python = Manager.create_course(beijing.name, "python", 365, 6000)
        class1 = Manager.create_class(beijing.name, u"1班", linux.name)
        class2 = Manager.create_class(beijing.name, u"2班", python.name)

        shanghai = Manager.create_school("shanghai")
        go = Manager.create_course(shanghai.name, "go", 365, 6000)
        class3 = Manager.create_class(shanghai.name, u"1班", go.name)

        alex = Manager.create_teacher("alex", "alex123", "123456", "123456")
        jack = Manager.create_teacher("jack", "jack123", "123456", "123456")
        lucy = Manager.create_teacher("lucy", "lucy123", "123456", "123456")

        RP.teachers[alex.id].add_class(class1.id)
        RP.teachers[jack.id].add_class(class2.id)
        RP.teachers[lucy.id].add_class(class3.id)
        save_resources_pool()


def console():
    while True:
        system_init_resources()
        msg = u"""------------欢迎访问无忧选课系统---------------
            您可以选择如下操作：
                <\033[36;1m1\033[0m>.学员用户注册                     <\033[36;1m2\033[0m>.用户登录
        """
        print(msg)
        actions = {"1": register_user,
                   "2": user_views}
        num = input(u"请输入您选择的操作编号：").strip()
        if num not in actions:
            print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))
            continue
        actions[num]()


if __name__ == "__main__":
    console()
