import os
import random
from locust import HttpUser, TaskSet, task
import json
from urllib.parse import urlparse

url = "http://alb-re957rez2ynd0kym7f.cn-hongkong.alb.aliyuncs.com"

class Testlocust(TaskSet):

    @task
    def eth_getBlockByNumber(self):
        blocknum = random.randint(1,11142248)
        blockhex = hex(blocknum)
        getBlockByNumber =self.client.post(urlparse(url).path,json={"jsonrpc":"2.0","method":"eth_getBlockByNumber","params": [blockhex,False],"id":1})
        assert getBlockByNumber.status_code == 200
        assert "result" in getBlockByNumber.json()

    @task
    def eth_getBlockByHash(self):
        getBlockByHash = self.client.post(urlparse(url).path,json={"jsonrpc":"2.0","method":"eth_getBlockByHash","params": ["0x4e91c1ee1465e874375c5cca139f0d8958033e36810b5b8f8dbd54a567bc1d70",False],"id":1})
        assert getBlockByHash.status_code == 200
        assert "result" in getBlockByHash.json()

    @task
    def eth_getTransactionReceipt(self):
        getTransactionReceipt = self.client.post(urlparse(url).path,json={"jsonrpc":"2.0","method":"eth_getTransactionReceipt","params": ["0xbbcca29ef186c80ad9307ddf05008049e4a47a7b373c7c0787b1d846b7cf225b"],"id":1})
        assert getTransactionReceipt.status_code == 200
        assert "result" in getTransactionReceipt.json()

    @task
    def eth_call(self):
        call = self.client.post(urlparse(url).path,json={"jsonrpc":"2.0","method":"eth_call","params": [{"from": "0x00192Fb10dF37c9FB26829eb2CC623cd1BF599E8","to": "0xd46e8dd67c5d32be8058bb8eb970870f07244567","gas": "0x76c0","gasPrice": "0x9184e72a000","value": "0x9184e72a","data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"}, "latest"],"id":1})
        assert call.status_code == 200
        assert "result" in call.json()

    @task
    def eth_getBalance(self):
        getBalance = self.client.post(urlparse(url).path,json={"jsonrpc":"2.0","method":"eth_getBalance","params": ["0x2532eC5E562a24E1eeD1E419c8b2713d01bbFA87", "latest"],"id":1})
        assert getBalance.status_code == 200
        assert "result" in getBalance.json()

class WebsiteUser(HttpUser):
    tasks = [Testlocust]
    min_wait = 500
    max_wait = 1500
    host = urlparse(url).scheme + "://" + urlparse(url).netloc


if __name__ == '__main__':
    path = os.path.abspath(__file__)
    os.system('locust -f' + path)