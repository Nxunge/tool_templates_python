import logging
from http.server import  HTTPServer
from utils.http_server import  HTTPServer_JSON_Factory

def run():
    print("_example_httpserver")
    ##解除注释,启动服务
    ##可指定端口,否则采用配置文件
    # server = HTTPServer_JSON_Factory()
    # server.addroutes("/test", test)
    # server.startserver()

    # server = HTTPServer_JSON_Factory(14001)
    # server.addroutes("/test", test)
    # server.startserver()

# 定义具体的处理方法
def test(self, data):
    return {"action": "test", "received": data, "status": "ok"}