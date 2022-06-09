from loguru import logger
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.readconfig import ReadConfig

headers = {
        "Content-Type":"application/json",
        }

class HttpRpcUtils:
    @staticmethod
    # RPC获取地址余额
    def httprpc_getbalance(node,address,blockhight):
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

        res = requests.post(url=url,json=body,headers=headers)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)

        # 十六进制字符串转换为十进制
        wei_in_dec = int(result['result'],16)

        # wei除以精度
        ethBalance = str(wei_in_dec / (10**18))
        return ethBalance


 

if __name__ == '__main__':
    node = 'eth'
    address = '0xD08B261e83486E88319250890AaC484BA8984632'
    blockhight = 'latest'
    res = HttpRpcUtils.httprpc_getbalance(node,address,blockhight)
    logger.info(res)
