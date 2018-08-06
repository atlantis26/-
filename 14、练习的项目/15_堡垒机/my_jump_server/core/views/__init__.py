# coding:utf-8
from core.views.manager_view import ManagerView
from core.views.user_view import UserView
from core.utils import SomethingError
from models.orm import Role
from models import DBSession


class HybridViews(object):
    def __init__(self, user_id, role_id):
        self.user_id = user_id
        self.role_id = role_id
        self.role_name = None
        self.adapter_views()

    @property
    def role_tag(self):
        if self.role_name is None:
            session = DBSession()
            role = session.query(Role).filter(Role.id == self.role_id).first()
            self.role_name = role.name
        return self.role_name

    def adapter_views(self):
        try:
            views = {"user": UserView,
                     "manager": ManagerView}
            views[self.role_tag](self.user_id)
        except KeyError:
            raise SomethingError(u"登录用户角色类型出错，请联系管理员")
