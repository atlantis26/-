#  coding:utf-8
from core.views.student_view import StudentView
from core.views.teacher_view import TeacherView
from core.views.manager_view import MangerView
from core.handler import login


def views(username, password, role_id):
    items = {"1": MangerView, "2": TeacherView, "3": StudentView}
    items[role_id](username, password, role_id)


def console():
    print(u"欢迎访问学员管理系统，请先登录。。。")
    while True:
        username = input(u"请输入登录账号：").strip()
        password = input(u"请输入登录密码：").strip()
        rsp = login(username, password)
        if rsp.code == 200:
            role_id = rsp.data["role_id"]
            views(username, password, role_id)
        else:
            print(rsp.msg)


if __name__ == "__main__":
    console()

