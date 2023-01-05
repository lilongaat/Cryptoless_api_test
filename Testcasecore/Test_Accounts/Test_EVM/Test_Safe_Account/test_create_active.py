# import json
# import random
# import string
# from time import sleep
# from decimal import Decimal
# import allure
# import pytest
# import sys
# import os
# sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
#     os.path.dirname(os.path.abspath(__file__)))))))
# from Common import Httpcore, Conf
# from Common.Loguru import logger

# from Config.readconfig import ReadConfig
# env_type = int(ReadConfig().get_env('type'))


# @allure.feature("Account Success!")
# class Test_account_success:
#     if env_type == 0: #测试
#         test_data = [
#             ("MATIC创建多签账户并激活","MATIC",["0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","03c420167aaf4fc7106646b2fe485519e5569ceb1584ae31d62537e349a4e4b5a9"],"2","dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da","0244fb46bba2e912f26a73126b89742ed7f521f593ee084953ae008172553a0113","0xe525E7cd17f6Dc950492755A089E452fd5d9d44f"),
#         ]
#     elif env_type == 1: #生产
#         test_data = []

#     @allure.story("Account Success!")
#     @allure.title('{test_title}')
#     @pytest.mark.parametrize('test_title,networkCode,publickey,threshold,privatekey_send,publickey_send,sendaddress,', test_data)
#     def test_custodial(self,test_title,networkCode,publickey,threshold,privatekey_send,publickey_send,sendaddress):

#         with allure.step("创建多签账户"):
#             body = {
#                 "networkCode":networkCode,
#                 "publicKeys":publickey,
#                 "threshold":threshold
#             }
#             safeacc = Httpcore.HttpCoreUtils.core_create_account(body)
#             assert safeacc.status_code == 200
#             id = safeacc.json()["id"]
#             safeaddress = safeacc.json()["address"]

#         with allure.step("激活账户"):
#             active = Httpcore.HttpCoreUtils.core_active_acc(id)
#             assert active.status_code == 200

#         with allure.step("查询账户"):
#             acc = Httpcore.HttpCoreUtils.core_query_account_byid(id)
#             assert acc.status_code == 200


# if __name__ == '__main__':
#     path = os.path.abspath(__file__) + ""
#     pytest.main(["-vs", path,'--alluredir=Report/Allure'])
#     # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')