# coding:utf-8
from core.users import settle_user, create_user_flow
from core.db_handler import load_flow_pkl, load_user_pkl, save_resources_pool
from core.views.base_view import BaseView
from core.orm import ResponseData, SomeError
from core.auth import auth
from conf.settings import AUTH_FLAG, RP
import logging

logger = logging.getLogger("system.student_view")


class StudentView(BaseView):
    """学员视图"""
    def __init__(self, username, password, role_id):
        BaseView.__init__(self, username, password, role_id)
        if AUTH_FLAG["is_authenticated"]:
            self.console()

    @property
    def student_id(self):
        return [student.id for student in RP.students if student.username == self.username][0]

    @auth(AUTH_FLAG)
    def console(self):
        """ 学员视图主页"""
        while True:
            msg = u"""-------------------------------------------------
                您可以选择如下操作：
                    <\033[36;1m1\033[0m>.课程列表                   <\033[36;1m2\033[0m>.购买课程
                    <\033[36;1m3\033[0m>.用户充值                   <\033[36;1m4\033[0m>.查询用户消费/充值历史
                    <\033[36;1m5\033[0m>.查询个人信息               <\033[36;1m6\033[0m>.登出系统
            """
            print(msg)
            actions = {"1": self.show_courses,
                       "2": self.purchase_course,
                       "3": self.user_recharge,
                       "4": self.show_history,
                       "5": self.show_personal_info,
                       "6": self.logout}
            num = input(u"请输入您选择的操作的编号:").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    @auth(AUTH_FLAG)
    def show_courses(self):
        """展示课程信息列表"""
        try:
            print(u"课程列表如下：（您可以通过[\033[36;1m购买课程\033[0m]购买你想要学习的课程）")
            course_list = list()
            for course in RP.courses:
                school = RP.schools[course.school_id]
                classes = [class1 for class1 in RP.classes
                           if (class1.school_id == course.school_id and class1.course_id == course.id)]
                for cl in classes:
                    teacher = [teacher for teacher in RP.teachers if cl.id in teacher.class_id_list][0]
                    info = u"课程编号：{0}  课程名：{1}  学校：{2}  班级：{3}  讲师：{4}  学费：{5}元   学习周期：{6}天"\
                        .format(course.id, course.name, school.name, cl.name, teacher.name, course.price, course.cycle)
                    print(info)
                    course_list.append(info)
            msg = u"用户{0}查询课程列表成功".format(self.username)
            logger.debug(ResponseData(200, msg, course_list).__dict__)
        except SomeError as e:
            msg = u"用户{0}查询课程列表出错，原因：{0}".format(self.username, str(e))
            logger.debug(ResponseData(400, msg).__dict__)
        print(msg)

    @auth(AUTH_FLAG)
    def purchase_course(self):
        """购买课程"""
        try:
            num = eval(input(u"请输入你想要购买的课程的编号：").strip())
            if not isinstance(num, int):
                raise SomeError(u"输入的课程编号{0}必须是整数".format(num))
            if num < 0 or num > len(RP.courses)-1:
                raise SomeError(u"输入的课程编号{0}不存在，请核实后再试".format(num))
            if num in RP.students[self.student_id].course_id_list:
                raise SomeError(u"用户{0}已购买课程{1}，不能重复购买".format(self.username, num))
            course = RP.courses[num]
            user = load_user_pkl(self.username)
            # 付费
            settle_user(user, course.price, flag=0)
            # 学生添加课程
            RP.students[self.student_id].add_course(course.id)
            # 班级添加学生
            RP.classes[course.id].add_student(self.student_id)
            # 保存资源池变更信息，写入到文件
            save_resources_pool()
            # 生成流水信息
            create_user_flow(self.username, u"购买课程", course.__dict__)
            msg = u"购买课程{1}成功，花费{2}元".format(self.username, course.id, course.price)
            logger.debug(ResponseData(200, msg).__dict__)
        except SomeError as e:
            msg = u"购买课程失败，原因：{1}".format(self.username, str(e))
            logger.debug(ResponseData(400, msg).__dict__)
        print(msg)

    @auth(AUTH_FLAG)
    def user_recharge(self):
        """用户充值"""
        try:
            money = eval(input(u"请输入你想要充值的金额：").strip())
            if not isinstance(money, (int, float)):
                raise SomeError(u"输入的充值金额必须是数字")
            else:
                if money <= 0:
                    raise SomeError(u"输入的充值金额必须大于0")
            user = load_user_pkl(self.username)
            settle_user(user, money, flag=1)
            msg = u"充值成功，充值金额为{1}元".format(self.username, money)
            create_user_flow(self.username, u"用户充值", msg)
            logger.debug(ResponseData(200, msg).__dict__)
        except SomeError as e:
            msg = u"充值失败，原因：{1}".format(self.username, str(e))
            logger.debug(ResponseData(400, msg).__dict__)
        print(msg)

    @auth(AUTH_FLAG)
    def show_history(self):
        """用户消费/充值历史"""
        try:
            flow_list = load_flow_pkl(self.username)
            for flow in flow_list:
                print(flow.__dict__)
            msg = u"查询消费/充值流水历史成功"
            data = flow_list
            logger.debug(ResponseData(200, msg, data).__dict__)
        except SomeError as e:
            msg = u"查询消费/充值流水历史失败，原因：{0}".format(str(e))
            print(msg)
            logger.debug(ResponseData(400, msg).__dict__)

    @auth(AUTH_FLAG)
    def show_personal_info(self):
        """查询个人信息"""
        try:
            user = load_user_pkl(self.username)
            info1 = u"用户信息：{0}".format(user.__dict__)
            course_list = [RP.courses[c_id] for c_id in
                           [student.course_id_list for student in RP.students if student.username == self.username][0]]
            info2 = u"已购课程信息：{0}".format([course.__dict__ for course in course_list])
            data = info1 + "\n" + info2
            print(data)
            msg = u"查询个人信息成功"
            logger.debug(ResponseData(200, msg).__dict__)
        except SomeError as e:
            msg = u"查询个人信息失败，原因：{1}".format(self.username, str(e))
            print(msg)
            logger.debug(ResponseData(400, msg).__dict__)
