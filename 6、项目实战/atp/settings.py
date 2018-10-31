# coding:utf-8
import ConfigParser
import os
from logconfig.logconfig import init_logging

# 初始化配置
config = ConfigParser.ConfigParser()
ROOT = os.path.dirname(os.path.abspath(__file__))
CONF_FILE = os.path.join(ROOT, "conf/server.conf")
config.read(CONF_FILE)

# app相关设置
cookie_secret = config.get('app', 'cookie_secret')
_MIGU_AUTH_URL = config.get('app', '_MIGU_AUTH_URL')

# 配置日志
init_logging()
