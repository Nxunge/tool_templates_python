import json
import logging
from http.server import BaseHTTPRequestHandler,HTTPServer
from urllib.parse import urlparse
from utils.config_manager import config
import threading


post_routes = {}

class HTTPServer_JSON_Factory():
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
        server = HTTPServer((host, self.port), HTTPServer_JSON)
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

class HTTPServer_JSON(BaseHTTPRequestHandler):
    def _send_json(self, data, status=200):
        """统一返回 JSON 响应"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path

        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)

        try:
            data = json.loads(post_data)
            logging.info(f"POST {path} 数据: {data}")
        except json.JSONDecodeError:
            self._send_json({"error": "Invalid JSON"}, status=400)
            return

        # 查找处理函数
        handler = post_routes.get(self.server.server_port).get(path)
        if handler:
            try:
                result = handler(self, data)  # 传递 self 和数据
                self._send_json(result)
            except Exception as e:
                self._send_json({"error": str(e)}, status=500)
        else:
            self._send_json({"error": "Unknown API path"}, status=404)
