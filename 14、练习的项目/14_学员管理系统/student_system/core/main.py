#  coding:utf-8
from core.student_view import StudentView
from core.teacher_view import TeacherView


def create_user():
    name = input(u"请输入用户姓名：").strip()
    account = input(u"请输入登录账号：").strip()
    password1 = input(u"请输入登录密码：").strip()
    password2 = input(u"请重复输入登录密码：").strip()
    qq = input(u"请输入用户qq账号：").strip()
    role = input(u"请输入编号设置用户角色（1：老师；2：学员；3：管理员）：").strip()
    rsp = create_user(name, account, password1, password2, qq, role)
    print(rsp.msg)


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


def console():
    while True:
        print(u"欢迎访问学员管理系统，")

        actions = {"1": register_user,
                   "2": user_views}
        num = input(u"请输入您选择的操作编号：").strip()
        if num not in actions:
            print(u"输入的操作项编号{0}不存在，请核对后再试".format(num))
            continue
        actions[num]()


if __name__ == "__main__":
    console()

