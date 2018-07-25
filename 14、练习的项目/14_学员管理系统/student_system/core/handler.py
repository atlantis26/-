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
            msg = u"登录成功"
            data = user.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"登录失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_user(name, account, password1, password2, qq, role_name):
        try:
            if password1 != password2:
                raise SomethingError(u"创建用户失败，两次密码不一致")
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
            msg = u"创建用户成功"
            data = user.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"创建用户失败，详情：{0}".format(str(e))
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
            msg = u"删除用户成功"
        except SomethingError as e:
            code = 400
            msg = u"删除用户失败，详情：{0}".format(str(e))
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
            msg = u"更新用户成功"
        except SomethingError as e:
            code = 400
            msg = u"更新用户失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def query_user(user_id):
        try:
            user = DatabaseHandler.query_user_by_id(user_id)
            if not user:
                raise SomethingError(u"id为'{0}'的用户不存在".format(user_id))
            code = 200
            msg = u"查询用户详情成功"
            data = user.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"查询用户详情失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_user():
        try:
            user_list = DatabaseHandler.list_user()
            code = 200
            msg = u"查询用户列表成功"
            data = user_list
        except SomethingError as e:
            code = 400
            msg = u"查询用户列表失败，详情：{0}".format(str(e))
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
            msg = u"创建班级成功"
            data = class1.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"创建班级失败，详情：{0}".format(str(e))
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
            msg = u"删除班级成功"
        except SomethingError as e:
            code = 400
            msg = u"删除班级失败，详情：{0}".format(str(e))
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
            msg = u"修改班级成功"
        except SomethingError as e:
            code = 400
            msg = u"修改班级失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def query_class(class_id):
        try:
            class1 = DatabaseHandler.query_class_by_id(class_id)
            if not class1:
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            code = 200
            msg = u"查询班级详情成功"
            data = class1.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"查询班级详情失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_class():
        try:
            class_list = DatabaseHandler.list_class()
            code = 200
            msg = u"查询班级列表成功"
            data = class_list
        except SomethingError as e:
            code = 400
            msg = u"查询班级列表失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_record(username, class_id, description):
        try:
            teacher = DatabaseHandler.query_user_by_account(username)
            if not teacher:
                raise SomethingError(u"账号为'{0}'的教师不存在".format(username))
            if not DatabaseHandler.query_class_by_id(class_id):
                raise SomethingError(u"id为'{0}'的班级不存在".format(class_id))
            record = DatabaseHandler.create_record(teacher.id, class_id, description)
            # 上课班级所属的同学添加家庭作业记录
            student_list = DatabaseHandler.list_students_by_class_id(class_id)
            for student_id in student_list:
                DatabaseHandler.create_homework(record.id, student_id, score=None, homework_path=None)
            code = 200
            msg = u"创建上课记录成功"
            data = record.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"创建上课记录失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_record():
        try:
            record_list = DatabaseHandler.list_record()
            code = 200
            msg = u"查询上课记录列表成功"
            data = record_list
        except SomethingError as e:
            code = 400
            msg = u"查询上课记录列表失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def create_homework(record_id, student_id, score=None, homework_path=None):
        try:
            if not DatabaseHandler.query_record_by_id(record_id):
                raise SomethingError(u"上课记录id'{0}'不存在".format(record_id))
            if not DatabaseHandler.query_user_by_id(student_id):
                raise SomethingError(u"学员id'{0}'不存在".format(student_id))
            homework = DatabaseHandler.create_homework(record_id, student_id, score, homework_path)
            code = 200
            msg = u"创建学员家庭作业记录成功"
            data = homework.to_dict()
        except SomethingError as e:
            code = 400
            msg = u"创建学员家庭作业记录失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def list_homework_by_record_id(record_id):
        try:
            if not DatabaseHandler.query_record_by_id(record_id):
                raise SomethingError(u"上课记录id不存在")
            home_list = DatabaseHandler.list_homework_by_record_id(record_id)
            code = 200
            msg = u"查询上课作业列表成功"
            data = home_list
        except SomethingError as e:
            code = 400
            msg = u"查询上课作业列表失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def update_homework_score(homework_id, score):
        try:
            if not DatabaseHandler.query_homework_by_id(homework_id):
                raise SomethingError(u"课程作业id不存在")
            if not (isinstance(score, (int, float)) and 0 <= score <= 100):
                raise SomethingError(u"成绩分数必须是大于等于0小于等于100的数值")
            DatabaseHandler.update_homework_score(homework_id, score)
            code = 200
            msg = u"更新学员作业成绩成功"
        except SomethingError as e:
            code = 400
            msg = u"更新学员作业成绩失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def commit_homework(homework_id, file_path):
        try:
            if not DatabaseHandler.query_homework_by_id(homework_id):
                raise SomethingError(u"课程作业id不存在")
            DatabaseHandler.update_homework_path(homework_id, file_path)
            code = 200
            msg = u"上传作业文件成功"
        except SomethingError as e:
            code = 400
            msg = u"上传作业文件失败，详情：{0}".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def show_student_info(username):
        try:
            student = DatabaseHandler.query_user_by_account(username)
            if not student:
                raise SomethingError(u"学员账号不存在")
            class_list = DatabaseHandler.list_class_by_student_id(student.id)
            class_list = [DatabaseHandler.query_class_by_id(c["class_id"]).name for c in class_list]
            code = 200
            msg = u"查询学员个人信息成功"
            data = [student.to_dict(), class_list]
        except SomethingError as e:
            code = 400
            msg = u"查询学员个人信息失败，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def show_student_homework(username):
        try:
            student = DatabaseHandler.query_user_by_account(username)
            if not student:
                raise SomethingError(u"学员账号不存在")
            homework_list = DatabaseHandler.list_homework_by_student_id(student.id)
            ret_list = list()
            for homework in homework_list:
                record = DatabaseHandler.query_record_by_id(homework["record_id"]).to_dict()
                ret_list.append({u"课程记录": record, "课程作业：": homework})
            code = 200
            msg = u"查询学员个人家庭作业信息成功"
            data = ret_list
        except SomethingError as e:
            code = 400
            msg = u"查询学员个人家庭作业信息成功，详情：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @staticmethod
    def class_add_student_by_qq(class_id, qq):
        try:
            if not DatabaseHandler.query_class_by_id(class_id):
                raise SomethingError(u"班级id不存在")
            user = DatabaseHandler.query_user_by_qq(qq)
            if not user:
                raise SomethingError(u"本系统不存在此qq号‘{0}’".format(qq))
            DatabaseHandler.create_mapping_class_user(class_id, user.id)
            code = 200
            msg = u"通过qq号添加学员到班级成功"
        except SomethingError as e:
            code = 400
            msg = u"通过qq号添加学员到班级失败，详情：{0}".format(str(e))

        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @staticmethod
    def query_score_and_rank(username, homework_id):
        try:
            user = DatabaseHandler.query_user_by_account(username)
            homework = DatabaseHandler.query_homework_by_id(homework_id)
            if not homework:
                raise SomethingError(u"课程作业id不存在")
            if user.id != homework.student_id:
                raise SomethingError(u"课程作业id错误，请核对后再试")
            homework_list = DatabaseHandler.list_homework()
            for i in range(len(homework_list) - 1):  # 这个循环负责设置冒泡排序进行的次数
                for j in range(len(homework_list) - i - 1):  # ｊ为列表下标
                    if homework_list[j].score > homework_list[j + 1].score:
                        homework_list[j], homework_list[j + 1] = homework_list[j + 1], homework_list[j]
            homework_list = reversed(homework_list)
            data = dict()
            for index, h in enumerate(homework_list):
                if h.id == int(homework_id):
                    data["rank"] = index + 1
                    data["score"] = h.score
                    break
            code = 200
            msg = u"查询个人成绩与当前排名成功"
            data = data if data else u"你的作业还未被老师查阅并给出成绩"
        except SomethingError as e:
            code = 400
            msg = u"查询个人成绩与当前排名失败，详情：{0}".format(str(e))
            data = None

        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

