from loguru import logger
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.readconfig import ReadConfig

url_ = ReadConfig().get_debug('url')
Authorization = ReadConfig().get_debug('Authorization')
headers = {
        "Content-Type":"application/json",
        "Authorization":Authorization
        }

class HttpUtils:
    @staticmethod
    # 注册token
    def http_post_registrations(ownerPublicKey,deviceToken):
        url = url_ + '/registrations'
        body = {
            "ownerPublicKey":ownerPublicKey,
            "deviceToken":deviceToken
            }

        print("url:",url)
        print("headers",json.dumps(headers))
        print("parameters",json.dumps(body))


        res = requests.post(url=url, json=body, headers=headers)
        print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    # 查询账户信息
    def http_get_account():
        url = url_ +'/accounts'

        res = requests.get(url=url,headers=headers)
        # print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result


    @staticmethod
    # 创建账户
    def http_post_account(networkcode,symbol,publickey):
        url = url_ + '/networks/'+ symbol +'/accounts'
        body  = {
            "networkCode": networkcode,
            "publicKeys": [
                publickey
    ],
    "threshold": 1
}

        res = requests.post(url=url,json=body,headers=headers)
        logger.info("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    # 查询networks信息
    def http_get_networks():
        url = url_ + '/networks'

        res = requests.get(url=url,headers=headers)
        # print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        if len(result) > 0:
            return result
        else:
            logger.info("没有查询到任何NetWorks信息！")
            logger.info(result)


    @staticmethod
    # 查询holders信息
    def http_get_holders():
        url = url_ + '/cryptocurrencies/holders'

        res = requests.get(url=url,headers=headers)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        if len(result) > 0:
            return result
        else:
            logger.info("没有查询到用户任何Balances信息！")
            logger.info(result)

        

    @staticmethod
    # 查询holders信息by_Authorization
    def http_get_holders_by_web3token(Authorization):
        url = url_ + '/cryptocurrencies/holders'
        headers_ = {
        "Content-Type":"application/json",
        "Authorization":Authorization
        }

        res = requests.get(url=url,headers=headers_)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        if len(result) > 0:
            return result
        else:
            logger.info("没有查询到用户任何资产信息！")
            logger.info(result)

    

if __name__ == '__main__':
    # own = "02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8"
    # device = "435523b0e80c45367577f5c49d661ac0"
    # HttpUtils.http_post_registrations(own,device)

    # 没有资产
    Authorization = 'eyJzaWduYXR1cmUiOiIweDEzMDZjNGRlMzhjNTE2ZTg0ZDkyMmRjMWJjZjcyNGE5MjgxMGI5MjM3NTdhZDBiZDdjZGEzNzRiMGEyOGExMTg1Njk5MDliZTQ5NDMwNzcyZjgzNzI5M2U1MjU5ZGRlNDk1ZWJiMzViNzgzOTAwYzU2MTkxNWI2OGU1ZTY0MWQ1MWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogOTExMzczNDNcbklzc3VlZCBBdDogV2VkLCA4IEp1biAyMDIyIDEwOjIyOjA5IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBTdW4sIDggSnVuIDIwNDIgMTA6MjI6MDkgR01UIn0='
    res = HttpUtils.http_get_holders_by_web3token(Authorization)
    logger.info(res)
    
    # networkcode = "ETH"
    # symbol = "ETH"
    # publickey = "027d4610e7e76f2d4ac82da535c126dea91600d2d6ea5188fd692a7a1c5a3b1d17"
    # HttpUtils.http_post_account(networkcode,symbol,publickey)

    # res = HttpUtils.http_get_networks()
    # logger.info(res[0]['code'])
