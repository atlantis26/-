# -*- coding:utf-8 -*-
from models.orm import UserProfile, Role, RemoteUser, Host, Group, BindHost, AuditLog
from models import DBSession
from sqlalchemy import and_
from core.utils import SomethingError


class DatabaseHandler(object):
    @staticmethod
    def create_user(username, password, role_id):
        try:
            session = DBSession()
            user = UserProfile(username=username, password=password, role_id=int(role_id))
            session.add(user)
            session.commit()
            user = session.query(UserProfile).filter(UserProfile.username == username).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_profile_by_id(user_id):
        try:
            session = DBSession()
            user = session.query(UserProfile).filter(UserProfile.id == user_id).first()
            session.close()
            return user
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_profile_by_account(username, password):
        try:
            session = DBSession()
            user_obj = session.query(UserProfile).filter(and_(UserProfile.username == username,
                                                              UserProfile.password == password)).first()
            session.close()
            return user_obj
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_remote_user_by_password(username, password):
        try:
            session = DBSession()
            remote_user_obj = session.query(RemoteUser).filter(and_(RemoteUser.username == username,
                                                                    RemoteUser.password == password)).first()
            session.close()
            return remote_user_obj
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_remote_user_by_auth_type(username, auth_type):
        try:
            session = DBSession()
            remote_user_obj = session.query(RemoteUser).filter(and_(RemoteUser.username == username,
                                                                    RemoteUser.auth_type == auth_type)).first()
            session.close()
            return remote_user_obj
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def create_audit_log(user_id, bind_host_id, action, cmd, timestamp):
        try:
            session = DBSession()
            log = AuditLog(user_id=user_id, bind_host_id=bind_host_id, action_type=action, cmd=cmd, date=timestamp)
            session.add(log)
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_host_by_id(host_id):
        try:
            session = DBSession()
            host = session.query(Host).filter(Host.id == host_id).first()
            session.close()
            return host
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_host_by_name(host_name):
        try:
            session = DBSession()
            host = session.query(Host).filter(Host.hostname == host_name).first()
            session.close()
            return host
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_group_by_names(group_name_list):
        try:
            session = DBSession()
            groups = session.query(Group).filter(Group.name.in_(group_name_list)).all()
            session.close()
            return groups
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_bindhost_by_names(host_name_list):
        try:
            session = DBSession()
            bind_hosts = session.query(BindHost).filter(Host.hostname.in_(host_name_list)).all()
            session.close()
            return bind_hosts
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def commit_orm_object(obj_or_list):
        try:
            session = DBSession()
            if isinstance(obj_or_list, list):
                session.add_all(obj_or_list)
            else:
                session.add(obj_or_list)
            session.commit()
            session.close()
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_user_profiles_by_usernames(usernames):
        try:
            session = DBSession()
            user_profiles = session.query(UserProfile).filter(UserProfile.username.in_(usernames).all())
            session.close()
            return user_profiles
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def list_role_by_names(names):
        try:
            session = DBSession()
            roles = session.query(Role).filter(Role.username.in_(names).all())
            session.close()
            return roles
        except Exception as e:
            raise SomethingError(u"操作数据库时出错，详情：{0}".format(str(e)))
