from python_graphql_client import GraphqlClient
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.readconfig import ReadConfig
from loguru import logger

# Debug
timeout_ = int(ReadConfig().get_debug('timeout'))
url_ = ReadConfig().get_debug('url_Enhanced_Api')
headers = {
            "Content-Type": "application/json",
        }


class HttpUtils:
    @staticmethod
    # 查询合集明细
    def get_collection_details(collection_address:str):
        url = url_ + '/sit/v1/nft/collection/' + collection_address

        logger.info("\n"+"<-----Query Collection Details----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Collection Details Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Collection Details Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询合集明细 Genie
    def get_collection_details_genie(collection_address:str):
        url = "https://genie-production-api.herokuapp.com/collections"
        body = {
                "filters": {
                    "address": collection_address
                },
                "limit": 1,
                "fields": {
                    "traits": 1,
                    "stats": 1,
                    "indexingStats.openSea": 1,
                    "imageUrl": 1,
                    "bannerImageUrl": 1,
                    "twitter": 1,
                    "externalUrl": 1,
                    "instagram": 1,
                    "discordUrl": 1,
                    "marketplaceCount": 1,
                    "floorPrice": 1
                },
                "offset": 0
            }

        logger.info("\n"+"<-----Genie Query Collection Details----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+"body:"+str(body))
        res = requests.post(url=url, headers=headers, json=body, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Genie Query Collection Details Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Genie Query Collection Details Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询NFT明细
    def get_nft_details(collection_address:str, id:str):
        url = url_ + '/sit/v1/nft/assets/' + collection_address + '/' + id

        logger.info("\n"+"<-----Query NFT Details----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query NFT Details Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query NFT Details Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询NFT明细 Genie
    def get_nft_details_genie(collection_address:str, id:str):
        url = 'https://genie-production-api.herokuapp.com/assetDetails?address=' + collection_address + '&tokenId=' + id

        logger.info("\n"+"<-----Genie Query NFT Details----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Genie Query NFT Details Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Genie Query NFT Details Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询NFT owner
    def get_nft_owners(collection_address:str, id:str):
        url = url_ + '/sit/v1/nft/assets/' + collection_address +'/' + id + '/owners'

        logger.info("\n"+"<-----Query NFT Owners----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query NFT Owners Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query NFT Owners Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询合集NFT列表
    def get_collection_nft_list(collection_address:str):
        url = url_ + '/sit/v1/nft/assets?collection_address=' + collection_address

        logger.info("\n"+"<-----Query Collection NFT List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Collection NFT List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Collection NFT List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询合集NFT列表 GEM
    def get_collection_nft_list_gem(collection_address:str):
        url = "https://api-3.gemlabs.xyz/assets"
        headers_ = {
            'authority': 'api-3.gemlabs.xyz',
            'accept': 'application/json',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7,ja;q=0.6,ko;q=0.5,la;q=0.4,pt;q=0.3,mt;q=0.2,es;q=0.1,it;q=0.1,ru;q=0.1',
            'content-type': 'application/json',
            'origin': 'https://www.gem.xyz',
            'referer': 'https://www.gem.xyz/',
            'sec-ch-ua': '".Not/A)Brand";v="99", "Google Chrome";v="103", "Chromium";v="103"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36',
            'x-api-key': 'iMHRYlpIXs3zfcBY1r3iKLdqS2YUuOUs'
        }
        body = {"filters":{"traits":{},"traitsRange":{},"address":collection_address,"rankRange":{},"price":{}},"sort":{"currentEthPrice":"asc"},"fields":{"id":1,"name":1,"address":1,"collectionName":1,"collectionSymbol":1,"externalLink":1,"imageUrl":1,"smallImageUrl":1,"animationUrl":1,"standard":1,"market":1,"pendingTrxs":1,"currentBasePrice":1,"paymentToken":1,"marketUrl":1,"marketplace":1,"tokenId":1,"priceInfo":1,"tokenReserves":1,"ethReserves":1,"sellOrders":1,"startingPrice":1,"rarityScore":1},"offset":0,"limit":20000,"markets":[],"status":["all"]}

        logger.info("\n"+"<-----GEM Query Collection NFT List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers_)+'\n\n'+"body:"+str(body))
        res = requests.post(url=url, headers=headers_, json=body ,timeout=100)
        if res.status_code == 200:
            # logger.info('\n'+"<-----GEM Query Collection NFT List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----GEM Query Collection NFT List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询合集owner列表
    def get_collection_owners_list(collection_address:str):
        url = url_ + '/sit/v1/nft/assets?collection_address=' + collection_address

        logger.info("\n"+"<-----Query Collection Owners List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Collection Owners List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Collection Owners List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询owner拥有的NFT列表
    def get_owner_nft_list(owner_address:str):
        url = url_ + '/sit/v1/nft/assets?owner_address=' + owner_address

        logger.info("\n"+"<-----Query Owner NFT List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Owner NFT List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Owner NFT List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询所有合集列表
    def get_collections_list():
        url = url_ + '/sit/v1/nft/collections'

        logger.info("\n"+"<-----Query Collections List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Collections List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Collections List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询合集历史交易
    def get_collections_transaction_history_list(collection_address:str):
        url = url_ + '/sit/v1/nft/collection/' + collection_address + '/transactions'

        logger.info("\n"+"<-----Query Collections Transaction History List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query Collections Transaction History List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query Collections Transaction History List Error----->'+(res.text))
            raise Exception("请求异常")

    @staticmethod
    # 查询NFT历史交易
    def get_nft_transaction_history_list(collection_address:str,id:str):
        url = url_ + '/sit/v1/nft/collection/' + collection_address + '/' + id + '/transactions'

        logger.info("\n"+"<-----Query NFT Transaction History List----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers))
        res = requests.get(url=url, headers=headers,timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Query NFT Transaction History List Response----->"+"\n"+(res.text))
            return res
        else:
            logger.error(str(res.status_code) + "\n"+'<-----Query NFT Transaction History List Error----->'+(res.text))
            raise Exception("请求异常")



if __name__ == '__main__':
    collection_address = "0x23581767a106ae21c074b2276d25e5c3e136a68b"
    id = "8607"
    owner_address = "0x01660cc34a2ae458dc040589f65d3b31cb08b5fb"
    # print(HttpUtils.get_collection_details_genie(collection_address))
    # print(HttpUtils.get_nft_details(collection_address,id))
    # print(HttpUtils.get_nft_owners(collection_address,id))
    # print(HttpUtils.get_collection_nft_list(collection_address))
    # print(HttpUtils.get_collection_owners_list(collection_address))
    # print(HttpUtils.get_owner_nft_list(owner_address))
    # print(HttpUtils.get_collections_list())
    # print(HttpUtils.get_collections_transaction_history_list(collection_address))
    # print(HttpUtils.get_nft_transaction_history_list(collection_address,id))
    # print(HttpUtils.get_collection_nft_list_gem(collection_address))