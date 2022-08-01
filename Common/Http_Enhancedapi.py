import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

# Debug
timeout_ = int(ReadConfig().get_debug('timeout'))
url_ = ReadConfig().get_debug('url_Enhanced_Api')



class HttpUtils:
    @staticmethod
    # Query tokenInfo
    def get_tokenInfo(token_address: str):
        url = url_ + '/v1/tokenInfo?address=' + token_address
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query tokenInfo----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query tokenInfo Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----Query tokenInfo Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query tokenInfo ethplorer
    def get_tokenInfo_ethplorer(token_address: str):
        url = "https://api.ethplorer.io/getTokenInfo/" + token_address + "?apiKey=freekey"
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query tokenInfo----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query tokenInfo Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----Query tokenInfo Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query balance
    def get_balance(address: str,token_address: str, token_id: str):
        url = url_ + '/v1/balance?address=' + address + '&token_address=' + token_address + '&token_id=' + token_id
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query balance Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----Query balance Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query tokenAssets
    def get_tokenAssets(address: str, types: str, limit:str):
        url = url_ + '/v1/tokenAssets?address=' + address + '&types=' + types + '&limit=' + limit
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query tokenAssets----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query tokenAssets Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('"\n"+<-----Query tokenAssets Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query tokenAssets ethplorer
    def get_tokenAssets_ethplorer(address: str):
        url = "https://api.ethplorer.io/getAddressInfo/" + address + "?apiKey=freekey"
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----ethplorer Query tokenAssets----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----ethplorer Query tokenAssets Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----ethplorer Query tokenAssets Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query tokenAssets ERC721&ERC1155
    def get_tokenAssets_erc721erc1155(address: str):
        url = "https://genie-production-api.herokuapp.com/walletAssets?address="+address +"&limit=5000000&offset=0"
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query tokenAssets ERC721&ERC1155----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query tokenAssets ERC721&ERC1155 Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----Query tokenAssets ERC721&ERC1155 Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Query nfts
    def get_nfts(address: str, types: str):
        url = url_ + '/v1/nfts?address=' + address + '&types=' + types
        headers = {
            "Content-Type": "application/json",
        }
        logger.info("\n"+"<-----Query nfts----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query nfts Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error("\n"+'<-----Query nfts Response Error----->'+(res.text))
            raise Exception("请求异常")

if __name__ == '__main__':
    # HttpUtils.get_tokenInfo("0xdac17f958d2ee523a2206206994597c13d831ec7")
    HttpUtils.get_balance("0x0000000000000000000000000000000000000000","0xcB97e65F07DA24D46BcDD078EBebd7C6E6E3d750","")