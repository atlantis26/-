# coding:utf-8
from core.views.base_view import BaseView
from core.orm import ResponseData, SomeError
from core.auth import auth
from conf.settings import AUTH_FLAG, RP
import logging

logger = logging.getLogger("system.teacher_view")


class TeacherView(BaseView):
    """讲师视图"""
    def __init__(self, username, password, role_id):
        BaseView.__init__(self, username, password, role_id)
        if AUTH_FLAG["is_authenticated"]:
            self.console()

    @property
    def teacher_id(self):
        return [teacher.id for teacher in RP.teachers if teacher.username == self.username][0]

    @auth(AUTH_FLAG)
    def console(self):
        """ 讲师视图主页"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.查看负责的班级                <\033[36;1m2\033[0m>.选班上课
                    <\033[36;1m3\033[0m>.查看班级学员信息                  <\033[36;1m4\033[0m>.修改学生作业
                    <\033[36;1m5\033[0m>.登出用户 
            """
            print(msg)
            actions = {"1": self.show_classes,
                       "2": self.select_class,
                       "3": self.show_student,
                       "4": self.correcting_homework,
                       "5": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    def show_classes(self):
        """查看负责的班级列表"""
        try:
            print(u"您负责的班级信息：")
            teacher = RP.teachers[self.teacher_id]
            class_list = list()
            for class_id in teacher.class_id_list:
                class1 = RP.classes[class_id]
                course = RP.courses[class1.course_id]
                school = RP.schools[class1.school_id]
                info = u"班级编号：{0}  名称：{1}  课程：{2}  学校：{3}"\
                    .format(class1.id, class1.name, course.name, school.name)
                print(info)
                class_list.append(info)
            msg = u"查询班级列表成功".format(self.username)
            logger.debug(ResponseData(200, msg, class_list).__dict__)
        except SomeError as e:
            msg = u"查询班级列表出错，原因：{0}".format(self.username, str(e))
            logger.debug(ResponseData(400, msg).__dict__)
            print(msg)

    def show_student(self):
        """查看某班级下的学生列表"""
        try:
            teacher = RP.teachers[self.teacher_id]
            class_id = eval(input(u"请输入你选择的班级的编号：").strip())
            if class_id not in teacher.class_id_list:
                raise SomeError(u"输入的班级编号不存在")
            class1 = RP.classes[class_id]
            student_list = list()
            print(u"班级{0}的学员信息列表:".format(class1.name))
            for student_id in class1.student_id_list:
                student = RP.students[student_id]
                school = RP.schools[class1.school_id]
                info = u"学员编号：{0}  学员名字：{1} 所属学校： {2} 班级: {3}"\
                    .format(student.id, student.name, school.name, class1.name)
                print(info)
                student_list.append(info)
            msg = u"查询学员信息成功".format(self.username)
            logger.debug(ResponseData(200, msg, student_list).__dict__)
        except SomeError as e:
            msg = u"查询学员信息失败，原因：{1}".format(self.username, str(e))
            logger.debug(ResponseData(400, msg).__dict__)
            print(msg)

    def select_class(self):
        """选课暂不实现"""
        pass

    def correcting_homework(self):
        """批改作业暂不实现"""
        pass
