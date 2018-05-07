# coding:utf-8
from core.server_handler import FtpServer
from conf.settings import init_logging

init_logging()


if __name__ == "__main__":

    server = FtpServer("0.0.0.0", 4396)
    server.run()
