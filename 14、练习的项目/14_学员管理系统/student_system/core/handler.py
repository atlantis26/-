#  coding:utf-8
from db.db_handler import DatabaseHandler
from core.utils import SomeError, ResponseData


def login(account, password):
    user = DatabaseHandler.query_user_by_account(account, password)
    if not user:
        raise SomeError(u"用户账号或密码错误")
    return user.__dict__

