#coding=utf-8 
'''
模拟框架程序部分
'''

from socket import * 
import time
from views import * 
from time import sleep

# 全局变量
frame_ip = '127.0.0.1'
frame_port = 8080
frame_addr = (frame_ip,frame_port)

# 静态网页位置
STATIC_DIR = './static' 

# url决定我们能处理什么数据
urls = [
    ('/time',show_time),
    ('/hello',say_hello),
    ('/bye',say_bye)
]

# 应用类　将功能封装在类中
class Application(object):
    def __init__(self):
        # 创建套接字
        self.sockfd = socket()
        # 设置端口重用
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
        # 绑定地址
        self.sockfd.bind(frame_addr)

    # 启动应用程序
    def start(self):
        self.sockfd.listen(5)
        print('listen the port 8080')
        # 等待客户端连接
        ######## 可以改进！！！！！！
        while True:
            connfd,addr = self.sockfd.accept()
            # 接收请求方法
            method = connfd.recv(128).decode()
            # 接收请求内容
            path = connfd.recv(1024).decode()
            print(method,path)
           
            # 处理请求
            self.handle(connfd,method,path)

    def handle(self,connfd,method,path):
        if method == 'GET':
            # 请求静态网页网页信息 
            if path == '/' or path[-5:] =='.html':
                # 获得网页 得到状态和响应体
                status,response_body = self.get_html(path)           
            else:
                # 获得数据
                status,response_body = self.get_data(path)
        elif method == 'POST':
            pass
        # 将结果给httpserver
        connfd.send(status.encode())
        time.sleep(0.1)
        connfd.send(response_body.encode()) 

    # 处理请求网页的请求
    def get_html(self,path):
        if path == '/':
            # 获得主页信息
            get_file = STATIC_DIR + '/index.html'
        else:
            # 其他网页的位置
            get_file = STATIC_DIR + path 

        try:
            # 打开网页的位置
            f = open(get_file)
        except IOError:
            # 没有这个网页的位置
            response = ('404','===Sorry not found the page===')
        else:
            # 打开成功　读取网页文件
            response = ('200',f.read())
        finally:
            return response

    # 处理请求数据
    def get_data(self,path):
        for url,handler in urls: 
            if path == url:
                response_body = handler()
                return '200',response_body
        # 如果没有找到
        return '404','Sorry,Not found the data'


if __name__ == "__main__":
    # 创建对象
    app = Application()
    # 启动框架应用程序 等待request
    app.start() 