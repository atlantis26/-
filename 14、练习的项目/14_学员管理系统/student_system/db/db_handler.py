# -*- coding:utf-8 -*-
from db.orm import User, Rule, Class, CourseRecord, Homework, user_m2m_class
from db import DBSession
from sqlalchemy import and_
from core.utils import SomeError


class DatabaseHandler(object):
    @staticmethod
    def create_user(name, account, password, qq, role_id):
        try:
            session = DBSession()
            user = User(name=name, account=account, password=password, qq=qq, role_id=role_id)
            session.add(user)
            session.commit()
            session.close()
        except Exception as e:
            raise SomeError("新用户数据入库时出错，详情：{0}".format(str(e)))

    @staticmethod
    def query_user_by_account(account, password):
        try:
            session = DBSession()
            user = session.query(User).filter(and_(User.account == account, User.password == password)).first()
            session.commit()
            session.close()
            return user
        except Exception as e:
            raise SomeError("新用户数据入库时出错，详情：{0}".format(str(e)))

