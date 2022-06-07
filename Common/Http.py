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


        res = requests.post(url=url, data=body, headers=headers)
        print("接口返回结果："+res.text)
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
        print("url:",url)
        print("headers",json.dumps(headers))
        print("parameters",json.dumps(body))

        res = requests.post(url=url,data=body,headers=headers)
        print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    # 查询holders信息
    def http_get_holders():
        url = url_ + '/cryptocurrencies/holders'

        res = requests.get(url=url,headers=headers)
        # print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result

    @staticmethod
    # 查询holders信息by_Authorization
    def http_get_holders_by_web3token(Authorization):
        url = url_ + '/cryptocurrencies/holders'
        headers_ = {
        "Content-Type":"application/json",
        "Authorization":Authorization
        }

        res = requests.get(url=url,headers=headers_)
        # print("接口返回结果："+res.text)
        if res.status_code != 200:
            raise Exception("请求异常")
        result = json.loads(res.text)
        return result

    

if __name__ == '__main__':
    # own = "02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8"
    # device = "435523b0e80c45367577f5c49d661ac0"
    # HttpUtils.http_post_registrations(own,device)
    # HttpUtils.http_get_holders()
    
    networkcode = "ETH"
    symbol = "ETH"
    publickey = "027d4610e7e76f2d4ac82da535c126dea91600d2d6ea5188fd692a7a1c5a3b1d17"
    HttpUtils.http_post_account(networkcode,symbol,publickey)