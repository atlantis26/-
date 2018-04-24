# coding:utf-8
import socket
import os


class FtpServer(object):
    def __init__(self, host_ip, host_port):
        self.host_ip = host_ip
        self.host_port = host_port
        self.server = self.connect()

    def connect(self):
        server = socket.socket()
        server.bind((self.host_ip, self.host_port))
        server.listen(5)
        conn, address = server.accept()

        return

    def receive(self):
        conn, address = server.accept()
        data = conn.recv(1024)

    def send(self):
        data = conn.recv(1024)
        conn.sendall(data)

    def upload(self):
        pass

    def download(self):
        pass

    def close(self):
        pass
