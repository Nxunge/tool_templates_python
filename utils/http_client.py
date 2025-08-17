import requests
import logging

class MyHTTPClient:
    def __init__(self):
        pass

    def request(self, method: str, url: str, headers: dict = None, data: dict = None) -> dict:
        """
        发送 HTTP 请求

        :param method: 请求方法 "GET" 或 "POST"
        :param url: 请求 URL
        :param headers: 请求头字典
        :param data: 请求数据字典（会作为 JSON 发送）
        :return: 响应 JSON 字典
        """
        method = method.upper()
        try:
            if method == "GET":
                response = requests.get(url, headers=headers, params=data)
            elif method == "POST":
                response = requests.post(url, headers=headers, json=data)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")
            # 尝试解析 JSON
            return response.json()
        except requests.RequestException as e:
            logging.error(f"HTTP 请求失败: {url} \n {e}")
            return {}
        except ValueError as e:
            logging.error(f"解析 JSON 失败: {e}")
            return {}
