from array import array
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    timeout_ = int(ReadConfig().get_debug('timeout'))
    url_ = ReadConfig().get_debug('url')
    token = ReadConfig().get_debug('token')
elif env_type == 1: # Release
    timeout_ = int(ReadConfig().get_release('timeout'))
    url_ = ReadConfig().get_release('url')
    token = ReadConfig().get_release('token')


class HttpUtils:

    @staticmethod
    # 请求连接
    def connect_req(email:str):
        url = url_ + '/vault/users/connect-request'
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "email": email
        }
        logger.info('\n'+"<-----Connect Req----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, headers=headers,json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Connect Req Success----->"+"\n\n")
            return res
        else:
            logger.info('\n'+"<-----Connect Req Error----->"+"\n"+(res.text)+"\n\n")
            return res

    @staticmethod
    # 确认连接
    def connect_confirm(email:str, oneTimePassword: str="000000"):
        url = url_ + '/vault/users/connect-confirm'
        headers = {
            "Content-Type": "application/json"
        }
        body = {
            "email": email,
            "oneTimePassword":oneTimePassword
        }
        logger.info('\n'+"<-----Connect Confirm----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, headers=headers,json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Connect Confirm Success----->"+"\n\n")
            return res
        else:
            logger.info('\n'+"<-----Connect Confirm Error----->"+"\n"+(res.text)+"\n\n")
            return res

    @staticmethod
    # 断开连接
    def disconnect(Authorization:str=token):
        url = url_ + '/vault/users/disconnect'
        headers = {
            "Content-Type": "application/json",
            "Authorization":Authorization
        }

        logger.info('\n'+"<-----Disconnect----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.post(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Disconnect Success----->"+"\n\n")
            return res
        else:
            logger.info('\n'+"<-----Disconnect Error----->"+"\n"+(res.text)+"\n\n")
            return res

    @staticmethod
    # 查询账户信息
    def accounts(networkCode:str="", address:str="", type:str="", Authorization=token):
        url = url_ + '/vault/accounts?networkCode=' + networkCode + '&address=' + address + '&type=' + type
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Accounts----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+"\n\n")
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Accounts Response----->"+"\n"+(res.text)+"\n\n")
            return res
        else:
            logger.error('\n'+'<-----Query Accounts Response Error----->'+"\n"+(res.text)+"\n\n")
            raise Exception("请求异常")

    @staticmethod
    # 创建托管账户
    def create_custodial_account(name: str, networkCode: str, Authorization=token):
        url = url_ + '/vault/accounts/custodial'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "name":name,
            "networkCode": networkCode
        }

        logger.info('\n'+"<-----Create Custodial Account------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create Custodial Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Create Custodial Response Error----->'+'\n'+(res.text)+'\n\n')
            return res

    @staticmethod
    # 创建外部账户
    def create_external_account(name: str, networkCode: str, publicKey:list, address:str, Authorization=token):
        url = url_ + '/vault/accounts/custodial'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "name":name,
            "networkCode": networkCode,
            "publicKey":publicKey,
            "address":address
        }

        logger.info('\n'+"<-----Create External Account------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create External Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Create External Response Error----->'+'\n'+(res.text)+'\n\n')
            return res

    @staticmethod
    # 创建安全账户
    def create_safe_account(name: str, networkCode: str, owner: str, recovery:str="" , Authorization=token):
        url = url_ + '/vault/accounts/safe'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "name":name,
            "networkCode": networkCode,
            "owner": owner,
            "recovery": recovery
        }

        logger.info('\n'+"<-----Create Safe Account------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create account Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Create account Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 激活安全账户
    def activation_safe_account(id: str, payer: str='', Authorization=token):
        url = url_ + '/vault/accounts/activations'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "accountId":id,
            "payer": payer
        }

        logger.info('\n'+"<-----Activation Safe Account------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Activation account Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Activation account Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id查询账户
    def account_byid(id:str, Authorization=token):
        url = url_ + "/vault/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Account Byid------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200 or res.status_code == 404:
            logger.info('\n'+"<-----Query Account Byid Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Query Account Byid Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id修改账户
    def update_account_byid(id:str,name:str, Authorization=token):
        url = url_ + "/vault/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "name":name
        }

        logger.info('\n'+"<-----Upadate Account Byid------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.put(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Upadate Account Byid Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Upadate Account Byid Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id删除账户
    def del_account_byid(id:str, Authorization=token):
        url = url_ + "/vault/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Delete Account Byid------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.delete(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Delete Account Byid Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Delete Account Byid Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 操作交易
    def instructions(body:list, Authorization=token):
        url = url_ + "/vault/instructions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Instructions----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Instructions Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Instructions Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res

    @staticmethod
    # 构建交易
    def transactions(body:list, Authorization=token):
        url = url_ + "/vault/transactions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Transactions----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Transactions Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Transactions Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res

    @staticmethod
    # rebuild交易
    def rebuild(id:str, params:list, Authorization=token):
        url = url_ + "/vault/transactions/params"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "id":id,
            "params":params
        }

        logger.info('\n'+"<-----Rebuild----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Rebuild Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Rebuild Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res

    @staticmethod
    # 取消交易
    def cancel(id:str, Authorization=token):
        url = url_ + "/vault/transactions/cancel/" + id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Cancel----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Cancel Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Cancel Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res

    @staticmethod
    # sign
    def sign(id: str, signatures: list, Authorization=token):
        url = url_ + "/vault/transactions/signatures"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "id": id,
            "signatures":signatures
        }
        logger.info('\n'+"<-----Sign----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Sign Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Sign Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # send
    def send(id: str, Authorization=token):
        url = url_ + "/vault/transactions/send/" + id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Send----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')

        res = requests.post(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Send Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Send Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 查询networks信息
    def networks(networkCode:str="", Authorization=token):
        url = url_ + '/vault/networks?networkCode='+networkCode
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        
        logger.info('\n'+"<-----NetWorks----->"+"\n"+"Url:"+url+'\n'+'Headers:'+'\n'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Networks Response----->"+"\n"+(res.text)+'\n\n')
            if len(json.loads(res.text)) > 0:
                return res
            else:
                logger.error('\n'+'<-----Query Networks Response Error----->'+'\n'+(res.text)+'\n\n')
                raise Exception("未查询到任何NetWorks信息!")
        else:
            logger.error('\n'+'<-----Query account Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询所有资产信息
    def assets(symbol:str="", source:str="",isFavorite:str="",limit:str="", Authorization=token):
        url = url_ + "/vault/proxy/core/api/assets?symbol="+symbol+"&source="+source+"&isFavorite="+isFavorite+"&limit="+limit
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        
        logger.info('\n'+"<-----Query Assets----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Assets Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Query Assets Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 查询holders信息
    def holders(networkCode:str='',symbol:str ='',address:str='',Authorization=token):
        url = url_ + '/vault/proxy/assets/holders/?networkCode='+networkCode+'&address='+address+'&symbol='+symbol
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Holders----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Holders Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Query Holders Response Error----->'+'\n'+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    # 刷新holders信息
    def holders_refresh(symbol:str, address:list, Authorization=token):
        url = url_ + '/vault/proxy/core/api/assets/holders'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "symbol":symbol,
            "address":address
        }

        logger.info('\n'+"<-----Refresh Holders Account------>"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n'+'Body:'+json.dumps(body)+'\n\n')
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Refresh Holders Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.error('\n'+'<-----Refresh Holders Response Error----->'+'\n'+(res.text)+'\n\n')
            return res

    @staticmethod
    # 查询alance_transactions记录byhash
    def balance_transactions_byhash(hash:str, Authorization=token):
        url = url_ + '/vault/proxy/core/api/assets/balance-transactions/' + hash
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        logger.info('\n'+"<-----Qurey Transactions by hash----->"+"\n"+"Url:"+url+'\n'+'Headers:'+json.dumps(headers)+'\n\n')

        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey Transactions by hash Response----->"+"\n"+(res.text)+'\n\n')
            return res
        else:
            logger.info('\n'+"<-----Qurey Transactions by hash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text)+'\n\n')
            return res
            raise Exception("请求异常")

    @staticmethod
    def transactions_byid(id:str, Authorization=token):
        url = url_ + '/vault/transactions/' + id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Transactions byid----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Transactions Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Transactions Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询账户staking信息
    def staking(networkCode='',address='',Authorization=token):
        url = url_ + "/vault/proxy/stakes/delegators?address="+address+"&networkCode="+networkCode
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Staking----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Staking Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Staking Response Error----->'+(res.text))
            raise Exception("请求异常")

    # @staticmethod
    # # 查询Swap路由信息
    # def get_swap_route(networkCode:str,from_coin:str,to_coin:str,amount:str,Authorization=token):
    #     url = url_ + '/quote?networkCode=' + networkCode +'&from=' + from_coin +'&to=' + to_coin + '&amount=' + amount
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": Authorization
    #     }

    #     logger.info('\n'+"<-----Swap Route----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
    #     res = requests.get(url=url, headers=headers, timeout=timeout_)
    #     if res.status_code == 200:
    #         logger.info('\n'+"<-----Query Swap Route Response----->"+"\n"+(res.text))
    #         return res
    #     else:
    #         logger.info('\n'+"<-----Query Swap Route Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
    #         return res

    # @staticmethod
    # # Rebuild
    # def get_balance_transactuons(networkCode:str, symbol:str, filter_address="", Authorization=token):
    #     url = "http://18.163.229.203:8888/asset/api/cryptocurrencies/balance-transactions?symbol="+symbol+"&networkCode="+networkCode+"&filter=address:"+filter_address
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": Authorization
    #     }
    #     logger.info('\n'+"<-----Qurey balance transactuons----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))

    #     res = requests.get(url=url,headers=headers,timeout=timeout_)
    #     if res.status_code == 200:
    #         logger.info('\n'+"<-----Qurey balance transactuons----->"+"\n"+(res.text))
    #         return res
    #     else:
    #         logger.info('\n'+"<-----Qurey balance transactuons Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
    #         raise Exception("请求异常")

    # @staticmethod
    # # Rebuild
    # def post_rebuild(txid:str, params:list, Authorization=token):
    #     url = url_ + '/transactions/' + txid + '/rebuild'
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": Authorization
    #     }
    #     body = {
    #        "params":params
    #     }

    #     logger.info('\n'+"<-----Rebuild----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
    #     res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
    #     if res.status_code == 200:
    #         logger.info('\n'+"<-----Rebuild Response----->"+"\n"+(res.text))
    #         res_ = res.json()
    #         r_estimatedFee = res_['estimatedFee']
    #         r_hash = res_['hash']
    #         r_id = res_['id']
    #         r_networkCode = res_['networkCode']
    #         r_requiredSignings = res_['requiredSignings']
    #         r_serialized = res_['serialized']
    #         r_status = res_['status']
    #         return res,r_estimatedFee,r_hash,r_id,r_networkCode,r_requiredSignings,r_serialized,r_status
    #     else:
    #         logger.info('\n'+"<-----Rebuild Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
    #         return res



if __name__ == '__main__':
    # HttpUtils.connect_req("lilongaat@gmail.com")
    # HttpUtils.connect_confirm("r@qq.com")
    # HttpUtils.accounts()
    HttpUtils.networks("CLV")
    # HttpUtils.holders(address="iaa1laewhl28xx9fujqawfnmt4wls2dgyvs6qz7vle")
    # HttpUtils.assets()
    # HttpUtils.holders(address="0x9D055026eB8D83eF561D5D8084F2DD02e7AD2C17")
    # HttpUtils.transactions_byid("1610518001510273025")