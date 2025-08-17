import logging
from utils.http_server import  MyHTTPServer
from utils.decorators import skip

#跳过,去除后正常执行
@skip
def run():
    print("_example_httpserver")

    ##可指定端口,否则采用配置文件
    server = MyHTTPServer()
    server.addroutes("/test", test)
    server.startserver()

    server = MyHTTPServer(14001)
    server.addroutes("/test/", test)
    server.startserver()

# 定义具体的处理方法
### 如果addroutes时,以/结尾,则extra_path为后续路径
### query为url参数
### data为请求体
def test(self,extra_path,query,data):
    return {"action": "test", "received": data, "status": "ok"}