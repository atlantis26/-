# coding:utf-8
from core.db_handler import save_user_pkl, save_flow_pkl, save_resources_pool
from core.orm import ResponseData, User, Flow, Teacher, Student, SomeError
from conf.settings import DB_Users, RP
from datetime import datetime
import os
import logging


logger = logging.getLogger("system.users")


def init_manager(username, password):
    """初始化管理员账号"""
    if not user_is_exists(username):
        create_user("admin", username, password, password, u"管理员")


def create_user(name, username, password1, password2, role, balance=0):
    """创建新用户"""
    if user_is_exists(username):
        raise SomeError(u"系统用户名{0}已被使用".format(username))
    if password1 != password2:
        raise SomeError(u"两次设置密码不一致".format(username))
    user = User(username, password1, balance, role)
    save_user_pkl(user)
    if role == u"学员":
        student_id = RP.get_student_id
        data = Student(student_id, name, username)
        RP.students.append(data)
    elif role == u"讲师":
        teacher_id = RP.get_teacher_id
        data = Teacher(teacher_id, name, username)
        RP.teachers.append(data)
    else:
        raise SomeError(u"暂不支持{0}角色人员的创建".format(role))
    save_resources_pool()

    return data


def user_is_exists(username):
    """检测用户是否存在"""
    user_file = os.path.join(DB_Users, "{0}.pkl".format(username))
    if os.path.exists(user_file):
        return True


def settle_user(user, money, flag):
    """结算功能：
                flag=0：表示支出业务；
                flag=1：表示存入业务；
    """
    if flag == 0:
        if user.balance < money:
            raise SomeError(u"结算失败，用户{0}的余额不足，当前余额为：{1}元".format(user.username, user.balance))
        user.balance -= money
        save_user_pkl(user)
        msg = u"结算成功，用户{0}扣款支出{1}元，当前余额为：{2}元".format(user.username, money, user.balance)
    elif flag == 1:
        user.balance += money
        save_user_pkl(user)
        msg = u"结算成功，用户{0}存入{1}元,当前余额为：{2}元".format(user.username, money, user.balance)
    else:
        raise SomeError(u"暂不支持此结算方式")

    return ResponseData(200, msg)


def create_user_flow(username, action, details):
    """记录用户流水"""
    now = datetime.now()
    time_stamp = now.strftime("%Y-%m-%d-%H-%M-%S")
    flow = Flow(time_stamp, username, action, details)
    save_flow_pkl(flow)
    msg = u"用户流水入库成功，流水详情：{0}".format(flow.__dict__)

    return ResponseData(200, msg)
