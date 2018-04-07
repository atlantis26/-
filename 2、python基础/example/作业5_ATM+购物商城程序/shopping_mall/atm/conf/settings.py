# coding:utf-8
import os
from logging.config import dictConfig

# ATM系统根目录
ATM_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 数据库设置
DB_TYPE = "FileStorage"  # 当前只支持文件存储信息方式，可扩展，留有接入MySQL等数据库的可能

# 文件存储信息相关配置
DB_Accounts = os.path.join(ATM_DIR, "db", "accounts")
DB_Flows_History = os.path.join(ATM_DIR, "db", "flows_history")
if not os.path.exists(DB_Accounts):
    os.mkdir(DB_Accounts)
if not os.path.exists(DB_Flows_History):
    os.mkdir(DB_Flows_History)

# # MySQL或其他关系数据库的相关配置
# DB_HOST = ""
# DB_PORT = ""
# DB_USER = ""
# DB_PASSWORD = ""

# 账户登录认证状态标示
AUTH_FLAG = {"account_name": None, "is_authenticated": False, "is_administrator": False}

# log日志配置设置
LOG_DIR = os.path.join(ATM_DIR, 'logs')
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
        'accounts': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'accounts.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'db.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'auth': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'auth.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'main': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'main.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },

    },
    'loggers': {
        'atm': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'atm.accounts': {
            'handlers': ['accounts'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'atm.auth': {
            'handlers': ['auth'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'atm.db': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'atm.main': {
            'handlers': ['main'],
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
