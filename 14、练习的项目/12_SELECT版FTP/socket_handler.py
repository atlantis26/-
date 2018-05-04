# coding:utf-8
import socket
import select
import queue


class SelectSocketServer(object):
    def __init__(self, host, port):
        self.server = socket.socket()
        self.server.bind((host, port))
        self.server.setblocking(False)

    def _init_select(self):
        inputs = list()
        outputs = list()
