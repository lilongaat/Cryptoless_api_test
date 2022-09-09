import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger

url_ = "http://18.162.150.113"

class Graphql:
    @staticmethod
    def getAccountByAddress(netWorkcode:str,address:str,coinId:str):

        if netWorkcode == "ETH":prot = "14100"
        elif netWorkcode == "BTC":prot = "14000"
        elif netWorkcode == "BSC":prot = "14101"
        elif netWorkcode == "DOT":prot = "14300"
        elif netWorkcode == "CLV":prot = "14301"
        elif netWorkcode == "ATOM":prot = "14200"
        elif netWorkcode == "IRIS":prot = "14201"
        elif netWorkcode == "DOGE":prot = "14003"
        elif netWorkcode == "LTC":prot = "14002"
        elif netWorkcode == "MATIC":prot = "14102"

        url = url_ + ":" + prot+ "/graphql/"
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


if __name__ == '__main__':
    print(float(Graphql.getAccountByAddress("cosmos1nm0rrq86ucezaf8uj35pq9fpwr5r82cl8sc7p5","ATOM").json()["data"]["getAccountByAddress"]["amount"]))