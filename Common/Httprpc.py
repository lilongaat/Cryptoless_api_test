from socket import timeout
from time import sleep
from xmlrpc.client import boolean
from loguru import logger
import requests
import json
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.readconfig import ReadConfig
from Httpfs import HttpFs

timeout = int(ReadConfig().get_debug_rpc('timeout'))
headers = {
        "Content-Type":"application/json",
        }

class HttpRpcUtils:
    @staticmethod
    # RPC获取地址余额
    def Eth_getBlockByNumber(node:str,block:str,status:boolean):
        url = ReadConfig().get_debug_rpc(node)
        body = {
    "jsonrpc":"2.0",
    "method":"eth_getBlockByNumber",
    "params":[
        "0x1b4",
        "true"
    ],
    "id":1
}


    @staticmethod
    # RPC获取地址余额
    def Eth_getbalance(node:str,address:str,blockhight:str):
        url = ReadConfig().get_debug_rpc(node)
        body = {
            "jsonrpc":"2.0",
            "method":"eth_getBalance",
            "params":[
                address, 
                blockhight
                ],
            "id":1
            }

        try:
            res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        except TimeoutError as e:
            logger.error(e)

        if res.status_code != 200:
            raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            # 十六进制字符串转换为十进制
            wei_in_dec = int(result['result'],16)
            # wei除以精度
            ethBalance = str(wei_in_dec / (10**18))
            return ethBalance


 

if __name__ == '__main__':
    node = 'eth'
    address = '0x44d9Ea428C4C1D097947A683439a60105281AAD7'
    blockhight = 'latest'
    res = HttpRpcUtils.Eth_getbalance(node,address,blockhight)
    logger.info(res)

