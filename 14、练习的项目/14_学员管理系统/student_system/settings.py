# -*- coding:utf-8 -*-
from logconfig.logconfig import init_logging
import configparser
import os

# 初始化配置
config = configparser.ConfigParser()
ROOT = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(ROOT, "conf/server_properties.conf")
config.read(CONF_FILE)

# 数据库设置
DB_NAME = config.get('db', 'database')
DB_USER = config.get('db', 'username')
DB_PASS = config.get('db', 'password')
DB_HOST = config.get('db', 'host')
DB_PORT = config.get('db', 'port')

# 初始化日志系统
init_logging()
