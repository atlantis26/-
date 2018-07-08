# coding:utf-8
from logging.config import dictConfig
import os.path

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(PROJECT_DIR, 'logs')

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
        'syslog2': {
            'level': 'DEBUG',
            'class': 'logging.handlers.SysLogHandler',
            'facility': 'logging.handlers.SysLogHandler.LOG_LOCAL7',
            'formatter': 'standard',
        },
        'view_handler': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(LOG_DIR, 'view_handler.log'),
            'maxBytes': 1024 * 1024 * 100,
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'system': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False
        },
        'system.view_handler': {
            'handlers': ['view_handler'],
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
