# coding:utf-8
from core.adapter.student_view import StudentView
from core.adapter.teacher_view import TeacherView
from core.adapter.manager_view import MangerView
from core.utils import SomethingError
from db.db_handler import DatabaseHandler


class HybridViews(object):
    def __init__(self, username, role_id):
        self.username = username
        self.role_id = role_id
        self.role_name = None
        self.adapter_views()

    @property
    def role_tag(self):
        if self.role_name is None:
            role = DatabaseHandler.query_role_by_id(self.role_id)
            self.role_name = role.name
        return self.role_name
    
    def adapter_views(self):
        try:
            views = {"student": StudentView,
                     "teacher": TeacherView,
                     "manager": MangerView}
            views[self.role_tag](self.username)
        except KeyError:
            raise SomethingError(u"登录用户角色类型出错，请联系管理员")
