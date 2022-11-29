import json
from time import sleep
from decimal import Decimal
import allure
import pytest
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Httprpc, Httpfs, Conf, Graphql, Httpexplore
from Common.Loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    ob_token = ReadConfig().get_debug('ob_token')

elif env_type == 1: # Release
    ob_token = ReadConfig().get_release('ob_token')


NetWorkcode = ""
address = ""
type = ""
limit = "1000"

accounts = Http.HttpUtils.get_account_list(NetWorkcode,address,type,limit,ob_token)

# 删除账户
for i in range(len(accounts.json())):
    id = accounts.json()[i]["id"]
    del_account = Http.HttpUtils.del_account_byid(id,ob_token)
    assert accounts.status_code == 200

accounts_ = Http.HttpUtils.get_account_list(NetWorkcode,address,type,limit,ob_token)
assert len(accounts_.json()) == 0