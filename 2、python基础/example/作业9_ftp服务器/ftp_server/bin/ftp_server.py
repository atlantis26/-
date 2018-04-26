# coding:utf-8
from core.server_handler import FtpServer

if __name__ == "__main__":

    server = FtpServer("localhost", 4396)
    server.console()
