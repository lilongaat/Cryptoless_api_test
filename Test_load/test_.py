import os
import random
import time
from locust import TaskSet, User, task, events
import websockets

events.request_failure.fire()
events.request_success.fire()

class WebSocketClient(object):
 
    def __init__(self, host):
        self.host = host
        self.ws = websockets.WebSocket()
 
    def connect(self, burl):
        start_time = time.time()
        try:
            self.conn = self.ws.connect(url=burl)
        except websockets.WebSocketTimeoutException as e:
            total_time = int((time.time() - start_time) * 1000)
            events.request_failure.fire(request_type="websockt", name='urlweb', response_time=total_time, exception=e)
        else:
            total_time = int((time.time() - start_time) * 1000)
            events.request_success.fire(request_type="websockt", name='urlweb', response_time=total_time, response_length=0)
        return self.conn
 
    def recv(self):
        return self.ws.recv()
 
    def send(self, msg):
        self.ws.send(msg)

class WebsocketLocust(User):
    def __init__(self, *args, **kwargs):
        super(WebsocketLocust, self).__init__(*args, **kwargs)
        self.client = WebSocketClient(self.host)

class SupperDianCan(TaskSet):

    @task
    def eth_getBlockByNumber(self):
        blocknum = random.randint(1,11142248)
        blockhex = hex(blocknum)

        self.url = "wss://eth-mainnet.cryptoless.io"
        self.data = {"jsonrpc":"2.0","method":"eth_getBlockByNumber","params": [blockhex,False],"id":1}
 
        self.client.connect(self.url)
        while True:
            recv = self.client.recv()
            print(recv)
            if eval(recv)['type'] == 'keepalive':
                self.client.send(recv)
            else:
                self.client.send(self.data)

class WebsiteUser(WebsocketLocust):
 
    tasks = [SupperDianCan]
 
    min_wait=5000
 
    max_wait=9000

if __name__ == '__main__':
    path = os.path.abspath(__file__)
    os.system('locust -f' + path)