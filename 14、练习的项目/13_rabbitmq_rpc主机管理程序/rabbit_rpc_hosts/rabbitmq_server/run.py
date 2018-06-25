# coding:utf-8
from conf.settings import MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD
from conf.settings import init_logging
from core.rpc_server import RpcServer

init_logging()

if __name__ == "__main__":
        server = RpcServer(MQ_HOST, MQ_PORT, MQ_VIRTUAL_HOST, MQ_USER, MQ_PASSWORD)
        server.run()
