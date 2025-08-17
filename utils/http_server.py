import json
import logging
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse
from utils.config_manager import config
import threading
from urllib.parse import urlparse, parse_qs


post_routes = {}

class MyHTTPServer():
    port = config.get("port")
    def __init__(self,_port = None):
        if(_port is not None):
            self.port = _port
        if(post_routes.get(self.port) is None):
            post_routes[self.port]={}

    def addroutes(self, path, logic):
        """注册 POST 路由"""
        if path in  post_routes.get(self.port):
            logging.error(f"POST 路径已存在: {path}，忽略添加")
            return
        post_routes.get(self.port)[path] = logic

    def startserver(self):
        """启动 HTTP JSON 服务（新线程）"""
        host = "0.0.0.0"
        server = HTTPServer((host, self.port), MyBaseHTTPRequestHandler)
        def run_server():
            logging.info(f"JSON HTTP 服务已启动: http://{host}:{self.port}")
            try:
                server.serve_forever()
            except KeyboardInterrupt:
                logging.info("\n服务已停止")
            finally:
                server.server_close()
        # 启动后台线程
        thread = threading.Thread(target=run_server, daemon=True)
        thread.start()
        return server, thread

class MyBaseHTTPRequestHandler(BaseHTTPRequestHandler): 
    def _send_json(self, data, status=200): 
        """统一返回 JSON 响应""" 
        self.send_response(status) 
        self.send_header('Content-type', 'application/json') 
        self.end_headers() 
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        query_dict = parse_qs(parsed_path.query)

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            logging.info(f"POST {path} url数据:{query_dict} 数据: {data}")
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return

        # 查找处理函数
        routes = post_routes.get(self.server.server_port, {})
        matched_handler = None
        extra_path = ""

        for route_path, handler in routes.items():
            if route_path.endswith("/"):
                if path.startswith(route_path):
                    matched_handler = handler
                    extra_path = path[len(route_path):]  # 提取路由后面的内容
                    break
            else:
                if path == route_path:
                    matched_handler = handler
                    break

        if matched_handler:
            try:
                result = matched_handler(self, extra_path, query_dict, data)  # 可以传递 extra_path
                self._send_json(result)
            except Exception as e:
                stre = str(e)
                logging.error(stre)
                self._send_json({"error":stre}, status=500)
        else:
            self._send_json({"error": "Unknown API path"}, status=404)

