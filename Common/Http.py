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
    web3token = ReadConfig().get_debug('web3token')

elif env_type == 1: # Release
    timeout_ = int(ReadConfig().get_release('timeout'))
    url_ = ReadConfig().get_release('url')
    token = ReadConfig().get_release('token')
    web3token = ReadConfig().get_release('web3token')


class HttpUtils:

    @staticmethod
    # 查询账户信息
    def get_account(address="",Authorization=web3token):
        url = url_ + '/accounts?address=' + address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Account----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query account Response Error----->'+(res.text))
            raise Exception("请求异常")

    # @staticmethod
    # # 创建账户
    # def post_create_account(body:list,Authorization=token):
    #     url = url_ + '/accounts/save'
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": Authorization
    #     }

    #     logger.info('\n'+"<-----Create Account----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'body:'+json.dumps(body))
    #     res = requests.post(url=url, headers=headers, json=body, timeout=timeout_)
    #     if res.status_code == 200:
    #         logger.info('\n'+"<-----Create account Response----->"+"\n"+(res.text))
    #         return res
    #     else:
    #         logger.error('\n'+'<-----Create account Error----->'+(res.text))
    #         raise Exception("请求异常")

    @staticmethod
    # 查询代理账户列表
    def get_safe_agents(Authorization=web3token):
        url = 'http://13.215.207.236:8888/context/api/safe/agents'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Safe Agents----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Safe Agents Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Safe Agents Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 代理账户签名交易
    def post_safe_agents_sign(networkCode:str,hash:str,Authorization=web3token):
        url = 'http://13.215.207.236:8888/context/api/safe/txs'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "networkCode":networkCode,
            "hash":hash
        }

        logger.info('\n'+"<-----Safe Agents sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, headers=headers,json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Safe Agents sign Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Safe Agents sign Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 激活账户
    def post_safe_activation(accountId:str,Authorization=web3token):
        url = 'http://13.215.207.236:8888/context/api/safe/activations'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "accountId": accountId
        }

        logger.info('\n'+"<-----Safe Account activation----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Safe Account activation Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n' + str(res.status_code) + '\n'+'<-----Safe Account activation Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 查询激活账户交易及状态
    def get_safe_activation(accountId:str,Authorization=web3token):
        url = 'http://13.215.207.236:8888/context/api/safe/activations?accountId=' + accountId
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Safe Account activation----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Safe Account activation Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n' + str(res.status_code) + '\n'+'<-----Query Safe Account activation Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 创建账户
    def post_create_account(networkcode: str, publickeys: list, threshold =1, address = "", Authorization=web3token):
        url = url_ + '/accounts/save'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "networkCode": networkcode,
            "publicKeys": publickeys,
            "threshold": threshold,
            "address":address
        }

        logger.info('\n'+"<-----Account-Create----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Create account Response Error----->'+(res.text))
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

        logger.info('\n'+"<-----Create custodial Account------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create custodial Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Create custodial Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 创建安全账户
    def create_safe_account(name: str, networkCode: str, owner: str, recovery:str , Authorization=token):
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

        logger.info('\n'+"<-----Create Safe Account------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Create account Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 激活安全账户
    def activation_safe_account(id: str, payer: str, Authorization=token):
        url = url_ + '/vault/accounts/activations'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "accountId":id,
            "payer": payer
        }

        logger.info('\n'+"<-----Activation Safe Account------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Activation account Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Activation account Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 查询账户列表
    def get_account_list(networkCode='', address='',  type='', Authorization=token):
        url = url_ + '/vault/accounts?networkCode='+networkCode+'&address='+address+'&type='+type
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Account List------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Account List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Account List Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 通过id查询账户
    def get_account_byid(id:str, Authorization=token):
        url = url_ + "/vault/accounts/"+id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Query Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200 or res.status_code == 404:
            logger.info('\n'+"<-----Query Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Account Byid Response Error----->'+(res.text))
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

        logger.info('\n'+"<-----Upadate Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.put(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Upadate Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Upadate Account Byid Response Error----->'+(res.text))
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

        logger.info('\n'+"<-----Delete Account Byid------>"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')
        res = requests.delete(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Delete Account Byid Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Delete Account Byid Response Error----->'+(res.text))
            return res
            raise Exception("请求异常")


    @staticmethod
    # 查询networks信息
    def get_networks(Authorization=web3token):
        url = url_ + '/networks'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        
        logger.info('\n'+"<-----NetWorks----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query account Response----->"+"\n"+(res.text))
            if len(json.loads(res.text)) > 0:
                return res
            else:
                logger.error('\n'+'<-----Query Networks Response Error----->'+(res.text))
                raise Exception("没有查询到任何NetWorks信息!")
        else:
            logger.error('\n'+'<-----Query account Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询所有资产信息
    def get_cryptocurrencies(symbol="", source="",isFavorite="",limit="10000", Authorization=web3token):
        url = url_ + "/cryptocurrencies?symbol="+symbol+"&source="+source+"&isFavorite="+isFavorite+"&limit="+limit
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        
        logger.info('\n'+"<-----Cryptocurrencies----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Cryptocurrencies Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query account Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询holders信息
    def get_holders(Network='',symbol ='',address='',Authorization=web3token):
        url = url_ + '/cryptocurrencies/holders?address='+address+'&networkCode='+Network+'&symbol='+symbol
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Holders----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Holders Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Holders Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询账户staking信息
    def get_staking(Network='',symbol ='',address='',Authorization=web3token):
        url = url_ + '/staking/delegators?networkCode='+Network+'&symbol='+symbol
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Staking----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Staking Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+'<-----Query Staking Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询Swap路由信息
    def get_swap_route(networkCode:str,from_coin:str,to_coin:str,amount:str,Authorization=web3token):
        url = url_ + '/quote?networkCode=' + networkCode +'&from=' + from_coin +'&to=' + to_coin + '&amount=' + amount
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Swap Route----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Swap Route Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Query Swap Route Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res

    @staticmethod
    #  instructions (type: Transfer/CrossChainTransfer/SwapTransfer)
    def post_instructions(type: str,body: list, networkCode: str, definiteSignerPublicKeys: list, transactionParams = '', Authorization=web3token):
        url = url_ + '/instructions'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body_ = {
            "body": body,
            "networkCode": networkCode,
            "type": type,
            "definiteSignerPublicKeys": definiteSignerPublicKeys,
            "transactionParams": transactionParams
        }

        logger.info('\n'+"<-----Instructions----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body_))
        res = requests.post(url=url, json=body_, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Instructions Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Instructions Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res

    @staticmethod
    #  instructions (type: Transfer/CrossChainTransfer/SwapTransfer)
    def instructions(type: str,body: list, networkCode: str, definiteSignerPublicKeys: list, transactionParams = '', Authorization=token):
        url = url_ + "/vault/instructions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body_ = {
            "body": body,
            "networkCode": networkCode,
            "type": type,
            "definiteSignerPublicKeys": definiteSignerPublicKeys,
            "transactionParams": transactionParams
        }

        logger.info('\n'+"<-----Instructions----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body_))
        res = requests.post(url=url, json=body_, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Instructions Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Instructions Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res


    @staticmethod
    # staking
    def post_staking(networkCode: str, symbol: str, delegator: str, amount: str, Authorization=web3token):
        url = url_ + '/staking/delegations'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "networkCode": networkCode,
            "coinSymbol":symbol,
            "delegator":delegator,
            "amount": amount
        }

        logger.info('\n'+"<-----Staking----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Staking Response----->"+"\n"+(res.text))
            # res_ = res.json()
            # r_estimatedFee = res_['_embedded']['transactions'][0]['estimatedFee']
            # r_hash = res_['_embedded']['transactions'][0]['hash']
            # r_id = res_['_embedded']['transactions'][0]['id']
            # r_networkCode = res_['_embedded']['transactions'][0]['networkCode']
            # r_requiredSignings = res_['_embedded']['transactions'][0]['requiredSignings']
            # r_serialized = res_['_embedded']['transactions'][0]['serialized']
            # r_status = res_['_embedded']['transactions'][0]['status']
            # ID = res_['id']

            return res
        else:
            logger.info('\n'+"<-----Staking Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res

    # @staticmethod
    # # 跨链
    # def post_crosschain(networkCode: str, symbol: str, from_add: str,toNetworkCode: str, to_add: str, amount: str, Authorization=Authorization_):
    #     url = url_ + '/cryptocurrencies/'+symbol+'/transfers'
    #     headers = {
    #         "Content-Type": "application/json",
    #         "Authorization": Authorization
    #     }
    #     body = {
    #         "from": from_add,
    #         "networkCode": networkCode,
    #         "symbol": symbol,
    #         "to": to_add,
    #         "toNetworkCode": toNetworkCode,
    #         "amount":amount
    #     }

    #     logger.info('\n'+"<-----Cross Chain----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
    #     res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
    #     if res.status_code == 200:
    #         logger.info('\n'+"<-----Cross Chain Response----->"+"\n"+(res.text))
    #         res_ = res.json()
    #         r_estimatedFee = res_['_embedded']['transactions'][0]['estimatedFee']
    #         r_hash = res_['_embedded']['transactions'][0]['hash']
    #         r_id = res_['_embedded']['transactions'][0]['id']
    #         r_networkCode = res_['_embedded']['transactions'][0]['networkCode']
    #         r_requiredSignings = res_['_embedded']['transactions'][0]['requiredSignings']
    #         r_serialized = res_['_embedded']['transactions'][0]['serialized']
    #         r_status = res_['_embedded']['transactions'][0]['status']
    #         ID = res_['id']

    #         return res,r_estimatedFee,r_hash,r_id,r_networkCode,r_requiredSignings,r_serialized,r_status,ID
    #     else:
    #         logger.info('\n'+"<-----Cross Chain Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
    #         return res

    @staticmethod
    # Rebuild
    def get_balance_transactuons(networkCode:str, symbol:str, filter_address="", Authorization=token):
        url = "http://18.163.229.203:8888/asset/api/cryptocurrencies/balance-transactions?symbol="+symbol+"&networkCode="+networkCode+"&filter=address:"+filter_address
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        logger.info('\n'+"<-----Qurey balance transactuons----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))

        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey balance transactuons----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Qurey balance transactuons Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # Rebuild
    def post_rebuild(txid:str, params:list, Authorization=web3token):
        url = url_ + '/transactions/' + txid + '/rebuild'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
           "params":params
        }

        logger.info('\n'+"<-----Rebuild----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Rebuild Response----->"+"\n"+(res.text))
            res_ = res.json()
            r_estimatedFee = res_['estimatedFee']
            r_hash = res_['hash']
            r_id = res_['id']
            r_networkCode = res_['networkCode']
            r_requiredSignings = res_['requiredSignings']
            r_serialized = res_['serialized']
            r_status = res_['status']
            return res,r_estimatedFee,r_hash,r_id,r_networkCode,r_requiredSignings,r_serialized,r_status
        else:
            logger.info('\n'+"<-----Rebuild Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res

    @staticmethod
    # sign
    def post_sign_transfers(transactions_estimatedFee: str, transactions_hash: str, transactions_id: str, transactions_networkCode: str, transactions_requiredSignings: list, transactions_serialized: str, signatures: list, status='BUILDING', Authorization=web3token):
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
        logger.info('\n'+"<-----Sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Sign Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Sign Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # sign
    def sign(id: str, signatures: list, serialized: str, Authorization=token):
        url = url_ + "/vault/transactions/" + id + "/signatures"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "signatures":signatures,
            "serialized": serialized
        }
        logger.info('\n'+"<-----Sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Sign Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Sign Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # send
    def send(id: str, Authorization=token):
        url = url_ + "/vault/transactions/" + id
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Send----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n')

        res = requests.patch(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Send Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Send Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 请求签名
    def post_req_sign(requiredSignings:array,Authorization=web3token):
        url = url_ + '/vault/keys/request-sign'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = requiredSignings
        logger.info('\n'+"<-----Request Sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Request Sign Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Request Sign Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 获取验证码
    def post_req_Verify(requestId:str,Authorization=web3token):
        url = url_ + '/vault/verify/verifications'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "requestId":requestId
        }
        logger.info('\n'+"<-----Request Verify----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Request Verify Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Request Verify Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # 托管key签名
    def post_confirm_sign(id:str,code:str,Authorization=web3token):
        url = url_ + '/vault/keys/confirm-sign'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        body = {
            "id":id,
            "code":code
        }
        logger.info('\n'+"<-----Confirm_Sign----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Confirm_Sign Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Confirm_Sign Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res
            raise Exception("请求异常")

    @staticmethod
    # send
    def post_send_transfers(transactions_id:str,Authorization=web3token):
        url = url_ + '/transactions/' + transactions_id + '/send'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Send----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.post(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Send Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Send Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            # raise Exception("请求异常")
            return res

    @staticmethod
    # 查询关联交易记录by hash
    def get_transactions_byhash(hash:str,Authorization=web3token):
        url = url_ + '/cryptocurrencies/balance-transactions/' + hash
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        logger.info('\n'+"<-----Qurey Transactions by hash----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))

        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey Transactions by hash Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Qurey Transactions by hash Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询交易
    def get_transactions(address: str, expand = 'transactions', Authorization=token):
        url = "http://13.215.207.236:8888/escrow/api/transactions?address="+address+"&asset=&categoryId=&network=MATIC"
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        logger.info('\n'+"<-----Qurey Transactions by id----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))

        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey Transactions by id Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Qurey Transactions by id Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询交易
    def get_transactions_byid(id: str, expand = 'transactions', Authorization=web3token):
        url = url_ + '/cryptocurrencies/transfers/' + id + '?expand=' + expand
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }
        logger.info('\n'+"<-----Qurey Transactions by id----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))

        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey Transactions by id Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Qurey Transactions by id Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询密钥
    def get_keys(Authorization=web3token):
        url = url_ + '/vault/keys'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Qurey Keys----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url,headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Qurey Keys Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----Qurey Keys Response Error----->"+"\n"+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 生成密钥
    def post_keys(count=1,Authorization=web3token):
        url = url_ + '/vault/keys'
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        body = {
            "count":count
        }

        logger.info('\n'+"<-----Create Key----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, headers=headers, json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Create Keys Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error('\n'+"<-----Create Keys Response Error----->"+"\n"+(res.text))
            raise Exception("请求异常")

if __name__ == '__main__':
    print(HttpUtils.get_account_list())
    # print(HttpUtils.post_keys())
    # print(HttpUtils.get_keys())
    # print(HttpUtils.get_balance_transactuons("BTC","BTC","34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo","eyJzaWduYXR1cmUiOiIweGU4YzU0YjkzYTRlZDBmM2UxY2FkMDVjMDQzZmQzY2U0MjUwNTExNzY4MGY4NWViMmViMzAzZjQ5ZjNhMGFmYjU1OWExOWQxNDg2OTI1YTM0YzFmYTMxNWYzMzhjYTRhNGM2NzY0YjNmNjhiODMxY2VkMmZlNGUxOGVkMWVkNTMwMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNDE0NDU2MDhcbklzc3VlZCBBdDogVGh1LCAyNSBBdWcgMjAyMiAxMTozMjoyMCBHTVRcbkV4cGlyYXRpb24gVGltZTogTW9uLCAyNSBBdWcgMjA0MiAxMTozMjoyMCBHTVQifQ==").json()[0]["blockHeight"])
    # print(HttpUtils.post_create_account("MATIC",["0293f4fefcaca702e09c0a121c33bc0059cc649079f26d420ed3fb64809e044565"]).json())