# coding:utf-8
from logging.config import dictConfig
import os

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 主机目录，存储主机信息的相关配置
DB_Host = os.path.join(BASE_DIR, "db", "Host")
if not os.path.exists(DB_Host):
    os.mkdir(DB_Host)

# 主机组目录，存储主机组信息的相关配置
DB_HostGroups = os.path.join(BASE_DIR, "db", "HostGroups")
if not os.path.exists(DB_HostGroups):
    os.mkdir(DB_HostGroups)

# log日志相关设置
LOG_DIR = os.path.join(BASE_DIR, 'logs')
if not os.path.exists(LOG_DIR):
    os.mkdir(LOG_DIR)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(asctime)s - %(filename)s:%(lineno)d(%(module)s:%(funcName)s) - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(asctime)s - %(levelname)s - %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard'
        },
        'syslog': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'logging.handlers.SysLogHandler.LOG_LOCAL7',
            'formatter': 'standard',
        },
        'manager': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'manager.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'fabric': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'fabric.manager': {
            'handlers': ['manager'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}


def init_logging():
    """
    initial logging
    """
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    dictConfig(LOGGING)
