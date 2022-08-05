from web3 import Web3, HTTPProvider
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common.Loguru import logger

timeout = 30
# infura
url_infura = "https://mainnet.infura.io/v3/f8167b1c15ae4716976dd317d03b3e7f"
url_test = "https://eth-mainnet.cryptoless.io/v1"

@allure.feature("Host_Methods!")
class Test_host_methods_check:

    test_data = [
            ("0x2fc57d8858DD47995e35E259Feb1c3556D8af047"),
            ("0x037244f1026Df01b6f6880e38A64BEF012D9B6e5"),
            ("0x65c2e54a4c75ff6da7b6B32369c1677250075fb2"),
            ("0x2532eC5E562a24E1eeD1E419c8b2713d01bbFA87"),
            ("0xbE00746639A1CE4E2E8DAF3538703d33E89FfDC3"),
            ("0x4f7bb4dce543d745abea9913f23cdd29a1c55620"),
            ("0xcbd6832ebc203e49e2b771897067fce3c58575ac"),
            ("0xea674fdde714fd979de3edf0f56aa9716b898ec8"),
            ("0x7670f484e339c9282a96633902379f4bb6881b58"),
            ("0x3cb354a8950cdda946d1a58f4accea8d05487fdf"),
    ]

    @allure.story("ETH_Host_Methods!")
    @allure.title('eth_getBalance  Address:-{address}')
    @pytest.mark.parametrize('address', test_data)
    def test_account_check(self, address):
        with allure.step("获取节点BlockNumber!"):
            blocknum_infura = Web3(Web3.HTTPProvider(url_infura)).eth.get_block_number()
            print(blocknum_infura)

        with allure.step("节点近1000个块 eth_getBalance 一致验证!"):
            for i in range(1000):
                params = [address,hex(blocknum_infura-i)]
                infura = Web3(Web3.HTTPProvider(url_infura)).eth.get_balance(params[0],params[1])
                logger.info("<-----Rquest----->"+"\n"+"Url:"+url_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" +"\n"+ str(infura))
                test = Web3(Web3.HTTPProvider(url_test)).eth.get_balance(params[0],params[1])
                logger.info("<-----Rquest----->"+"\n"+"Url:"+url_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

                assert infura == test

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')



