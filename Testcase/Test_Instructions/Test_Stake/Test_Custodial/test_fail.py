import json
import random
import string
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))))
from Common import Http, Conf
from Common.Loguru import logger

# custodial
@allure.feature("Stake_Fail!")
class Test_stake_fail:
    test_data = [
        # IRIS网络
        ("Custodial账户IRIS质押networkcode为空","","IRIS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2100000),
        ("Custodial账户IRIS质押networkcode不存在","IRISS","IRIS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS质押networkcode不支持","ETH","ETH","stake","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS质押symbol为空","IRIS","","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS质押symbol不存在","IRIS","IIRS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS质押地址为空","IRIS","IRIS","stake","",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS质押地址非该用户","IRIS","IRIS","stake","iva1543nj4z07vjqztvu3358fr2z2hcp0qtmceank5",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS质押地址非该网络","IRIS","IRIS","stake","0xC0959365ca20e3e587FEfAEaf48DaEC479bE83eD",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS质押金额为空","IRIS","IRIS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a","",400,2300000),
        ("Custodial账户IRIS质押金额大于余额","IRIS","IRIS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a","100000",400,2400000),
        ("Custodial账户IRIS质押金额超出精度","IRIS","IRIS","stake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(19)),400,2100000),

        ("Custodial账户IRIS赎回networkcode为空","","IRIS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2100000),
        ("Custodial账户IRIS赎回networkcode不存在","IRISS","IRIS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS赎回networkcode不支持","ETH","ETH","unstake","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS赎回symbol为空","IRIS","","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS赎回symbol不存在","IRIS","IIRS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(5)),400,2200000),
        ("Custodial账户IRIS赎回地址为空","IRIS","IRIS","unstake","",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS赎回地址非该用户","IRIS","IRIS","unstake","iva1543nj4z07vjqztvu3358fr2z2hcp0qtmceank5",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS赎回地址非该网络","IRIS","IRIS","unstake","0xC0959365ca20e3e587FEfAEaf48DaEC479bE83eD",str(Conf.Config.random_amount(5)),404,2200000),
        ("Custodial账户IRIS赎回金额为空","IRIS","IRIS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a","",400,2300000),
        ("Custodial账户IRIS赎回金额大于余额","IRIS","IRIS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a","100",400,2100000),
        ("Custodial账户IRIS赎回金额超出精度","IRIS","IRIS","unstake","iaa1tpm89pqldl2fcte86xqv4328tyywdyz6x2u47a",str(Conf.Config.random_amount(19)),400,2100000),

        # CLV网络
        # ("Custodial账户IRIS质押","CLV","CLV","stake","5DhLERQkHMtYXipo3jrp5eQYpgHNmYdC3qMS4bW4Sx6hp9Bw",str(Conf.Config.random_amount(4))),
        # ("Custodial账户IRIS赎回","CLV","CLV","unstake","5DhLERQkHMtYXipo3jrp5eQYpgHNmYdC3qMS4bW4Sx6hp9Bw",str(Conf.Config.random_amount(5))),
        # ("Custodial账户IRISclaim","CLV","CLV","claim","5DhLERQkHMtYXipo3jrp5eQYpgHNmYdC3qMS4bW4Sx6hp9Bw",0),
    ]

    @allure.story("Custodial_Stake_Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,symbol,type,address,amount,status_check,code_check', test_data)
    def test_custodial(self,test_title,networkCode,symbol,type,address,amount,status_check,code_check):

        with allure.step("构建交易——instructions"):
            if type == "claim":
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                }
            else:
                body = {
                    "delegator":address,
                    "coinSymbol":symbol,
                    "amount":amount
                }
            transactionParams = {
                "memo":''.join(random.sample(string.ascii_letters + string.digits, 10))
            }
            stake = Http.HttpUtils.instructions(type,body,networkCode,[],transactionParams)

        with allure.step("交易断言"):
            assert stake.status_code == status_check
            assert stake.json()["code"] == code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')