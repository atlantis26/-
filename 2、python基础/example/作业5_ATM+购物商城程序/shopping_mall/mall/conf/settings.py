# coding:utf-8
import os
from logging.config import dictConfig

# 项目根目录
MALL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ATM系统管理员账号
ATM_ADMIN = {"account_name": "admin", "password": "admin"}

# 数据库设置
DB_TYPE = "FileStorage"  # 当前只支持文件存储信息方式，可扩展，留有接入MySQL等数据库的可能

# 文件存储信息相关配置
DB_Products = os.path.join(MALL_DIR, "db", "products", "products.txt")
DB_Flows_History = os.path.join(MALL_DIR, "db", "flows_history")
if not os.path.exists(DB_Products):
    raise Exception(u"找不到商品列表信息，请联系管理员")
if not os.path.exists(DB_Flows_History):
    os.mkdir(DB_Flows_History)


# # MySQL或其他关系数据库的相关配置
# DB_HOST = ""
# DB_PORT = ""
# DB_USER = ""
# DB_PASSWORD = ""


# log日志配置设置
LOG_DIR = os.path.join(MALL_DIR, 'logs')
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
        'db': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'db.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
        'products': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'products.log'),
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
        'mall': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'mall.db': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mall.products': {
            'handlers': ['products'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mall.main': {
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
