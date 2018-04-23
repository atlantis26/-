# coding:utf-8
from core.orm import School, SomeError, ResponseData
from core.users import create_user
from core.views.base_view import BaseView
from conf.settings import AUTH_FLAG, RP
from core.db_handler import save_resources_pool
from core.auth import auth
import logging

logger = logging.getLogger("system.manager_view")


class Manager(object):
    @staticmethod
    def create_school(school_name):
        school_id = RP.get_school_id
        if RP.school_is_exists(school_name):
            raise SomeError(u"学校{0}已存在".format(school_name))
        school = School(school_id, school_name)
        RP.schools.append(school)
        save_resources_pool()

        return school

    @staticmethod
    def create_course(school_name, course_name, cycle, price):
        school = RP.school_is_exists(school_name)
        if not school:
            raise SomeError(u"学校{0}不存在".format(school_name))
        if RP.course_is_exists(school.id, course_name):
            raise SomeError(u"学校'{0}'已存在课程'{1}'".format(school_name, course_name))
        course_id = RP.get_course_id
        course = RP.schools[school.id].create_course(course_id, course_name, cycle, price)
        RP.courses.append(course)
        save_resources_pool()

        return course

    @staticmethod
    def create_class(school_name, class_name, course_name):
        school = RP.school_is_exists(school_name)
        course = RP.course_is_exists(school.id, course_name)
        if not school:
            raise SomeError(u"学校{0}不存在".format(school_name))
        if not course:
            raise SomeError(u"学校{0}不存在课程{1}".format(school_name, course_name))
        class_id = RP.get_class_id
        class1 = RP.schools[school.id].create_class(class_id, class_name, course.id)
        RP.classes.append(class1)
        save_resources_pool()

        return class1

    @staticmethod
    def create_teacher(teacher_name, username, password1, password2, role=u"讲师"):
        teacher = create_user(teacher_name, username, password1, password2, role)
        return teacher


class MangerView(BaseView):
    """管理员视图"""
    def __init__(self, username, password, role_id):
        BaseView.__init__(self, username, password, role_id)
        if AUTH_FLAG["is_authenticated"]:
            self.console()

    @auth(AUTH_FLAG)
    def console(self):
        """ 管理员视图主页"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.创建学校                   <\033[36;1m2\033[0m>.创建课程
                    <\033[36;1m3\033[0m>.创建班级                   <\033[36;1m4\033[0m>.创建讲师
                    <\033[36;1m5\033[0m>.查询已存在的教学资源列表    <\033[36;1m6\033[0m>.为讲师分配班级
                    <\033[36;1m7\033[0m>.登出系统
            """
            print(msg)
            actions = {"1": self.create_school,
                       "2": self.create_course,
                       "3": self.create_class,
                       "4": self.create_teacher,
                       "5": self.show_info,
                       "6": self.teacher_add_class,
                       "7": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            ret = actions[num]()
            print(ret.msg)

    @auth(AUTH_FLAG)
    def create_school(self):
        """创建学校"""
        try:
            school_name = input(u"请输入新建学校的名字：").strip()
            school = Manager.create_school(school_name)
            code = 200
            msg = u"创建学校{0}成功".format(school_name)
            data = school.__dict__
        except SomeError as e:
            code = 400
            msg = u"创建学校失败，原因：{0}".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def create_course(self):
        """创建课程"""
        try:
            school_name = input(u"请输入学校的名字：").strip()
            course_name = input(u"请输入课程的名字：").strip()
            cycle = input(u"请输入课程的学习周期（天）：").strip()
            price = input(u"请输入课程的学费：").strip()
            course = Manager.create_course(school_name, course_name, cycle, price)
            code = 200
            msg = u"创建课程{0}成功".format(course_name)
            data = course.__dict__
        except SomeError as e:
            code = 400
            msg = u"创建课程{0}失败，原因：".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def create_class(self):
        """创建班级"""
        try:
            school_name = input(u"请输入学校的名字：").strip()
            course_name = input(u"请输入课程的名字：").strip()
            class_name = input(u"请输入班级的名字：").strip()
            class1 = Manager.create_class(school_name, class_name, course_name)
            code = 200
            msg = u"创建班级{0}成功".format(class_name)
            data = class1.__dict__
        except SomeError as e:
            code = 400
            msg = u"创建班级{0}失败，原因：".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def create_teacher(self):
        """创建讲师角色"""
        try:
            teacher_name = input(u"请输入讲师的名字：").strip()
            username = input(u"请输入讲师登录系统的用户名：").strip()
            password1 = input(u"请输入设置密码：").strip()
            password2 = input(u"请再次输入设置密码：").strip()
            user = Manager.create_teacher(teacher_name, username, password1, password2, role=u"讲师")
            code = 200
            msg = u"创建讲师{0}成功".format(teacher_name)
            data = user.__dict__
        except SomeError as e:
            code = 400
            msg = u"创建讲师{0}失败，原因：".format(str(e))
            data = None
        logger.debug(ResponseData(code, msg, data).__dict__)

        return ResponseData(code, msg, data)

    @auth(AUTH_FLAG)
    def teacher_add_class(self):
        """为讲师分配班级"""
        try:
            teacher_id = eval(input(u"请输入讲师的员工编号：").strip())
            class_id = eval(input(u"请输入班级的编号：").strip())
            if not (isinstance(teacher_id, int) and 0 <= teacher_id <= len(RP.teachers)-1):
                raise SomeError(u"讲师的编号{0}不存在".format(teacher_id))
            if not (isinstance(class_id, int) and 0 <= class_id <= len(RP.classes) - 1):
                raise SomeError(u"班级的编号{0}不存在".format(class_id))
            RP.teachers[teacher_id].add_class(class_id)
            save_resources_pool()
            code = 200
            msg = u"分配班级成功".format(RP.teachers[teacher_id].name)
        except SomeError as e:
            code = 400
            msg = u"分配课程失败，原因：".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)

    @auth(AUTH_FLAG)
    def show_info(self):
        """查询已存在的教学资源列表"""
        try:
            print(u"学校资源列表：")
            for school in RP.schools:
                print(school.__dict__)
            print(u"课程资源列表：")
            for course in RP.courses:
                print(course.__dict__)
            print(u"班级资源列表：")
            for class1 in RP.classes:
                print(class1.__dict__)
            print(u"讲师资源列表：")
            for teacher in RP.teachers:
                print(teacher.__dict__)
            code = 200
            msg = u"查询资源成功"
        except SomeError as e:
            code = 400
            msg = u"查询资源失败，原因：".format(str(e))
        logger.debug(ResponseData(code, msg).__dict__)

        return ResponseData(code, msg)
