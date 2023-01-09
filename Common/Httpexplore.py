import requests
from decimal import Decimal
from enum import Enum
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Common import Conf
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))


class BTC:
    @staticmethod
    def balance(address:str):
        url = "https://blockchain.coinmarketcap.com/api/address?address="+address+"&symbol=BTC&start=1&limit=10"

        payload={}
        headers = {
        'Cookie': 'next-i18next=en'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    # https://blockchain.coinmarketcap.com/chain/bitcoin 
    # 查询 块信息、价格信息
    def block():
        url = "https://blockchain.coinmarketcap.com/api/blocks?symbol=BTC&start=1&limit=1&quote=true"
        payload={}
        headers = {
        'authority': 'blockchain.coinmarketcap.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182e87f785ea7e-037c0825a51e454-56510c16-2073600-182e87f785fc62%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyZTg3Zjc4NWVhN2UtMDM3YzA4MjVhNTFlNDU0LTU2NTEwYzE2LTIwNzM2MDAtMTgyZTg3Zjc4NWZjNjIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22182e87f785ea7e-037c0825a51e454-56510c16-2073600-182e87f785fc62%22%7D; _ga=GA1.2.1664231870.1661758046; _gid=GA1.2.1193544221.1662016585; _fbp=fb.1.1662016589906.1009730436; _tt_enable_cookie=1; _ttp=6a64d327-d346-4dc6-a7de-3503846df3b9; next-i18next=en; _gat_UA-40475998-1=1; _hjSessionUser_1295813=eyJpZCI6ImZjMzk2OGY1LTVlNzYtNWE4OC04ZGYwLWU5ZTk4Nzk0MWNhMSIsImNyZWF0ZWQiOjE2NjIwMTY2MzkyMjIsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_1295813=eyJpZCI6IjM0Nzk1YjMzLTM5OTEtNDYyMC1hYTJhLWE0YWFiZmJhNmUyNiIsImNyZWF0ZWQiOjE2NjIwMTY2Mzk4NTUsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; intercom-id-h7krdida=edc0dcd2-5893-4b8e-9864-ecec886c9735; intercom-session-h7krdida=; next-i18next=en',
        'referer': 'https://blockchain.coinmarketcap.com/chain/bitcoin',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

class BTC_Test:
    @staticmethod
    # https://mempool.emzy.de/testnet
    def balance(address:str):
        url = "https://mempool.emzy.de/testnet/api/address/" + address

        payload={}
        headers = {
        'authority': 'mempool.emzy.de',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'referer': 'https://mempool.emzy.de/testnet/address/tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

class DOGE:
    @staticmethod
    # https://dogechain.info/api/simple
    def balance(address:str):
        url = "https://dogechain.info/chain/Dogecoin/q/addressbalance/" + address
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    # https://dogechain.info/api/simple
    def block():
        url = "https://dogechain.info/chain/Dogecoin/q/getblockcount"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)

        logger.info('\n'+"<-----block----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----block response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

class ETH:
    @staticmethod
    def balance(address:str):
        url = "https://api.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"
        payload={}
        headers = {}

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    # https://blockchain.coinmarketcap.com/chain/ethereum 
    # 查询 块信息、价格信息
    def block():
        url = "https://blockchain.coinmarketcap.com/api/blocks?symbol=ETH&start=1&limit=50&quote=true"
        payload={}
        headers = {
        'authority': 'blockchain.coinmarketcap.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22182e87f785ea7e-037c0825a51e454-56510c16-2073600-182e87f785fc62%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E8%87%AA%E7%84%B6%E6%90%9C%E7%B4%A2%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC%22%2C%22%24latest_referrer%22%3A%22https%3A%2F%2Fwww.google.com.hk%2F%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTgyZTg3Zjc4NWVhN2UtMDM3YzA4MjVhNTFlNDU0LTU2NTEwYzE2LTIwNzM2MDAtMTgyZTg3Zjc4NWZjNjIifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22182e87f785ea7e-037c0825a51e454-56510c16-2073600-182e87f785fc62%22%7D; _ga=GA1.2.1664231870.1661758046; _gid=GA1.2.1193544221.1662016585; _fbp=fb.1.1662016589906.1009730436; _tt_enable_cookie=1; _ttp=6a64d327-d346-4dc6-a7de-3503846df3b9; next-i18next=en; _gat_UA-40475998-1=1; _hjSessionUser_1295813=eyJpZCI6ImZjMzk2OGY1LTVlNzYtNWE4OC04ZGYwLWU5ZTk4Nzk0MWNhMSIsImNyZWF0ZWQiOjE2NjIwMTY2MzkyMjIsImV4aXN0aW5nIjpmYWxzZX0=; _hjFirstSeen=1; _hjIncludedInSessionSample=0; _hjSession_1295813=eyJpZCI6IjM0Nzk1YjMzLTM5OTEtNDYyMC1hYTJhLWE0YWFiZmJhNmUyNiIsImNyZWF0ZWQiOjE2NjIwMTY2Mzk4NTUsImluU2FtcGxlIjpmYWxzZX0=; _hjIncludedInPageviewSample=1; _hjAbsoluteSessionInProgress=0; intercom-id-h7krdida=edc0dcd2-5893-4b8e-9864-ecec886c9735; intercom-session-h7krdida=; next-i18next=en',
        'referer': 'https://blockchain.coinmarketcap.com/chain/bitcoin',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    @staticmethod
    def block_etherscanapi():
        url = "https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

class GOERLI:
    @staticmethod
    def balance(address:str):
        url = "https://api-goerli.etherscan.io/api?module=account&action=balance&address="+address+"&tag=latest&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"
        payload={}
        headers = {}

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def balance_erc20(address:str, contractaddress:str):
        url = "https://api-goerli.etherscan.io/api?module=account&action=tokenbalance&contractaddress="+contractaddress+"&address="+address+"&tag=latest&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"
        payload={}
        headers = {}

        logger.info('\n'+"<-----balance Erc20----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance Erc20 response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def block():
        url = "https://api-goerli.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

class BSC:
    @staticmethod
    def balance(address:str):
        url = "https://api.bscscan.com/api?module=account&action=balance&address=" + address+ "&apikey=1N55SHXT8U6N3YX8TZK3U8QV7862XDEG2J"
        payload={}
        headers = {}

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def balance_erc20(address:str,contractaddress:str):
        url = "https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress="+contractaddress+"&address="+address+"&tag=latest&apikey=1N55SHXT8U6N3YX8TZK3U8QV7862XDEG2J"
        payload={}
        headers = {}

        logger.info('\n'+"<-----Balance EEC20----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----Balance EEC20 response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    # https://blockchain.coinmarketcap.com/chain/binance-coin
    # 查询 块信息、价格信息
    def block():
        url = "https://api.bscscan.com/api?module=block&action=getblocknobytime&timestamp="+str(Conf.Config.now_timestamp())+"&closest=before&apikey=1N55SHXT8U6N3YX8TZK3U8QV7862XDEG2J"
        payload={}
        headers = {}

        logger.info('\n'+"<-----block----->"+"\n"+"Url:"+url+'\n\n')
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----block response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

class MATIC:
    @staticmethod
    def balance(address:str):
        url = "https://api.polygonscan.com/api?module=account&action=balance&address="+address+"&apikey=85W6B7V5TPH7TDZA3JQCFT8UN8RKAEMA4Y"
        payload={}
        headers = {}

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response  

    @staticmethod
    def balance_erc20(address:str,contractaddress:str):
        url = "https://api.polygonscan.com/api?module=account&action=tokenbalance&contractaddress="+contractaddress+"&address="+address+"&tag=latest&apikey=85W6B7V5TPH7TDZA3JQCFT8UN8RKAEMA4Y"
        payload={}
        headers = {}

        logger.info('\n'+"<-----Balance ERC20----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----Balance ERC20 response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response 

    @staticmethod
    def block():
        url = "https://api.polygonscan.com/api?module=block&action=getblocknobytime&timestamp="+str(Conf.Config.now_timestamp())+"&closest=before&apikey=85W6B7V5TPH7TDZA3JQCFT8UN8RKAEMA4Y"
        payload={}
        headers = {}

        logger.info('\n'+"<-----block----->"+"\n"+"Url:"+url+'\n\n')
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----block response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response     

class ATOM:
    # 网站:https://www.mintscan.io/cosmos/
    @staticmethod
    def assets():
        url = "https://api.mintscan.io/v2/assets/cosmos"
        payload={}
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.mintscan.io',
        'Referer': 'https://www.mintscan.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        logger.info('\n'+"<-----assets----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----assets response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def balance(address:str):
        url = "https://lcd-cosmos.cosmostation.io/cosmos/bank/v1beta1/balances/"+ address+"?pagination.limit=1000"
        payload={}
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.mintscan.io',
        'Referer': 'https://www.mintscan.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def price():
        url = "https://api-utility.cosmostation.io/v1/market/price?id=uatom"

        payload={}
        headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://www.mintscan.io',
        'Referer': 'https://www.mintscan.io/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'cross-site',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"'
        }

        logger.info('\n'+"<-----price----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----price response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def block():
        url = "https://cosmos.lcd.atomscan.com/cosmos/base/tendermint/v1beta1/blocks/latest"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

class IRIS:
    @staticmethod
    def balance(address:str):
        url = "https://proxy.atomscan.com/iris-lcd/cosmos/bank/v1beta1/balances/" + address
        payload={}
        headers = {
        'authority': 'proxy.atomscan.com',
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9',
        'origin': 'https://atomscan.com',
        'referer': 'https://atomscan.com/',
        'sec-ch-ua': '"Not?A_Brand";v="8", "Chromium";v="108", "Google Chrome";v="108"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

    @staticmethod
    def block():
        url = "https://proxy.atomscan.com/iris-lcd/cosmos/base/tendermint/v1beta1/blocks/latest"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        return response

class CLV:
    @staticmethod
    # https://clover.subscan.io/
    def balance(address:str):
        url = "https://clover.webapi.subscan.io/api/scan/account/tokens"
        payload = json.dumps({
        "address": address
        })
        headers = {
        'authority': 'clover.webapi.subscan.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN',
        'baggage': '',
        'content-type': 'application/json',
        'origin': 'https://clover.subscan.io',
        'referer': 'https://clover.subscan.io/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sentry-trace': 'ea3a8691962949979b1cf67d39347ede-99c15b8b0f09a827-0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def block():
        url = "https://clover.webapi.subscan.io/api/v2/scan/blocks"
        payload = "{\"row\":25,\"page\":0}"
        headers = {
        'sentry-trace': '89b2e03907c247be8ac631d7fa25e2e3-9de03032876be9f4-0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Content-Type': 'text/plain'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

class CLV_Test:
    @staticmethod
    # https://clover.subscan.io/
    def balance(address:str):
        url = "https://clover-testnet.webapi.subscan.io/api/scan/account/tokens"
        payload = json.dumps({
        "address": address
        })
        headers = {
        'authority': 'clover.webapi.subscan.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN',
        'baggage': '',
        'content-type': 'application/json',
        'origin': 'https://clover.subscan.io',
        'referer': 'https://clover.subscan.io/',
        'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sentry-trace': 'ea3a8691962949979b1cf67d39347ede-99c15b8b0f09a827-0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

    @staticmethod
    def block():
        url = "https://clover-testnet.webapi.subscan.io/api/v2/scan/blocks"
        payload = "{\"row\":25,\"page\":0}"
        headers = {
        'sentry-trace': '89b2e03907c247be8ac631d7fa25e2e3-9de03032876be9f4-0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36',
        'Content-Type': 'text/plain'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

class DOT:
    @staticmethod
    def block():
        url = "https://polkadot.api.subscan.io/api/scan/blocks"
        payload = json.dumps({
        "row": 1,
        "page": 0
        })
        headers = {
        'Content-Type': 'application/json',
        'X-API-Key': '0a2600579990474e888ffd2b5d932969'
        }

        response = requests.request("POST", url, headers=headers, data=payload)
        return response

    @staticmethod
    def balance(address:str):
        url = "https://polkadot.webapi.subscan.io/api/scan/account/tokens"
        payload = json.dumps({
        "address": address
        })
        headers = {
        'authority': 'polkadot.webapi.subscan.io',
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN',
        'baggage': 'sentry-public_key=da3d374c00b64b6196b5d5861d4d1374,sentry-trace_id=8bf2b9324f364eb2895338cd25bbf1e3,sentry-sample_rate=0.01',
        'content-type': 'application/json',
        'cookie': '_ga_CP7HRJLKYD=GS1.1.1665632649.1.0.1665632651.0.0.0; local_language=zh-CN; _ga_3HWKS4132B=GS1.1.1667806991.6.1.1667807260.0.0.0; _ga_C466PTP61F=GS1.1.1668503324.10.0.1668503324.0.0.0; _gid=GA1.2.1260619428.1669174936; _ga_8WG03ZR03E=GS1.1.1669174939.12.0.1669174941.0.0.0; _ga_1HVHK949MH=GS1.1.1669183047.6.1.1669183400.0.0.0; _gat_UA15256131410=1; _gat_UA1525613147=1; _ga_RLSZTY8RF0=GS1.1.1669183047.20.1.1669183402.0.0.0; _ga=GA1.1.1366628872.1667532296',
        'origin': 'https://polkadot.subscan.io',
        'referer': 'https://polkadot.subscan.io/',
        'sec-ch-ua': '"Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'sentry-trace': '8bf2b9324f364eb2895338cd25bbf1e3-b6ae778e5d1ab4b5-0',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
        }

        logger.info('\n'+"<-----balance----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'payload:'+json.dumps(payload))
        response = requests.request("POST", url, headers=headers, data=payload)
        logger.info('\n'+"<-----balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response

class BN:
    @staticmethod
    def BN_price(symbol:str):
        url = "https://api.binance.com/api/v3/avgPrice?symbol="+symbol+"USDT"
        payload={}
        headers = {}

        response = requests.request("GET", url, headers=headers, data=payload)
        logger.info('\n'+"<-----BN balance response----->"+'\n\n'+'Body:'+json.dumps(response.json()))
        return response


class Balances_explore:
    @staticmethod
    def query(networkCode:str, address:str, symbol="USDC"):
        if networkCode == "BTC":
            if env_type == 0:
                response = BTC_Test.balance(address)
                if response.status_code == 200:
                    balance = (Decimal(response.json()["chain_stats"]["funded_txo_sum"]) - Decimal(response.json()["chain_stats"]["spent_txo_sum"]))/Decimal(10**8)
                else:
                    balance = None
            elif env_type == 1:
                response = BTC.balance(address)
                if response.status_code == 200:
                    balance = (Decimal(response.json()["chain_stats"]["funded_txo_sum"]) - Decimal(response.json()["chain_stats"]["spent_txo_sum"]))/Decimal(10**8)
        elif networkCode == "DOGE":
            response = DOGE.balance(address)
            assert response.status_code == 200
            balance = Decimal(str(response.json()))
        elif networkCode == "ETH":
            pass
        elif networkCode == "GOERLI":
            if symbol == "GoerliETH":
                response = GOERLI.balance(address)
                assert response.status_code == 200
                balance = Decimal(str(response.json()["result"]))/Decimal(10**18)
            else:
                response = GOERLI.balance_erc20(address,"0x1eC2CE6108240118Ff2c66eC8AFAC28618D7e066")
                assert response.status_code == 200
                balance = Decimal(str(response.json()["result"]))/Decimal(10**18)
        elif networkCode == "BSC":
            if symbol == "BNB":
                response = BSC.balance(address)
                assert response.status_code == 200
                balance = Decimal(response.json()["result"])/Decimal(10**18)
            else:
                response = BSC.balance_erc20(address,"0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d")
                assert response.status_code == 200
                balance = Decimal(response.json()["result"])/Decimal(10**18)
        elif networkCode == "MATIC":
            if symbol == "MATIC":
                response = MATIC.balance(address)
                assert response.status_code == 200
                balance = Decimal(response.json()["result"])/Decimal(10**18)
            else:
                response = MATIC.balance_erc20(address,"0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
                assert response.status_code == 200
                balance = Decimal(response.json()["result"])/Decimal(10**6)
        elif networkCode == "ATOM":
            response = ATOM.balance(address)
            assert response.status_code == 200
            balance_ = [b.get("amount") for b in response.json()["balances"] if b.get("denom") == "uatom"]
            balance = (Decimal(int(balance_[0]))/Decimal(10**6))
        elif networkCode == "IRIS":
            response = IRIS.balance(address)
            assert response.status_code == 200
            balance_detail = [b for b in response.json()["balances"] if b.get("denom") == "uiris"][0]
            balance = Decimal(balance_detail["amount"])/Decimal(10**6)
        elif networkCode == "CLV":
            if env_type == 1:
                response = CLV.balance(address)
                assert response.status_code == 200
                balance_detail = [b for b in response.json()["data"]["native"] if b.get("symbol") == "CLV"][0]
                balance = (Decimal(balance_detail["balance"]) - Decimal(balance_detail["lock"]) - Decimal(balance_detail["reserved"]))/Decimal(10**18)
            elif env_type == 0:
                response = CLV_Test.balance(address)
                assert response.status_code == 200
                balance_detail = [b for b in response.json()["data"]["native"] if b.get("symbol") == "CLV"][0]
                balance = (Decimal(balance_detail["balance"]) - Decimal(balance_detail["lock"]) - Decimal(balance_detail["reserved"]))/Decimal(10**18)
        else:
            raise Exception("networkCode No support")
        return balance

class Block_explore:
    @staticmethod
    def block_height():
        pass
    

if __name__ == '__main__':
    # decimal = [a.get("decimal") for a in ATOM.assets().json()["assets"] if a.get("denom") == "uatom"][0]
    # print(decimal)
    # balance = [b.get("amount") for b in ATOM.balance("cosmos1ku5klzmup3an5mxva6u9pr8jmhzrapa7lrtukh").json()["balances"] if b.get("denom") == "uatom"][0]
    # print(int(balance)/(10**decimal))
    # price = [p.get("prices")[0]["current_price"] for p in ATOM.price().json() if p.get("denom") == "uatom"][0]
    # print(price)

    # balance = DOGE.balance("DDogepartyxxxxxxxxxxxxxxxxxxw1dfzr")
    # balance_detail = [b for b in CLV.balance("5H3MSzCTbvwUXfRqfP5QdUKqW7LpTtMQRcH3fU7T566PyQDL").json()["data"]["native"] if b.get("symbol") == "CLV"][0]
    # print(balance_detail)
    # balance = Decimal(balance_detail["balance"]) - Decimal(balance_detail["lock"]) - Decimal(balance_detail["reserved"])
    # print(balance/Decimal(10**18))

    # print(BTC.balance("34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo").json()["balance"])
    # print((ETH.block().json()))
    # print(BN.BN_price("BTC"))
    # MATIC.balance_erc20("0x9b532cf5F662e51ba643672797Ad3eC1A60bb939","0x2791Bca1f2de4661ED88A30C99A7a9449Aa84174")
    # print(IRIS.balance("iaa18j8rds5hqwp88s4qsrytq5w4eafu288cfza9th").json())
    # GOERLI.balance("0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17")
    # print(Balances_explore.query("GOERLI","0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17","GoerliETH"))
    # BTC_Test.balance("tb1qagkvxdz2zq76atvr0rzh8n9lewjmlm25umq0xq")

    # print((Balances_explore.query("CLV","5EwMcCvUPD7RKUTs86NoLPame9oCg8edtdKCdbcsxTFL3aTQ")))

    # print(IRIS.block().json()["block"]["last_commit"]["height"])
    print(int(GOERLI.block().json()["result"],16))
