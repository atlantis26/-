# coding:utf-8
from core.orm import Student
from core.users import settle_user
from core.views.base_view import BaseView
from core.orm import SomeError


class StudentView(BaseView):
    """学员视图"""
    def __init__(self, username, password, schools):
        BaseView.__init__(self, username, password, schools)
        self.courses_list = list()
        self.__init_courses()
        self.console()

    def console(self):
        """ 学员视图主页"""
        msg = u"""-------------------------------------------------
            您可以选择如下操作：
                <\033[36;1m1\033[0m>.课程列表                   <\033[36;1m2\033[0m>.购买课程
                <\033[36;1m3\033[0m>.账户充值                   <\033[36;1m4\033[0m>.查询消费历史
                <\033[36;1m5\033[0m>.查询个人信息               <\033[36;1m6\033[0m>.重置密码 
                <\033[36;1m7\033[0m>.登出账户
        """
        print(msg)
        while True:
            actions = {"1": self.show_course_list,
                       "2": self.purchase_course,
                       "3": self.course_in_learning,
                       "4": self.show_history,
                       "5": self.show_personal_info,
                       "6": self.reset_password,
                       "7": self.logout}
            num = input(u"请输入您选择的操作的编号").strip()
            if num not in actions:
                print(u"输入的操作编号{0}不存在，请核对后再试".format(num))
                continue
            actions[num]()

    def __init_courses(self):
        """初始化将展示给学员的课程列表信息"""
        course_id = 1
        for school in self.schools:
            for course in school.courses:
                for class1 in school.classes:
                    self.courses_list.append([str(course_id), course.name, school.name,
                                              class1.name, course.price, course.cycle])
                    course_id += 1

    def show_course_list(self):
        """展示可选择的课程信息列表"""
        print(u"课程列表如下：（您可以通过[<\033[36;1m购买课程\033[0m>]功能报名你想要学习的课程）")
        for course_info in self.courses_list:
            info = u"课程编号：{0}  课程名：{1}  所属学校：{2}  所属班级：{3}  所需学费：{4}元   学习周期：{5}天"\
                .format(*course_info)
            print(info)

    def purchase_course(self):
        """购买课程"""
        num = input(u"请输入你想要购买的课程的编号：").strip()
        courses = [i for i in self.courses_list if num == i[0]]
        if not courses:
            print(u"课程编号{0}不存在，你可用通过<\033[36;1m课程列表\033[0m>功能查询，请核对后再试".format(num))
        else:
            info = u"你将购买的课程：课程编号：{0}  课程名：{1}  所属学校：{2}  所属班级：{3}  " \
                   u"所需学费：{4}元   学习周期：{5}天".format(*courses[0])
            print(info)
            num = input(u"请确定是否购买该课程,输入Y确认，输入N取消：").strip()
            if num == "Y":
                # 支付
                rsp = settle_user(self.username, courses[0][4])
                if rsp.cpde == 200:
                    # 创建学员角色
                    student = Student()
                else:


            #


    def course_in_learning(self):
        pass
