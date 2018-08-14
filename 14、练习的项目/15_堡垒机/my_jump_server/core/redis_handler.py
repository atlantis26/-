# coding:utf-8
import redis
from models.db_handler import DatabaseHandler
from settings import REDIS_HOST, REDIS_PORT


class RedisHandler(object):
    def __init__(self, host, port=6379):

        self.host = host
        self.port = port
        pool = redis.ConnectionPool(host=self.host,
                                    port=self.port,
                                    decode_responses=True)
        self.client = redis.Redis(connection_pool=pool)
        self.key = "AuditLogs"

    def push(self, log):
        """添加log到redis的列表AuditLogs中，当log数大于等于10条时，写入到数据库"""
        num = self.client.llen(self.key)
        if num >= 10:
            # 获取列表中的所有元素
            logs = self.client.lrange(self.key, 0, -1)
            DatabaseHandler.commit_orm_object(logs)
            # 清空列表中的所有元素
            self.client.ltrim(self.key, 1, 0)
        else:
            self.client.rpush(self.key, log)


Redis_Handler = RedisHandler(REDIS_HOST, REDIS_PORT)
