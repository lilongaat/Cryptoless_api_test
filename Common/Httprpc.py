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

timeout = int(ReadConfig().get_debug_rpc('timeout'))
headers = {
        "Content-Type":"application/json",
        }

class HttpRpcEth_Utils:
    @staticmethod
    # RPC eth_accounts
    def eth_accounts(url:str):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_accounts",
            "params": [],
            "id": 1
            }
        logger.info('\n'+"<-----eth_accounts----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_accounts Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_accounts Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_blockNumber
    def eth_blockNumber(url:str):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_blockNumber",
            "params": [],
            "id": 1
            }
        logger.info('\n'+"<-----eth_blockNumber----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_blockNumber Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_blockNumber Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_call
    def eth_call(url:str, pyload:dict,blocknum:str):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_call",
            "params": [
                pyload,
                blocknum
            ],
            "id": 1
            }
        logger.info('\n'+"<-----eth_call----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_call Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_call Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_estimateGas
    def eth_estimateGas(url:str, pyload:dict):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_estimateGas",
            "params": [
                pyload
            ],
            "id": 1
            }
        logger.info('\n'+"<-----eth_estimateGas----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_estimateGas Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_estimateGas Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_chainId
    def eth_chainId(url:str):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_chainId",
            "params": [],
            "id": 1
            }
        logger.info('\n'+"<-----eth_chainId----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_chainId Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_chainId Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_feeHistory
    def eth_feeHistory(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_feeHistory",
                "params": [
                    "0xa",
                    "latest",
                    []
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_feeHistory----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_feeHistory Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_feeHistory Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getBalance
    def eth_getbalance(url:str, address:str, blockhight:str):
        body = {
            "jsonrpc":"2.0",
            "method":"eth_getBalance",
            "params":[
                address, 
                blockhight
                ],
            "id":1
            }
        logger.info('\n'+"<-----eth_getbalance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            # 十六进制字符串转换为十进制
            # wei_in_dec = int(res.json()['result'],16)
            # wei除以精度
            # ethBalance = str(wei_in_dec / (10**18))
            logger.info('\n'+"<-----eth_getbalance Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getbalance Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_gasPrice
    def eth_gasPrice(url:str):
        body = {
            "jsonrpc": "2.0",
            "method": "eth_gasPrice",
            "params": [],
            "id": 1
            }
        logger.info('\n'+"<-----eth_gasPrice----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url,json=body,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_gasPrice Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_gasPrice Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC getBlockByHash
    def eth_getBlockByHash(url:str, BlockHash:str, type: boolean):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getBlockByHash",
                "params": [
                    BlockHash,
                    type
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getBlockByHash----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getBlockByHash Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getBlockByHash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")
            
    @staticmethod
    # RPC getBlockByNumber
    def eth_getBlockByNumber(url:str, BlockNumber:str, type: boolean):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getBlockByNumber",
                "params": [
                    BlockNumber,
                    type
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getBlockByNumber----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getBlockByNumber Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getBlockByNumber Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getBlockTransactionCountByHash
    def eth_getBlockTransactionCountByHash(url:str, BlockHash:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getBlockTransactionCountByHash",
                "params": [
                    BlockHash
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getBlockTransactionCountByHash----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getBlockTransactionCountByHash Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getBlockTransactionCountByHash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getBlockTransactionCountByNumber
    def eth_getBlockTransactionCountByNumber(url:str, BlockNumber:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getBlockTransactionCountByNumber",
                "params": [
                    BlockNumber
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getBlockTransactionCountByNumber----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getBlockTransactionCountByNumber Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getBlockTransactionCountByNumber Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getCode
    def eth_getCode(url:str, address:str, blocknumber:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getCode",
                "params": [
                    address,
                    blocknumber
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getCode----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getCode Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getCode Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getLogs
    def eth_getLogs(url:str, address:str, blockhash:str, topics:list):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getLogs",
                "params": [{
                    "address":address,
                    "blockhash":blockhash,
                    "topics":topics
                    }],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getLogs----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getLogs Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getLogs Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getStorageAt
    def eth_getStorageAt(url:str, address:str, storageposition:str, blocknumber:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getStorageAt",
                "params": [
                    address,
                    storageposition,
                    blocknumber
                    ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getStorageAt----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getStorageAt Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getStorageAt Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getTransactionByBlockHashAndIndex
    def eth_getTransactionByBlockHashAndIndex(url:str, blockhash:str, index:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByBlockHashAndIndex",
                "params": [
                    blockhash,
                    index
                    ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getTransactionByBlockHashAndIndex----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getTransactionByBlockHashAndIndex Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getTransactionByBlockHashAndIndex Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getTransactionByBlockNumberAndIndex
    def eth_getTransactionByBlockNumberAndIndex(url:str, blocknumber:str, index:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByBlockNumberAndIndex",
                "params": [
                    blocknumber,
                    index
                    ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getTransactionByBlockNumberAndIndex----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getTransactionByBlockNumberAndIndex Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getTransactionByBlockNumberAndIndex Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")
    
    @staticmethod
    # RPC eth_getTransactionByHash
    def eth_getTransactionByHash(url:str, hash:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionByHash",
                "params": [
                    hash
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getTransactionByHash----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getTransactionByHash Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getTransactionByHash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getTransactionCount
    def eth_getTransactionCount(url:str, address:str, blocknumber: str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionCount",
                "params": [
                    address,
                    blocknumber
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getTransactionCount----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getTransactionCount Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getTransactionCount Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getTransactionReceipt
    def eth_getTransactionReceipt(url:str, hash:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getTransactionReceipt",
                "params": [
                    hash
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getTransactionReceipt----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getTransactionReceipt Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getTransactionReceipt Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getUncleByBlockHashAndIndex
    def eth_getUncleByBlockHashAndIndex(url:str, blockhash:str, index:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getUncleByBlockHashAndIndex",
                "params": [
                    blockhash,
                    index
                    ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getUncleByBlockHashAndIndex----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getUncleByBlockHashAndIndex Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getUncleByBlockHashAndIndex Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getUncleByBlockNumberAndIndex
    def eth_getUncleByBlockNumberAndIndex(url:str, blocknumber:str, index:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getUncleByBlockNumberAndIndex",
                "params": [
                    blocknumber,
                    index
                    ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getUncleByBlockNumberAndIndex----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getUncleByBlockNumberAndIndex Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getUncleByBlockNumberAndIndex Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getUncleCountByBlockHash
    def eth_getUncleCountByBlockHash(url:str, BlockHash:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getUncleCountByBlockHash",
                "params": [
                    BlockHash
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getUncleCountByBlockHash----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getUncleCountByBlockHash Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getUncleCountByBlockHash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getUncleCountByBlockNumber
    def eth_getUncleCountByBlockNumber(url:str, BlockNumber:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getUncleCountByBlockNumber",
                "params": [
                    BlockNumber
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getUncleCountByBlockNumber----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getUncleCountByBlockNumber Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getUncleCountByBlockNumber Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_getWork
    def eth_getWork(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_getWork",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----eth_getWork----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_getWork Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_getWork Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_mining
    def eth_mining(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_mining",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----eth_mining----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_mining Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_mining Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_hashrate
    def eth_hashrate(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_hashrate",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----eth_hashrate----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_hashrate Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_hashrate Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_protocolVersion
    def eth_protocolVersion(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_protocolVersion",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----eth_protocolVersion----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_protocolVersion Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_protocolVersion Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_sendRawTransaction
    def eth_sendRawTransaction(url:str,rawtx:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_sendRawTransaction",
                "params": [rawtx],
                "id": 1
            }
        logger.info('\n'+"<-----eth_sendRawTransaction----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_sendRawTransaction Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_sendRawTransaction Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_submitWork
    def eth_submitWork(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_submitWork",
                "params": [
                    "0x0000000000000001",
                    "0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef",
                    "0xD1FE5700000000000000000000000000D1FE5700000000000000000000000000"
                ],
                "id": 1
            }
        logger.info('\n'+"<-----eth_submitWork----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_submitWork Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_submitWork Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC eth_syncing
    def eth_syncing(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "eth_syncing",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----eth_syncing----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----eth_syncing Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----eth_syncing Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC net_listening
    def net_listening(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "net_listening",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----net_listening----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----net_listening Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----net_listening Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC net_peerCount
    def net_peerCount(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "net_peerCount",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----net_peerCount----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----net_peerCount Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----net_peerCount Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC net_version
    def net_version(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "net_version",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----net_version----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----net_version Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----net_version Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC parity_nextNonce
    def parity_nextNonce(url:str, address:str):
        body = {
                "jsonrpc": "2.0",
                "method": "parity_nextNonce",
                "params": [
                    address
                ],
                "id": 1
            }
        logger.info('\n'+"<-----parity_nextNonce----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----parity_nextNonce Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----parity_nextNonce Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # RPC web3_clientVersion
    def web3_clientVersion(url:str):
        body = {
                "jsonrpc": "2.0",
                "method": "web3_clientVersion",
                "params": [],
                "id": 1
            }
        logger.info('\n'+"<-----web3_clientVersion----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url,json=body,headers=headers,timeout=timeout)
        if res.status_code == 200:
            logger.info('\n'+"<-----web3_clientVersion Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----web3_clientVersion Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")
 

if __name__ == '__main__':
    url = 'https://rinkeby.infura.io/v3/f8167b1c15ae4716976dd317d03b3e7f'
    print(HttpRpcEth_Utils.eth_accounts(url)[1])
    # print(HttpRpcEth_Utils.eth_blockNumber(url)[1])
    # print(HttpRpcEth_Utils.eth_chainId(url)[1])
    # print(HttpRpcEth_Utils.eth_gasPrice(url)[1])

