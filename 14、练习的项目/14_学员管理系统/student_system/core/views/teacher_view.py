# coding:utf-8
from core.views.base_view import BaseView
from core.utils import ResponseData, SomeError
from core.auth import auth
import logging

logger = logging.getLogger("system.teacher_view")


class TeacherView(BaseView):
    """讲师视图"""
    def __init__(self, username, password, role_id):
        BaseView.__init__(self, username, password, role_id)
        if AUTH_FLAG["is_authenticated"]:
            self.console()

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

    def create_class(self):
        pass

    def delete_class(self):
        pass

    def modify_class(self):
        pass

    def query_class(self):
        pass

    def create_record(self):
        pass

    def list_homework_by_record_id(self):
        pass

    def update_homework_score(self):
        pass

