from array import array
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

# Debug
# timeout_ = int(ReadConfig().get_debug('timeout'))
# url_ = ReadConfig().get_debug('url')
# Authorization_ = ReadConfig().get_debug('Authorization')

# Release
timeout_ = int(ReadConfig().get_release('timeout'))
url_ = ReadConfig().get_release('url')
Authorization_ = ReadConfig().get_release('Authorization')


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
        logger.info("<-----Register----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))

        res = requests.post(url=url, json=body, headers=headers, timeout=timeout_)
        if res.status_code != 200:
            logger.error('registrations 失败！')
            logger.error('Response | '+res.text)
            # raise Exception("请求异常")
        else:
            return res

    @staticmethod
    # 查询账户信息
    def get_account(address="",Authorization=Authorization_):
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

    @staticmethod
    # 查询代理账户列表
    def get_safe_agents(Authorization=Authorization_):
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
    def post_safe_agents_sign(networkCode:str,hash:str,Authorization=Authorization_):
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
    def post_safe_activation(accountId:str,Authorization=Authorization_):
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
    def get_safe_activation(accountId:str,Authorization=Authorization_):
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
    def post_create_account(networkcode: str, publickeys: list, threshold =1, address = "", Authorization=Authorization_):
        url = 'http://18.163.229.203:8888/core/api/accounts/save'
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
    # 查询networks信息
    def get_networks(Authorization=Authorization_):
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
    # 查询holders信息
    def get_holders(Network='',symbol ='',address='',Authorization=Authorization_):
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
    def get_staking(Network='',symbol ='',address='',Authorization=Authorization_):
        url = url_ + '/staking/delegators?networkCode='+Network+'&symbol='+symbol
        headers = {
            "Content-Type": "application/json",
            "Authorization": Authorization
        }

        logger.info('\n'+"<-----Staking----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Staking Response----->"+"\n"+(res.text))
            if len(json.loads(res.text)) > 0:
                return res
            else:
                logger.error('\n'+'<-----Query Staking Response Error----->'+(res.text))
                raise Exception("没有查询到任何Staking信息!")
        else:
            logger.error('\n'+'<-----Query Staking Response Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询Swap路由信息
    def get_swap_route(networkCode:str,from_coin:str,to_coin:str,amount:str,Authorization=Authorization_):
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
    def post_instructions(type: str,body: list, networkCode: str, definiteSignerPublicKeys: list, transactionParams = '', Authorization=Authorization_):
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
    # staking
    def post_staking(networkCode: str, symbol: str, delegator: str, amount: str, Authorization=Authorization_):
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
    def get_balance_transactuons(networkCode:str, symbol:str, filter_address="", Authorization=Authorization_):
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
    def post_rebuild(txid:str, params:list, Authorization=Authorization_):
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
    # 请求签名
    def post_req_sign(requiredSignings:array,Authorization=Authorization_):
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
    def post_req_Verify(requestId:str,Authorization=Authorization_):
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
    def post_confirm_sign(id:str,code:str,Authorization=Authorization_):
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
    def post_send_transfers(transactions_id:str,Authorization=Authorization_):
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
            logger.info('\n'+"<-----Transfer Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            # raise Exception("请求异常")
            return res

    @staticmethod
    # 查询关联交易记录by hash
    def get_transactions_byhash(hash:str,Authorization=Authorization_):
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
    # 查询转账信息by id
    def get_transactions_byid(id: str, expand = 'transactions', Authorization=Authorization_):
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
    def get_keys(Authorization=Authorization_):
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
    def post_keys(count=1,Authorization=Authorization_):
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
    # print(HttpUtils.post_keys())
    # print(HttpUtils.get_keys())
    print(HttpUtils.get_balance_transactuons("BTC","BTC","34xp4vRoCGJym3xR7yCVPFHoCNxv4Twseo","eyJzaWduYXR1cmUiOiIweGU4YzU0YjkzYTRlZDBmM2UxY2FkMDVjMDQzZmQzY2U0MjUwNTExNzY4MGY4NWViMmViMzAzZjQ5ZjNhMGFmYjU1OWExOWQxNDg2OTI1YTM0YzFmYTMxNWYzMzhjYTRhNGM2NzY0YjNmNjhiODMxY2VkMmZlNGUxOGVkMWVkNTMwMWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNDE0NDU2MDhcbklzc3VlZCBBdDogVGh1LCAyNSBBdWcgMjAyMiAxMTozMjoyMCBHTVRcbkV4cGlyYXRpb24gVGltZTogTW9uLCAyNSBBdWcgMjA0MiAxMTozMjoyMCBHTVQifQ==").json()[0]["blockHeight"])