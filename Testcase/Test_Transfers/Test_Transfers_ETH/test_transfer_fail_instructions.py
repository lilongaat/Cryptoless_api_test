import random
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger

# 单签账户 ETH转账失败
@allure.feature("Transfers_Fail!")
class Test_transfers_fail_eth:
    test_data = [
        # 测试
        ("余额不足转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'1000000',400),
        ("精度超长(19位)转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'',400),
        ("转账金额为负数!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-0.000001",400),
        ("转账金额字符串类型异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","max",400),
        ("转账from地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_ETH_transfer_Fail!")
    @allure.title('单签账户异常转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_transfer_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == status_code_check

# 多签账户 ETH转账失败
@allure.feature("Transfers_Fail!")
class Test_transfers_fail_eth_safe:
    test_data = [
        # 测试
        ("余额不足转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'1000000',400),
        ("精度超长(19位)转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'',400),
        ("转账金额为负数!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-0.000001",400),
        ("转账金额字符串类型异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","max",400),
        ("转账from地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","F0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账from地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账to地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账to地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传一个[k1],k1不在账户下!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k1不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k2不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k1k2都不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["039a91ef110ef339820a2ade32e66cb147034d6bffe5d0ef9dc57f97f8b8d1820a","0350752b44279cd17b51f8a32feaa551f61d75a8491ef13d6543b42f8cffd7bd86"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k1不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k2不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k1k2都不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["039a91ef110ef339820a2ade32e66cb147034d6bffe5d0ef9dc57f97f8b8d1820a","0350752b44279cd17b51f8a32feaa551f61d75a8491ef13d6543b42f8cffd7bd86","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
    ]

    @allure.story("Transfers_ETH_transfer_Fail!")
    @allure.title('单签账户异常转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_transfer_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == status_code_check

# 单签账户 ERC20 转账失败
@allure.feature("Transfers_Fail!")
class Test_transfers_fail_erc20:
    test_data = [
        # 测试
        ("余额不足转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'9999999999999999999',400),
        ("精度超长(19位)转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'',400),
        ("转账金额为负数!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-0.000001",400),
        ("转账金额字符串类型异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","max",400),
        ("转账from地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账from地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(6),400),
        ("转账to地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","",Conf.Config.random_amount(6),400),
    ]

    @allure.story("Transfers_ERC20_Success!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_erc20(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == status_code_check

# 多签账户 ERC20转账失败
@allure.feature("Transfers_Fail!")
class Test_transfers_fail_erc20_safe:
    test_data = [
        # 测试
        ("余额不足转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'999999999999999999',400),
        ("精度超长(19位)转账!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",Conf.Config.random_amount(19),400),
        ("转账金额为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",'',400),
        ("转账金额为负数!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","-0.000001",400),
        ("转账金额字符串类型异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","max",400),
        ("转账from地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","F0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账from地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账to地址异常!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","bDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("转账to地址为空!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传一个[k1],k1不在账户下!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k1不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k2不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2],k1k2都不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["039a91ef110ef339820a2ade32e66cb147034d6bffe5d0ef9dc57f97f8b8d1820a","0350752b44279cd17b51f8a32feaa551f61d75a8491ef13d6543b42f8cffd7bd86"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k1不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["028daaa4515f3b7aa4b9842d76bfd620f0a915143324761e35ce5ecd846219b28d","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k2不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","03e7c686af45ffd23da1951920b4d6ae97e404ae4e296255b3d20c753c68e799fc","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
        ("publickey传两个[k1,k2,k3],k1k2都不在账户下!!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["039a91ef110ef339820a2ade32e66cb147034d6bffe5d0ef9dc57f97f8b8d1820a","0350752b44279cd17b51f8a32feaa551f61d75a8491ef13d6543b42f8cffd7bd86","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.01), random.randint(5,18)),400),
    ]

    @allure.story("Transfers_ERC20_transfer_Fail!")
    @allure.title('单签账户异常转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check', test_data)
    def test_transfers_transfer_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == status_code_check

# 单签账户转账 send手续费过大
@allure.feature("Transfers_Fail!")
class Test_send_fail:
    test_data = [
        # 测试
        ("ETH转账手续费超出限制!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(6),400,2101000),
        ("ERC20转账手续费超出限制!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",Conf.Config.random_amount(2),400,2101000),
    ]

    @allure.story("Transfers_send_Fail!")
    @allure.title('单签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

        with allure.step("rebuild交易——rebuild"):
            params = {
                "gasPrice":"0x6edf2a079f"
                }
            rebuild = Http.HttpUtils.post_rebuild(transfer.json()['_embedded']['transactions'][0]['id'],params)
            assert rebuild[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],rebuild[5][0]['hash'])
            signatures = [
                {
                    "hash":rebuild[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        with allure.step("签名交易——sign"):
            sig = Http.HttpUtils.post_sign_transfers(rebuild[1],rebuild[2],rebuild[3],rebuild[4],rebuild[5],rebuild[6],signatures)
            assert sig.status_code == 200

        with allure.step("广播交易——send"):
            send = Http.HttpUtils.post_send_transfers(rebuild[3])
            assert send.status_code == status_code_check
            assert send.json()['code'] == code_check

# 多签账户转账 send手续费过大
@allure.feature("Transfers_Fail!")
class Test_send_fail_safe:
    test_data = [
        # 测试
        ("publickey[k1(托管),k2(私有),k2(私有)]",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","ETH","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(0.00001,0.0001), random.randint(5,18)),400,400),
        # ("publickey[k1(托管),k2(私有),k2(私有)]",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],["03f1b7e94f4c83b3c1505cc15e4a14e172323afe0b946295eece18300da6ec2228","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0","0331e3ab5059c28098131d50856a99fcf40bea39b61f08ea55e1f35fbed131d2c0"],"ETH-RINKEBY","symbol","0xF0d689E18d2f000663e507A39dCfA1DdC26a8Dc3","0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be",round(random.uniform(1,1000), random.randint(5,18)),400,400),
    ]

    @allure.story("Transfers_send_Fail!")
    @allure.title('多签账户转账-{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check', test_data)
    def test_transfers_send_fail(self,test_title,privatekey,PublicKeys,networkCode,symbol,from_add,to_add,amount,status_code_check,code_check):

        with allure.step("构建交易——instructions"):
            body = {
                "from":from_add,
                "to":to_add,
                "symbol":symbol,
                "amount":amount
            }
            transactionParams = {
                "memo":"hahahhahahhahahhaahhahhahhahahaha@@==这是一段描述！！====@@hahahhahahhahahhaahhahhahhahahaha"
            }
            transfer = Http.HttpUtils.post_instructions("Transfer",body,networkCode,PublicKeys,transactionParams)
            assert transfer.status_code == 200

        with allure.step("rebuild交易——rebuild"):
            params = {
                "gasPrice":"0x6edf2a079f"
                }
            rebuild = Http.HttpUtils.post_rebuild(transfer.json()['_embedded']['transactions'][0]['id'],params)
            assert rebuild[0].status_code == 200

            signature = Conf.Config.sign(privatekey[0],rebuild[5][0]['hash'])
            signatures = [
                {
                    "hash":rebuild[5][0]['hash'],
                    "publickey":PublicKeys[0],
                    "signature":signature
                }
            ]

        # with allure.step("签名交易——sign"):
        #     sig = Http.HttpUtils.post_sign_transfers(rebuild[1],rebuild[2],rebuild[3],rebuild[4],rebuild[5],rebuild[6],signatures)
        #     assert sig.status_code == 200

        # with allure.step("广播交易——send"):
        #     send = Http.HttpUtils.post_send_transfers(rebuild[3])
        #     assert send.status_code == status_code_check
        #     assert send.json()['code'] == code_check


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_send_fail_safe"
    pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')