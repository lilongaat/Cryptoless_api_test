from loguru import logger
import requests
import json
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Config.readconfig import ReadConfig

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))
if env_type == 0:
    webhook_url = ReadConfig().get_debug('webhook_url')
elif env_type == 1:
    webhook_url = ReadConfig().get_release('webhook_url')

class HttpFs:
         
    def send_msg(text:str):
        #webhook
        header = {
            "Content-type": "application/json",
            "charset":"utf-8"
            }
        data = {
            "msg_type": "text",
            "content": {
                "text": text
                }
            }
        requests.post(webhook_url,json=data,headers=header)