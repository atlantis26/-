# coding:utf-8
import redis
import json
from datetime import datetime
from models.db_handler import DatabaseHandler
from models.orm import AuditLog
from settings import REDIS_HOST, REDIS_PORT


class RedisHandler(object):
    def __init__(self, host, port=6379, key="AuditLogs", limit=10):

        self.host = host
        self.port = port
        self.key = key
        self.limit = limit
        pool = redis.ConnectionPool(host=self.host,
                                    port=self.port,
                                    decode_responses=True)
        self.client = redis.Redis(connection_pool=pool)

    def push(self, log):
        """添加log到redis的列表AuditLogs中，当log数大于等于10条时，写入到数据库"""
        self.client.rpush(self.key, json.dumps(log))
        num = self.client.llen(self.key)
        if num >= self.limit:
            # 获取列表中的所有元素
            logs = self.client.lrange(self.key, 0, -1)
            lst = []
            for d in logs:
                d = json.loads(d)
                time_stamp = float(d.pop("date"))
                date = datetime.utcfromtimestamp(time_stamp)
                log = AuditLog(date=date, **d)
                lst.append(log)
            DatabaseHandler.commit_orm_object(lst)
            # 清空列表中的所有元素
            self.client.ltrim(self.key, 1, 0)


Redis_Handler = RedisHandler(REDIS_HOST, REDIS_PORT)
