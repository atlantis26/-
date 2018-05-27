# coding:utf-8
from core.select_server_handler import SelectSocketServer
from conf.settings import init_logging

init_logging()


if __name__ == "__main__":

    server = SelectSocketServer("0.0.0.0", 4396)
    server.run()
