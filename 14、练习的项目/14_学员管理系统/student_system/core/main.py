#  coding:utf-8
from core.views.student_view import StudentView
from core.views.teacher_view import TeacherView
from core.views.manager_view import MangerView
from db.db_handler import query_user_by_account



def user_views():
    try:
        user_info = login()

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


def console():
    while True:
        msg = u"""------------欢迎访问学员管理系统---------------
            您可以选择如下操作：
                <\033[36;1m1\033[0m>.用户登录                     <\033[36;1m2\033[0m>.退出系统
        """
        print(msg)
        num = input(u"请输入您选择的操作编号：").strip()
        if num == "1":
            user_views()
        elif num == "2":
            exit()
        else:
            print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))


if __name__ == "__main__":
    console()

