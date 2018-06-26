# coding:utf-8
from core.main import HostManager
from conf.settings import init_logging

init_logging()

if __name__ == "__main__":
    manager = HostManager()
    manager.console()
