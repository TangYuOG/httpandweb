from socket import *
import sys
from threading import Thread
from settings import *

# 创建服务器的类
class Httpserver(object):
    
    def __init__(self,address):
        self.address = address
        # 执行创建套接字方法
        self.create_socket()
        self.bind(address)
    
    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        # 端口重用
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)

    # 绑定端口
    def bind(self,address):
        self.ip = address[0]
        self.port = address[1]
        self.sockfd.bind(address)

    # 启动服务
    def serve_forver(self):
        # 监听
        self.sockfd.listen(5)
        # 循环等待接受客户端请求
        while True:
            connfd,addr = self.sockfd.accept()


if __name__ == '__main__':
    # 创建服务器对象
    httpd = Httpserver(ADDR)
    # 启动服务
    httpd.serve_forver()