# -*- coding:utf-8 -*-
from model.models import User, Rule, Class, CourseRecord, Homework, user_m2m_class
from model import DBSession
from sqlalchemy import and_
from core.utils import SomeError


def create_user(name, account, password, qq, role_id):
    try:
        session = DBSession()
        user = User(name=name, account=account, password=password, qq=qq, role_id=role_id)
        session.add(user)
        session.commit()
        session.close()
    except Exception as e:
        raise SomeError("新用户数据入库时出错，详情：{0}".format(str(e)))


def query_user_by_qq(**kwargs):
    try:
        session = DBSession()
        user = session.query(User).filter(getattr(User, ) == qq).all()
        session.close()
    except Exception as e:
        raise SomeError("通过查询用户数据入库时出错，详情：{0}".format(str(e)))


def query_user_by_account(account):
    try:
        session = DBSession()
        session.commit()
        session.close()
    except Exception as e:
        raise SomeError("新用户数据入库时出错，详情：{0}".format(str(e)))