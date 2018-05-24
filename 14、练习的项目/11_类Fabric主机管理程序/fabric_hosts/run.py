# coding:utf-8
from core.main import Fabric
from conf.settings import init_logging

init_logging()

if __name__ == "__main__":
    Fabric.console()
