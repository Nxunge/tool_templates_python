from utils.http_client import  MyHTTPClient
from utils.decorators import skip

#跳过,去除后正常执行
@skip
def run():
    client = MyHTTPClient()
    url = "http://127.0.0.1:13001/test"
    headers = {"Content-Type": "application/json"}
    data = {"title": "foo", "body": "bar", "userId": 1}
    result = client.request("POST", url, headers, data)
    print(result)