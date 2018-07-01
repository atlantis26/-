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

    def commit_homework(self, student_id, record_id, file_path):
        pass

    def query_score(self):
        pass

    def query_rank(self):
        pass
