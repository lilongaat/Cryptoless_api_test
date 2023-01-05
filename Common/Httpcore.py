from array import array
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig
from Common import Conf



env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    timeout_ = int(ReadConfig().get_debug('timeout'))
    url_ = ReadConfig().get_debug('url')
    web3token = ReadConfig().get_debug('web3token')

elif env_type == 1: # Release
    timeout_ = int(ReadConfig().get_release('timeout'))
    url_ = ReadConfig().get_release('url')
    web3token = ReadConfig().get_release('web3token')


relay_MATIC = "http://16.163.105.179:18000"


class HttpCoreUtils:

    @staticmethod
    # Network
    def network(networkCode:str="",Authorization=web3token):
        url = url_ + '/networks?networkCode=' + networkCode
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Network List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Network Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Network Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Holders
    def holder(networkCode:str="", symbol:str="",address:str="", Authorization=web3token):
        url = url_ + '/assets/holders?networkCode=' + networkCode + '&symbol=' + symbol + '&address=' + address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Holders List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Holders Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Holders Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # delegators
    def core_delegators(networkCode:str, address:str, Authorization=web3token):
        url = url_ + '/stakes/delegators?networkCode=' + networkCode + '&address=' + address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Delegators List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Delegators Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Delegators Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询账户列表
    def core_account(networkCode:str="", address:str="", Authorization=web3token):
        url = url_ + '/accounts?networkCode=' + networkCode + '&address=' + address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Account List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core account Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 创建账户
    def core_create_account(body:list,Authorization=web3token):
        url = url_ + '/accounts'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Create Account----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'body:'+json.dumps(body))
        res = requests.post(url=url, headers=headers, json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Create account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Create account Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 通过id查询账户
    def core_query_account_byid(id:str, Authorization=web3token):
        url = url_ + "/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Query Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Query Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Query Account Byid Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id删除账户
    def core_del_account_byid(id:str, Authorization=web3token):
        url = url_ + "/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Delete Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.delete(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Delete Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Delete Account Byid Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id批量删除账户
    def core_batchdel_account_byid(ids:array, Authorization=web3token):
        url = url_ + "/accounts"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core BatchDelete Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+json.dumps(ids)+'\n\n')
        res = requests.delete(url=url,headers=headers,json=ids,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core BatchDelete Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core BatchDelete Account Byid Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 激活账户
    def core_active_acc(accountId:str, payer:str="", payType:str="", Authorization=web3token):
        url = url_ + "/accounts/activations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "accountId": 1605140754287775746,
            "payer": "",
            "payType": ""
        }

        logger.info('\n'+"<-----Core Active Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+json.dumps(body)+'\n\n')
        res = requests.post(url=url,headers=headers,json=body,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Active Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Active Account Byid Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # Build交易
    def core_build(body:list, Authorization=web3token):
        url = url_ + "/transactions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Build------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+json.dumps(body)+'\n\n')
        res = requests.post(url=url,headers=headers,json=body,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Build Response---->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Build Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # Transaction交易
    def core_instructions(body:list, Authorization=web3token):
        url = url_ + "/instructions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Instructions------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+json.dumps(body)+'\n\n')
        res = requests.post(url=url,headers=headers,json=body,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Instructions Response---->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Instructions Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # Sign交易
    def core_sign(id:str, signatures:array, Authorization=web3token):
        url = url_ + "/transactions/signatures"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "id":id,
            "signatures":signatures
        }

        logger.info('\n'+"<-----Core Sign------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+json.dumps(body)+'\n\n')
        res = requests.post(url=url,headers=headers,json=body,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Sign Response---->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Sign Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # Send交易
    def core_send(id:str, Authorization=web3token):
        url = url_ + "/transactions/send/" + id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Core Send------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.post(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Core Send Response---->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Core Send Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    #EVM母账户转账nativecoin
    def core_parent_account_transfer_nativecoin(networkCode:str, receiver:str, amount:str = "30000000000000000"):
        M_web3token = "eyJzaWduYXR1cmUiOiIweDJmMjdiYzZlYzhjYjUwM2VmYmRhYWEzMmNjOWRmODc5ZDZlN2M1MTFmYjk3ZTgwYTQxMGM3MWU1ZDY4YzI5ODk2ZDQxMzk5ZmE3Y2E1NjlkOGMxMGU4ZmIwODk5MzI5MmRlZjJlM2ExY2ZmZjhjYjMxODNjYzQ1ZGQ1ZjdjNDFjMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNjczNDUwMDdcbklzc3VlZCBBdDogVGh1LCA4IERlYyAyMDIyIDE0OjQzOjI0IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBNb24sIDggRGVjIDIwNDIgMTQ6NDM6MjQgR01UIn0="
        t = HttpCoreUtils.core_build({
            "networkCode":networkCode,
            "payload":{
                "from":"0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",
                "to":receiver,
                "value":amount
            },
            "type":"TRANSACTION"
        },M_web3token)
        assert t.status_code == 200
        id = t.json()["id"]
        hash = t.json()["requiredSignings"][0]["hash"]
        publickey = t.json()["requiredSignings"][0]["publicKeys"][0]
        signatures = [{
            "hash":hash,
            "publickey":publickey,
            "signature": Conf.Config.sign("9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38",hash)
        }]

        sign = HttpCoreUtils.core_sign(id,signatures,M_web3token)
        assert sign.status_code == 200
        send = HttpCoreUtils.core_send(id,M_web3token)
        assert send.status_code == 200

    @staticmethod
    #EVM母账户转账erc20coin
    def core_parent_account_transfer_erc20coin(networkCode:str, tokenaddress:str, receiver:str, amount:str = "1000"):
        M_web3token = "eyJzaWduYXR1cmUiOiIweDJmMjdiYzZlYzhjYjUwM2VmYmRhYWEzMmNjOWRmODc5ZDZlN2M1MTFmYjk3ZTgwYTQxMGM3MWU1ZDY4YzI5ODk2ZDQxMzk5ZmE3Y2E1NjlkOGMxMGU4ZmIwODk5MzI5MmRlZjJlM2ExY2ZmZjhjYjMxODNjYzQ1ZGQ1ZjdjNDFjMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNjczNDUwMDdcbklzc3VlZCBBdDogVGh1LCA4IERlYyAyMDIyIDE0OjQzOjI0IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBNb24sIDggRGVjIDIwNDIgMTQ6NDM6MjQgR01UIn0="
        t = HttpCoreUtils.core_build({
            "networkCode":networkCode,
            "payload":{
                "from":"0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591",
                "to":receiver,
                "value":amount,
                "tokenaddress":tokenaddress
            },
            "type":"TRANSACTION"
        },M_web3token)
        assert t.status_code == 200
        id = t.json()["id"]
        hash = t.json()["requiredSignings"][0]["hash"]
        publickey = t.json()["requiredSignings"][0]["publicKeys"][0]
        signatures = [{
            "hash":hash,
            "publickey":publickey,
            "signature": Conf.Config.sign("9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38",hash)
        }]

        sign = HttpCoreUtils.core_sign(id,signatures,M_web3token)
        assert sign.status_code == 200
        send = HttpCoreUtils.core_send(id,M_web3token)
        assert send.status_code == 200

    @staticmethod
    # 查询relay手续费
    def relay_estimate(networkCode:str, safeaddress:str, toaddress:str, value:str):
        if networkCode == "MATIC":
            url = relay_MATIC + '/api/v2/safes/' + safeaddress + '/transactions/estimate/'
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "gasToken": "0x0000000000000000000000000000000000000000",
            "operation": "0",
            "safe": safeaddress,
            "to": toaddress,
            "data":"0x",
            "value": value
        }

        logger.info('\n'+"<-----Relay estimate----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Relay estimate Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n' + str(res.status_code) + '\n'+'<-----Relay estimate Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 查询UTXO
    def query_utxo(networkCode:str, address:str):
        if networkCode == "BTC":
            url = "https://api.bitcore.io/api/BTC/testnet/address/" + address + "?unspent=true"
        elif networkCode == "DOGE":
            url = "https://api.bitcore.io/api/DOGE/mainnet/address/" + address + "?unspent=true"
        else:
            logger.error("networkCode not support!")
        headers = {
            "Content-Type": "application/json"
        }

        logger.info('\n'+"<-----Query UTXO----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query UTXO Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n' + str(res.status_code) + '\n'+'<-----Query UTXO Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")


if __name__ == '__main__':
    HttpCoreUtils.network("BTC")
    # HttpCoreUtils.holder(address="tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x")
    # HttpCoreUtils.core_delegators("CLV","5Hdmv7BeAe1XFJXso8oGMidGp186cb4uNTNMywp6fBY7UEsr")
    # HttpCoreUtils.core_account(address="tb1q7ymdm79ryug7vttw4jrf87pdcmn67n3p9rgc5x")
    # HttpCoreUtils.relay_estimate("MATIC","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","0x6490C1b13A4576128159576F9d3acadF79e8dd6f","100")
    # HttpCoreUtils.query_utxo("BTC","tb1qhcuul2fcyv5rvr5mc5cy5saz0q5p3kx0gsy3c0")
    # HttpCoreUtils.core_parent_account_transfer("MATIC","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591")
    # HttpCoreUtils.core_parent_account_transfer_erc20coin("MATIC","0x2791bca1f2de4661ed88a30c99a7a9449aa84174","0x3d7f18Ad2cEa9B59E54dFAf09b327C1CCd899591")