# -*- coding:utf-8 -*-
from logconfig.logconfig import init_logging
from core.redis_handler import RedisHandler
import configparser
import os

# 初始化配置
config = configparser.ConfigParser()
ROOT = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(ROOT, "conf/server.properties")
config.read(CONF_FILE)

# 数据库设置
DB_NAME = config.get('db', 'database')
DB_USER = config.get('db', 'username')
DB_PASS = config.get('db', 'password')
DB_HOST = config.get('db', 'host')
DB_PORT = config.get('db', 'port')

# redis连接初始化
REDIS_HOST = config.get('redis', 'host')
REDIS_PORT = config.get('redis', 'port')
Redis_Handler = RedisHandler(REDIS_HOST, REDIS_PORT)

# 初始化日志系统
init_logging()
