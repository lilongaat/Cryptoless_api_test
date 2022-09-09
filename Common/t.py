import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

# Debug
timeout_ = int(ReadConfig().get_debug('timeout'))
url_ = ReadConfig().get_debug('url')
Authorization_ = ReadConfig().get_debug('Authorization')

# Release
# timeout_ = int(ReadConfig().get_release('timeout'))
# url_ = ReadConfig().get_release('url')
# Authorization_ = ReadConfig().get_release('Authorization')


class HttpUtils:

    @staticmethod
    #  instructions
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

        logger.info('\n'+"<-----Instructions----->"+"\n"+"Url:"+url+'\n\n'+'Headers:'+json.dumps(headers)+'\n\n'+'Body:'+json.dumps(body))
        res = requests.post(url=url, json=body_, headers=headers, timeout=timeout_)
        if res.status_code == 200:
            logger.info('\n'+"<-----Instructions Response----->"+"\n"+(res.text))
            return res
        else:
            logger.info('\n'+"<-----Instructions Response Error----->"+"\n"+str(res.status_code)+"\n"+(res.text))
            return res

 

if __name__ == '__main__':
    body = {
        "from":"0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",
        "to":"0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",
        "symbol":"ETH",
        "amount":0.00001
    }
    r = HttpUtils.post_instructions("Transfer",body,"ETH-RINKEBY",["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"])