# coding:utf-8
from mall.core.orm import Flow, ResponseData
import logging

logger = logging.getLogger("mall.db")


def flow_sample(time_stamp, name, action, details):
    """生成购物消费流水信息记录"""
    flow = Flow(time_stamp, name, action, details)
    code = 200
    msg = u"新建消费流水模型成功,详情：{0}".format(flow.__dict__)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg, flow)
