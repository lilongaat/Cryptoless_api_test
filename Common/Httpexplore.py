import requests
from decimal import Decimal
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

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

    print(BTC.balance("34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo").json()["balance"])
