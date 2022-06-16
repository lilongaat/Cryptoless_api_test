import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

# Debug
timeout = int(ReadConfig().get_debug('timeout'))
url_ = ReadConfig().get_debug('url')
Authorization_ = ReadConfig().get_debug('Authorization')

# Release
# timeout = int(ReadConfig().get_release('timeout'))
# url_ = ReadConfig().get_release('url')
# Authorization_ = ReadConfig().get_release('Authorization')


class HttpUtils:
    @staticmethod
    # 注册web3token
    def post_registrations(Authorization, ownerPublicKey, deviceToken):
        url = url_ + '/registrations'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "ownerPublicKey": ownerPublicKey,
            "deviceToken": deviceToken
        }

        logger.info("<-----Register----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers)+'\n\n'+'Body:'+str(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('registrations 失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            return result

    @staticmethod
    # 查询账户信息
    def get_account(Authorization=Authorization_):
        url = url_ + '/accounts'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info("<-----Account----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers))
        res = requests.get(url=url, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('Account 查询失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            return result

    @staticmethod
    # 创建账户
    def post_account(networkcode: str, symbol: str, publickeys: list, threshold=1, Authorization=Authorization_):
        url = url_ + '/networks/' + symbol + '/accounts'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "networkCode": networkcode,
            "publicKeys": publickeys,
            "threshold": threshold
        }

        logger.info("<-----Account-Create----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers)+'\n\n'+'Body:'+str(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('Account 创建失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            return result

    @staticmethod
    # 查询networks信息
    def get_networks(Authorization=Authorization_):
        url = url_ + '/networks'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        
        logger.info("<-----NetWorks----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers))
        res = requests.get(url=url, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('Networks 查询失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            if len(result) > 0:
                return result
            else:
                logger.info("没有查询到任何NetWorks信息！")
                logger.info(result)

    @staticmethod
    # 查询holders信息
    def get_holders(Authorization=Authorization_, address=''):
        url = url_ + '/cryptocurrencies/holders?address='+address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info("<-----Holders----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers))
        res = requests.get(url=url, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('Holsers 查询失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            if len(result) > 0:
                return result
            else:
                logger.info("没有查询到用户任何Balances信息！")
                logger.info(result)

    # transfers
    def post_transfers(networkCode: str, symbol: str, definiteSignerPublicKeys: list, from_add: str, to_add: str, amount: str, Authorization=Authorization_):
        url = url_ + '/cryptocurrencies/'+symbol+'/transfers'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "amount": amount,
            "definiteSignerPublicKeys": definiteSignerPublicKeys,
            "from": from_add,
            "networkCode": networkCode,
            "to": to_add
        }

        logger.info("<-----Transfers----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers)+'\n\n'+'Body:'+str(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error('transfers 交易失败！')
            logger.error(json.dumps(body))
            # logger.error('Response | '+res.text)
            raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            r_estimatedFee = result['_embedded']['transactions'][0]['estimatedFee']
            r_hash = result['_embedded']['transactions'][0]['hash']
            r_id = result['_embedded']['transactions'][0]['id']
            r_networkCode = result['_embedded']['transactions'][0]['networkCode']
            r_requiredSignings = result['_embedded']['transactions'][0]['requiredSignings']
            r_serialized = result['_embedded']['transactions'][0]['serialized']
            r_status = result['_embedded']['transactions'][0]['status']
            ID = result['id']
            r_updatedTime = result['_embedded']['transactions'][0]['updatedTime']

            return result,r_estimatedFee,r_hash,r_id,r_networkCode,r_requiredSignings,r_serialized,r_status,ID,r_updatedTime

    # sign
    def post_sign_transfers(transactions_estimatedFee: str, transactions_hash: str, transactions_id: str, transactions_networkCode: str, transactions_requiredSignings: list, transactions_serialized: str, signatures: list, status='BUILDING', Authorization=Authorization_):
        url = url_ + '/transactions/'+transactions_id+'/sign'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "estimatedFee": transactions_estimatedFee,
            "hash": transactions_hash,
            "id": transactions_id,
            "networkCode": transactions_networkCode,
            "requiredSignings": transactions_requiredSignings,
            "serialized": transactions_serialized,
            "signatures": signatures,
            "status": status
        }

        logger.info("<-----Sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers)+'\n\n'+'Body:'+str(body))
        try:
            res = requests.post(url=url, json=body, headers=headers, timeout=10)
        except TimeoutError as e:
            logger.info("<-----Sign timeout----->")
        if res.status_code != 200:
            logger.error('Sign 签名失败！')
            logger.error('<-----Sign Response----->'+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            return result

    # send
    def post_send_transfers(transactions_id:str,Authorization=Authorization_):
        url = url_ + '/transactions/' + transactions_id + '/send'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info("<-----Send----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+str(headers))
        res = requests.post(url=url, headers=headers, timeout=10)
        if res.status_code != 200:
            logger.error(json.loads(res.text))
            logger.error('Send 交易失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            result = json.loads(res.text)
            return result

if __name__ == '__main__':
    # HttpUtils.post_send_transfers('1535216278276812802')
    Authorization = ''
    ownerPublicKey = '0x0388924a9fedf683cb9c6aec801d19afae932f767e21df4ea91cd282fa06295795'
    deviceToken = '0x0388924a9fedf683cb9c6aec801d19afae932f767e21df4ea91cd282fa06295795'
    print(HttpUtils.post_registrations(Authorization,ownerPublicKey,deviceToken))