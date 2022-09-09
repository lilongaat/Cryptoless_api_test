import csv
from web3 import Web3
import allure
import pytest
import pandas
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common.Loguru import logger

@allure.feature("Get Accounts!")
class Test_get_accounts:

    test_data = [
        ("ETH节点","https://mainnet.infura.io/v3/f8167b1c15ae4716976dd317d03b3e7f")
    ]

    @allure.story("Get Accounts!")
    @allure.title('获取地址 - {test_title}')
    @pytest.mark.parametrize('test_title,host', test_data)
    def test_get_accounts_byhost(self, test_title, host):
        
        with allure.step("Web3连接节点"):
            w3 = Web3(Web3.HTTPProvider(host))

        with allure.step("Web3获取当前区块高度"):
            blocknum = w3.eth.get_block_number()
            for i in range(10000):
                block_num = blocknum - i
                logger.error(block_num)

                with allure.step("Web3获取区块transactions"):
                    block = w3.eth.get_block(block_num)
                    transactions = block.transactions
                    for j in range(len(transactions)):

                        with allure.step("Web3获取区块每个transaction内address"):
                            transaction = w3.eth.get_transaction(transactions[j])
                            fromadd = transaction['from']
                            toadd = transaction['to']
                            # logger.error(transaction)
                            logger.info(fromadd)
                            logger.info(toadd)

                        with allure.step("address写入文件"):
                            path = '/Users/lilong/Documents/Test_Api/Testcase/Test_Account/Test_Create_Account/eth_address.csv'
                            with open(path,'a+') as f:
                                csv_write = csv.writer(f)
                                csv_write.writerow(["address",fromadd])
                                csv_write.writerow(["address",toadd])



if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')