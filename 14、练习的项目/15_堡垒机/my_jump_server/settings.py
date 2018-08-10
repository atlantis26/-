# -*- coding:utf-8 -*-
from logconfig.logconfig import init_logging
import configparser
import os

# 初始化配置
config = configparser.ConfigParser()
ROOT = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(ROOT, "conf/server.properties")
config.read(CONF_FILE)

# 数据库设置
DB_NAME = config.get('models', 'database')
DB_USER = config.get('models', 'username')
DB_PASS = config.get('models', 'password')
DB_HOST = config.get('models', 'host')
DB_PORT = config.get('models', 'port')

# 初始化日志系统
init_logging()
