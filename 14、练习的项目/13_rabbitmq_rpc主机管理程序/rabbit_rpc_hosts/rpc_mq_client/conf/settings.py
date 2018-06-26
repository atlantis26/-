# coding:utf-8
from logging.config import dictConfig
import os

# RabbitMq队列相关配置
MQ_HOST = "127.0.0.1"
MQ_PORT = 5672
MQ_VIRTUAL_HOST = "/"
MQ_USER = "alex"
MQ_PASSWORD = "123456"
CLIENT_QUEUE = "client_queue_1"

# 支持的多mq server
MQ_QUEUE_DICT = {"127.0.0.1": "server_queue_1",
                 "192.168.2.105": "server_queue_2"
                 }

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 主机组目录，存储主机组信息的相关配置
DB_Task = os.path.join(BASE_DIR, "db", "Task")
if not os.path.exists(DB_Task):
    os.mkdir(DB_Task)

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

        'task': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'task.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'rabbit_mq': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'rabbit_mq.task': {
            'handlers': ['task'],
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
