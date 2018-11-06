#coding=utf-8 
'''
name : Levi
time : 2018-10-1
httpserver v3.0
'''
from socket import *
import sys 
import re
from threading import Thread 
# 为了获取ADDR等配置信息
from setting import *
# 防止粘包
import time 

# 和WebFrame通信
def connect_frame(METHOD,PATH):
    s = socket()
    # 防止连接不上
    try:
        # 连接框架服务器地址 从模块中导入
        s.connect(frame_addr)
    except Exception as e:
        print('Connect erro',e)
        return
    s.send(METHOD.encode())
    time.sleep(0.1)
    s.send(PATH.encode())
    # 接受web的响应
    status = s.recv(128).decode()
    response_body = s.recv(4096 * 10).decode()
    if not (status or response_body):
        status =  '404'
        response_body = 'sorry' 
    s.close()
    return status,response_body
        
        
# 封装httpserver类
class HTTPServer(object):
    def __init__(self,addr):
        self.addr = addr
        # 执行创建套接字方法
        self.create_socket()
        self.bind(addr) 

    # 创建套接字
    def create_socket(self):
        self.sockfd = socket()
        # 端口重用
        self.sockfd.setsockopt(SOL_SOCKET,
                SO_REUSEADDR,1) 

    # 绑定地址
    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    # HTTP服务器启动
    def serve_forever(self):
        # 监听
        self.sockfd.listen(10)
        print("Listen the port %d..." % self.port)
        # 循环等待客户端的连接
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from",addr)
            # 处理客户端请求
            # 创建线程 执行handle_request
            handle_client = Thread\
            (target = self.handle_request,args = (connfd,))
            # 子线程随主线程的退出而退出
            handle_client.setDaemon(True)
            # 开始线程
            handle_client.start()

    # 处理客户端请求
    def handle_request(self,connfd):
        # 接收浏览器发来的http请求
        request = connfd.recv(4096)
        # print(request)
        # 如果请求为空　就结束了
        if not request:
            connfd.close()
            return
        # 按行进行切割
        request_lines = request.splitlines()
        # 获取请求行
        request_line = request_lines[0].decode('utf-8')
        # request_line = request_lines[0]
        # 打印请求行
        print(request_line)
        # 正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            # 得到的是字典
            env = re.match(pattern,request_line).groupdict()
            print(env)
        except:
            # 没有匹配到的情况下
            # 给客户端响应　一定要按照响应格式
            response_headlers = "HTTP/1.1 500 Server Error\r\n"
            response_headlers += '\r\n'
            response_body = "Server Error"
            response = response_handlers + response_body
            connfd.send(response.encode())
            connfd.close()
            return
        
        # 将请求发给frame得到返回数据结果
        # 使字典的键对应的返回形参
        status,response_body = connect_frame(**env)
        # 根据响应码组织响应头内容
        response_headlers = self.get_headlers(status)

        # 将结果组织为http response 发送给客户端
        response = response_headlers + response_body
        connfd.send(response.encode())
        connfd.close()

    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'

        return response_headlers

if __name__ == "__main__":
    # 生成服务器类对象 地址ADDR让用户自己去配置
    # ADDR从配置文件中进行配置,从setting导入即可获得ADDR
    httpd = HTTPServer(ADDR)
    # 启动http服务
    httpd.serve_forever()

