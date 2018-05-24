# coding:utf-8
from socketserver import ThreadingTCPServer
from core.request_handler import FtpHandler

import logging

logger = logging.getLogger("ftp.ftp_server")


class FtpServer(object):
    def __init__(self, host, port):
        self.server = ThreadingTCPServer((host, port), FtpHandler)

    def run(self):
        self.server.serve_forever()


