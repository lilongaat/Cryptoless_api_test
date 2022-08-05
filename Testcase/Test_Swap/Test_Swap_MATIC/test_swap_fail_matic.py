import json
from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger

# 单签账户
@allure.feature("Swap_MATIC!")
class Test_swap_fail_matic:
    test_data = [
        # 测试&生产
        ("amount精度超出-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(7),400),
        ("fromcoin==tocoin-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),400),
        ("amount为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1","",400),
        ("amount超出余额-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",100000,400),
        ("address为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","","1",Conf.Config.random_amount(3),400),
        ("address异常-Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","swap","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","1",Conf.Config.random_amount(3),400),
        ("from_coin为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),404),
        ("from_coin不支持-Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","PAX","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),404),
        ("to_coin为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),404),
        ("to_coin异常-Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","MKR","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),400),
        ("slippage为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","",Conf.Config.random_amount(3),400),
        ("slippage为0(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0",Conf.Config.random_amount(3)),
        ("slippage超出(51)-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","51",Conf.Config.random_amount(3),400),
        ("networkCode为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),400),
        ("networkCode不支持-Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"BTC","USDT","USDC","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),400),
        ("type为空-Swap(USDC-USDT)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),400),
        ("type异常-Swap(USDT-USDC)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDT","USDC","transfer","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(3),404),
    ]

    @allure.story("Swap_MATIC_Fail!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述!!--SWAP--!!====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,amount,type,transactionParams)
            assert res.status_code == status_code_check

# 单签账户
@allure.feature("Swap_MATIC!")
class Test_swap_sign_fail_matic:
    test_data = [
        # 测试&生产
        ("Swap-错误的私钥签名!",["83b749bf2fa7af2f20bd154fef973646fba9bc6c6da422ed633c653134a4a782"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","1",Conf.Config.random_amount(2),400),
    ]

    @allure.story("Swap_MATIC_Fail!")
    @allure.title('单签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check', test_data)
    def test_swap_matic_safe(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述!!--SWAP--!!====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,amount,type,transactionParams)
            assert res[0].status_code == 200

        with allure.step("签名交易——sign"):
            signature = Conf.Config.sign(privatekey[0],res[5][0]['hash'])
            signatures = [
                {
                    "hash":res[5][0]['hash'],
                    "publickey":res[5][0]['publicKeys'][0],
                    "signature":signature
                }
            ]
            sig = Http.HttpUtils.post_sign_transfers(res[1],res[2],res[3],res[4],res[5],res[6],signatures)
            assert sig.status_code == status_code_check

# 多签账户
@allure.feature("Swap_MATIC!")
class Test_swap_fail_matic_safe:
    test_data = [
        # 测试
        ("fromcoin==tocoin-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDC","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1","",400),
        ("amount为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1","",400),
        ("amount超出余额-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1","10000",400),
        ("address为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","","1",Conf.Config.random_amount(3),400),
        ("address异常-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","1",Conf.Config.random_amount(3),400),
        ("from_coin为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),404),
        ("from_coin不支持-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","PAX","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),404),
        ("to_coin为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),400),
        ("to_coin不支持-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","PAX","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),400),
        ("slippage为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","",Conf.Config.random_amount(3),400),
        ("slippage为0-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","0",Conf.Config.random_amount(3),400),
        ("slippage超出(51)-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","51",Conf.Config.random_amount(3),400),
        ("networkCode为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),400),
        ("networkCode不支持-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"BTC","USDC","USDT","swap","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),404),
        ("type为空-Swap!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),400),
        ("type异常-Swap",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["02ac5e97a0659d6ce59c5b10b2ace331bffa276a555ff333b09beda99bd6b9f52e","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"MATIC","USDC","USDT","transfer","0xE8e140D77F9Ff1f5b4eaC5388D182ac16D80E0f2","1",Conf.Config.random_amount(3),404),
    ]
    # test_data = [
    #     # 生产
    #     ("fromcoin==tocoin-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDC","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1","",400),
    #     ("amount为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1","",400),
    #     ("amount超出余额-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1","10000",400),
    #     ("address为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","","1",Conf.Config.random_amount(3),400),
    #     ("address异常-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","tb1qqrw8uz4j305w6fjr4mwng040sv7kz8hcczjfun","1",Conf.Config.random_amount(3),400),
    #     ("from_coin为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),404),
    #     ("from_coin不支持-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","PAX","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),404),
    #     ("to_coin为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),400),
    #     ("to_coin不支持-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","PAX","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),400),
    #     ("slippage为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","",Conf.Config.random_amount(3),400),
    #     ("slippage为0-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","0",Conf.Config.random_amount(3),400),
    #     ("slippage超出(51)-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","51",Conf.Config.random_amount(3),400),
    #     ("networkCode为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),400),
    #     ("networkCode不支持-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"BTC","USDC","USDT","swap","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),400),
    #     ("type为空-Swap!",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),400),
    #     ("type异常-Swap",["f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9"],["033685566f89433252d4c6fcf39ef73daf004ca5b454a7a4815e3f514d8b74d8ad","028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d"],"MATIC","USDC","USDT","transfer","0x7FdafbE014B345A4ab884a1AF98981AE2462F2A8","1",Conf.Config.random_amount(3),404),
    # ]

    @allure.story("Swap_MATIC_Fail!")
    @allure.title('多签账户Swap-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check', test_data)
    def test_swap_matic(self,test_title,privatekey,PublicKeys,networkCode,from_coin,to_coin,type,address,slippage,amount,status_code_check):

        with allure.step("构建交易——transfers"):
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述!!--SWAP--!!====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            res = Http.HttpUtils.post_instructions(networkCode,from_coin,to_coin,PublicKeys,address,slippage,amount,type,transactionParams)
            assert res.status_code == status_code_check

if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_swap_fail_matic_safe"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')