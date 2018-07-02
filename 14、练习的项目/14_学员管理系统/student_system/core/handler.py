#  coding:utf-8
from db.db_handler import DatabaseHandler
from core.utils import SomeError, ResponseData
import logging

logger = logging.getLogger("system.handler")


def login(account, password):
    try:
        user = DatabaseHandler.query_user_by_account(account, password)
        if not user:
            raise SomeError(u"用户账号或密码错误")
        code = 200
        msg = "用户登录验证成功"
        data = user.__dict__
    except SomeError as e:
        code = 400
        msg = "用户登录验证失败，详情：{0}".format(str(e))
        data = None
    logger.debug(ResponseData(code, msg, data).__dict__)

    return ResponseData(code, msg, data)

