#  coding:utf-8
from db.db_handler import DatabaseHandler
from core.utils import SomethingError, ResponseData
import logging

logger = logging.getLogger("system.handler")


class Handler(object):
    @staticmethod
    def login(account, password):
        try:
            user = DatabaseHandler.query_user_by_account(account, password)
            if not user:
                raise SomethingError(u"用户账号或密码错误")
            code = 200
            msg = "登录成功"
            data = user.__dict__
        except SomethingError as e:
            code = 400
            msg = "登录失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_user(name, account, password1, password2, qq, role_name):
        try:
            if password1 != password2:
                raise SomethingError("创建用户失败，两次密码不一致")
            role = DatabaseHandler.query_role_by_name(role_name)
            if not role:
                raise SomethingError(u"用户角色类型‘{0}’不存在".format(role_name))
            role_id = role.id
            if DatabaseHandler.query_user_by_qq(qq):
                raise SomethingError(u"qq号'{0}'已被使用".format(qq))
            if DatabaseHandler.query_user_by_account(account):
                raise SomethingError(u"用户账号名'{0}'已被使用".format(account))
            user = DatabaseHandler.create_user(name, account, password1, qq, role_id)
            code = 200
            msg = "创建用户成功"
            data = user.__dict__
        except SomethingError as e:
            code = 400
            msg = "创建用户失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def delete_user(user_id):
        try:
            if not DatabaseHandler.query_user_by_id(user_id):
                raise SomethingError(u"id为'{0}'的用户不存在".format(user_id))
            DatabaseHandler.delete_user_by_id(user_id)
            code = 200
            msg = "删除用户成功"
        except SomethingError as e:
            code = 400
            msg = "删除用户失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def update_user(user_id, name, password, qq, role_name):
        try:
            user = DatabaseHandler.query_user_by_id(user_id)
            if not user:
                raise SomethingError(u"id为'{0}'的用户不存在".format(user_id))
            role = DatabaseHandler.query_role_by_name(role_name)
            if not role:
                raise SomethingError(u"用户角色类型‘{0}’不存在".format(role_name))
            role_id = role.id
            if DatabaseHandler.query_user_by_qq(qq):
                if user.qq != qq:
                    raise SomethingError(u"qq号'{0}'已被使用".format(qq))
            DatabaseHandler.update_user(user_id, name, password, qq, role_id)
            code = 200
            msg = "更新用户成功"
        except SomethingError as e:
            code = 400
            msg = "更新用户失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def query_user(user_id):
        try:
            user = DatabaseHandler.query_user_by_id(user_id)
            if not user:
                raise SomethingError(u"id为'{0}'的用户不存在".format(user_id))
            code = 200
            msg = "查询用户详情成功"
            data = user.__dict__
        except SomethingError as e:
            code = 400
            msg = "查询用户详情失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_user():
        try:
            user_list = DatabaseHandler.list_user()
            code = 200
            msg = "查询用户列表成功"
            data = user_list
        except SomethingError as e:
            code = 400
            msg = "查询用户列表失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_class(name):
        try:
            if DatabaseHandler.query_class_by_name(name):
                raise SomethingError(u"班级名称'{0}'已被使用".format(name))
            class1 = DatabaseHandler.create_class(name)
            code = 200
            msg = "创建班级成功"
            data = class1.__dict__
        except SomethingError as e:
            code = 400
            msg = "创建班级失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def delete_class(class_id):
        try:
            if not DatabaseHandler.query_class_by_id(class_id):
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            DatabaseHandler.delete_class_by_id(class_id)
            code = 200
            msg = "删除班级成功"
        except SomethingError as e:
            code = 400
            msg = "删除班级失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def update_class(class_id, name):
        try:
            if not DatabaseHandler.query_class_by_id(class_id):
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            class1 = DatabaseHandler.query_class_by_name(name)
            if class1 and class1.name != name:
                raise SomethingError(u"名称'{0}'已被使用".format(name))
            DatabaseHandler.delete_class_by_id(class_id)
            code = 200
            msg = "修改班级成功"
        except SomethingError as e:
            code = 400
            msg = "修改班级失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def query_class(class_id):
        try:
            class1 = DatabaseHandler.query_class_by_id(class_id)
            if not class1:
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            code = 200
            msg = "查询班级详情成功"
            data = class1.__dict__
        except SomethingError as e:
            code = 400
            msg = "查询班级详情失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_class():
        try:
            class_list = DatabaseHandler.list_class()
            code = 200
            msg = "查询班级列表成功"
            data = class_list
        except SomethingError as e:
            code = 400
            msg = "查询班级列表失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_record(username, class_id, description):
        try:
            teacher = DatabaseHandler.query_user_by_account(username)
            if not teacher:
                raise SomethingError(u"账号为'{0}'的教师不存在".format(username))
            class1 = DatabaseHandler.query_class_by_id(class_id)
            student_list = class1.User
            if class1:
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            record = DatabaseHandler.create_record(teacher.id, class_id, description)
            # 同时为班级的所有学生创建本次课程的家庭作业

            code = 200
            msg = "创建上课记录成功"
        except SomethingError as e:
            code = 400
            msg = "创建上课记录失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
