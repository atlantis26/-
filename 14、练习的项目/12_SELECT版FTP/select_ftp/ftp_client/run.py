# coding:utf-8
from core.main import FtpPortal
from conf.settings import init_logging

init_logging()


if __name__ == "__main__":
    client = FtpPortal("localhost", 4396)
    client.console()
