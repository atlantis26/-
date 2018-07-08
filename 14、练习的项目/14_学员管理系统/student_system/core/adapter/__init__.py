# coding:utf-8
from core.adapter.student_view import StudentView
from core.adapter.teacher_view import TeacherView
from core.adapter.manager_view import MangerView
from core.utils import SomethingError


class HybridViews(object):
    def __init__(self, username, role_tag):
        self.username = username
        self.role_tag = role_tag
        self.adapter_views()

    def role_tag(self):
        pass
    
    def adapter_views(self):
        try:
            views = {"student": StudentView,
                     "teacher": TeacherView,
                     "manager": MangerView}
            views[self.role_tag](self.username)
        except KeyError:
            raise SomethingError(u"登录用户角色类型出错，请联系管理员")
