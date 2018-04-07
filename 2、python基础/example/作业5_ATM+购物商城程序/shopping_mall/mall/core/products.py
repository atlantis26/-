# coding:utf-8
from atm.core.main import pay
from mall.conf.settings import DB_TYPE, DB_Products, DB_Flows_History
from mall.core.orm import ResponseData
from mall.db.flow_sample import flow_sample
from datetime import datetime
import os
import json
import logging


logger = logging.getLogger("mall.products")


def get_products():
    """加载商品列表"""
    if DB_TYPE == "FileStorage":
        with open(DB_Products, "r") as f:
            products = eval(f.read().strip())
        code = 200
        msg = u"加载商品列表成功，详情：{0}".format(products)
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
        products = None
    logger.debug(ResponseData(code, msg, products).__dict__)

    return ResponseData(code, msg, products)


def purchase_product(product_id):
    """购物"""
    rsp = get_products()
    if rsp.code == 200:
        products = rsp.data
        if product_id > len(products)-1 or product_id < 0:
            code = 400
            msg = u"商品编号{0}不存在，请仔细查看后再选择".format(product_id)
        else:
            p_name = products[product_id][0]
            p_price = products[product_id][1]
            rsp = pay(p_price)
            if rsp.code == 200:
                code = 200
                msg = u"购买商品{0}成功，共计花费{1}元".format(p_name, p_price)
            else:
                code = 400
                msg = u"购买商品{0}失败，原因：{1}".format(p_name, rsp.msg)
    else:
        code = 400
        msg = u"购买商品{0}失败，原因：{0}".format(rsp.msg)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def purchase_flow(name, action, details):
    if DB_TYPE == "FileStorage":
        now = datetime.now()
        time_stamp = now.strftime("%Y-%m-%d %H:%M:%S")
        rsp = flow_sample(time_stamp, name, action, details)
        if rsp.code == 200:
            flow = rsp.data
            tmp = "flows_history_{0}_{1}.json".format(now.year, now.month)
            flows_history_file = os.path.join(DB_Flows_History, tmp)
            with open(flows_history_file, "a") as f:
                f.write("{0}\n".format(json.dumps(flow.__dict__)))
                f.flush()
            code = 200
            msg = u"购物消费流水入库成功，流水详情：{0}".format(flow.__dict__)
        else:
            code = 400
            msg = u"购物消费流水入库失败，失败原因：{0}".format(rsp.msg)
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
    logger.debug(ResponseData(code, msg).__dict__)

    return ResponseData(code, msg)


def query_purchase_flow(name, year, month):
    """查询购物单月流水记录"""
    flow_list = list()
    if DB_TYPE == "FileStorage":
        tmp = "flows_history_{0}_{1}.json".format(year, month)
        flows_history_file = os.path.join(DB_Flows_History, tmp)
        if os.path.exists(flows_history_file):
            with open(flows_history_file, "r") as f:
                for flow in f:
                    if name == json.loads(flow)["name"]:
                        flow_list.append(flow)
            code = 200
            msg = u"查询成功"
        else:
            code = 400
            msg = u"查询失败，无相关流水信息"
    else:
        code = 400
        msg = u"暂不支持{0}类型数据库，请联系管理员".format(DB_TYPE)
    logger.debug(ResponseData(code, msg, flow_list).__dict__)

    return ResponseData(code, msg, flow_list)

