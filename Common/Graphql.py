import requests
import json
import os
import sys
sys.path.append(os.path.dirname((os.path.abspath(__file__))))
from loguru import logger
from Httpfs import HttpFs
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))

# btc goerli clv "http://13.212.89.244"
test_url = "http://172.31.32.130"
# BTC DOT CLV ATOM IRIS DOGE LTC 
release_url = "http://18.162.150.113"
# ETH BSC MATIC
release_evm_url = "http://18.166.208.93"

class Url:
    @staticmethod
    def url(netWorkcode):
        if netWorkcode == "ETH":
            url_ = release_evm_url
            prot = "14100"
        elif netWorkcode == "BTC":
            if env_type == 0:
                url_ = test_url
                prot = "4001"
            elif env_type == 1:
                url_ = release_url
                prot = "14000"
        elif netWorkcode == "BSC":
            url_ = release_evm_url
            prot = "14101"
        elif netWorkcode == "DOT":
            url_ = release_url
            prot = "14300"
        elif netWorkcode == "CLV":
            if env_type == 0:
                url_ = test_url
                prot = "4003"
            elif env_type == 1:
                url_ = release_url
                prot = "14301"
        elif netWorkcode == "ATOM":
            url_ = release_url
            prot = "14200"
        elif netWorkcode == "IRIS":
            url_ = release_url
            prot = "14201"
        elif netWorkcode == "DOGE":
            url_ = release_url
            prot = "14003"
        elif netWorkcode == "LTC":
            url_ = release_url
            prot = "14002"
        elif netWorkcode == "MATIC":
            url_ = release_evm_url
            prot = "14102"
        return url_ + ":" + prot

class C(Url):
    @staticmethod
    def call(netWorkcode):
        return Url.url(netWorkcode)

class Graphql(Url):
    @staticmethod
    def getAccountByAddress(netWorkcode:str,address:str,coinId:str):

        url = Url.url(netWorkcode) + "/graphql/"
        payload = json.dumps({
            "query": "query{getAccountByAddress(address:\""+address+"\",coinId:\""+coinId+"\"){blockHash blockNumber address time amount coinId}}"
            })
        headers = {
        'Content-Type': 'application/json'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def getLatestBlock(netWorkcode:str):

        url = Url.url(netWorkcode) + "/graphql/"
        payload = json.dumps({
            "query": "query{getLatestBlock{blockHash blockNumber}}"
            })
        headers = {
        'Content-Type': 'application/json'
        }

        logger.info('\n'+"<-----LatestBlock----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        if response.status_code == 200:
            logger.info('\n'+"<-----LatestBlock response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
            return response
        else:
            HttpFs.send_msg(netWorkcode + " Graphql getLatestBlock 查询失败!")


if __name__ == '__main__':
    # print(Graphql.getAccountByAddress("GOERLI","0xc53ce86d5b3fcf72963df2faa0856a3d9bc7a1ae","goerliETH"))
    print(Graphql.getLatestBlock("ATOM"))