# coding:utf-8
import os
from logging.config import dictConfig

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 文件存储信息相关配置
DB_Courses = os.path.join(BASE_DIR, "db", "Courses")
DB_Schools = os.path.join(BASE_DIR, "db", "Schools")
DB_Students = os.path.join(BASE_DIR, "db", "Students")
DB_Teachers = os.path.join(BASE_DIR, "db", "Teachers")
if not os.path.exists(DB_Courses):
    os.mkdir(DB_Courses)
if not os.path.exists(DB_Schools):
    os.mkdir(DB_Schools)
if not os.path.exists(DB_Students):
    os.mkdir(DB_Students)
if not os.path.exists(DB_Teachers):
    os.mkdir(DB_Teachers)


# log日志配置设置
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
        'views': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'views.log'),
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
        'course_system': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'course_system.views': {
            'handlers': ['views'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'course_system.auth': {
            'handlers': ['auth'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'course_system.db': {
            'handlers': ['db'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'course_system.main': {
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
