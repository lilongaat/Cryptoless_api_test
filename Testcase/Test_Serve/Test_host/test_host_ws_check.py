import ssl
import certifi
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(certifi.where())
from web3 import Web3, HTTPProvider
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common.Loguru import logger

timeout_ws = 30

@allure.feature("Host_Checks!")
class Test_host_ws_check:

    test_data = [
            # infura                                                          # 测试的节点
            ("wss://mainnet.infura.io/ws/v3/f8167b1c15ae4716976dd317d03b3e7f","wss://eth-mainnet.cryptoless.io")
    ]

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_accounts')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_account_check(self, host_infura, host_test):

        with allure.step("节点WS eth_accounts一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.accounts
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" +"\n"+ str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.accounts
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test
            

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_blockNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_blockNumber_check(self, host_infura, host_test):

        with allure.step("节点 eth_blockNumber一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.block_number
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" +"\n"+ str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.block_number
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" +"\n"+ str(test))

            assert -3 < (infura - test) < 3

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_call')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_call_check(self, host_infura, host_test):

        with allure.step("节点WS eth_call 一致验证!"):
            params = {"to": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","data": "0x6d4ce63c"}
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.call(params)
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.call(params)
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_chainId')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_chainId_check(self, host_infura, host_test):

        with allure.step("节点WS eth_chainId 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.chain_id
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.chain_id
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_estimateGas')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_estimateGas_check(self, host_infura, host_test):

        with allure.step("节点WS eth_estimateGas 一致验证!"):
            params = {"to": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","data": "0x6d4ce63c"}
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.estimate_gas(params)
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.estimate_gas(params)
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_feeHistory')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_feeHistory_check(self, host_infura, host_test):

        with allure.step("节点WS eth_feeHistory 一致验证!"):
            params = ["0x5","latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.fee_history(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.fee_history(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getBalance')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBalance_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getBalance 一致验证!"):
            params = ["0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_balance(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_balance(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_gasPrice')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_gasPrice_check(self, host_infura, host_test):

        with allure.step("节点WS eth_gasPrice 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.gas_price
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.gas_price
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getBlockByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockByHash_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getBlockByHash 一致验证!"):
            params = ["0x9c74f439c66de34b6d4486b21b41f13438f8e87a04bfd42488693a6a54eb48f3",False]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))
            logger.info(type(test))

            assert infura == test
    
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getBlockByNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockByNumber_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getBlockByNumber 一致验证!"):
            params = [hex(15171844),False]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getBlockTransactionCountByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockTransactionCountByHash_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getBlockTransactionCountByHash 一致验证!"):
            params = ["0x9c74f439c66de34b6d4486b21b41f13438f8e87a04bfd42488693a6a54eb48f3"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block_transaction_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block_transaction_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getBlockTransactionCountByNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockTransactionCountByNumber_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getBlockTransactionCountByNumber 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block_transaction_count(hex(15171844))
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_block_transaction_count(hex(15171844))
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getCode')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getCode_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getCode 一致验证!"):
            params = ["0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_code(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_code(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getLogs')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getLogs_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getLogs 一致验证!"):
            params = [{
                "address":"0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
                "blockHash":"0x5d089aeb0ff4b9bbb14577ef99d1cb9fc47873871b00780df38751d9d4c75679"
            }]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_logs(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_logs(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getStorageAt')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getStorageAt_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getStorageAt 一致验证!"):
            params = ["0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","0x6661e9d6d8b923d5bbaab1b96e1dd51ff6ea2a93520fdc9eb75d059238b8c5e9","latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_storage_at(params[0],params[1],params[2])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_storage_at(params[0],params[1],params[2])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByBlockHashAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockHashAndIndex_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getTransactionByBlockHashAndIndex 一致验证!"):
            params = ["0xb8704fdcd36a122797928a657554dbe1c312ff562d762d3accb828d3205025a4","0x0"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.getTransactionByBlock(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.getTransactionByBlock(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByBlockNumberAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockNumberAndIndex_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getTransactionByBlockNumberAndIndex 一致验证!"):
            params = [hex(15178549),"0x0"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByHash_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getTransactionByHash 一致验证!"):
            params = ["0x66a05cb59b330428945a4b3b691075dd7c9b23dd773f4a0ce2046f3eb5f5973b"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getTransactionCount')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionCount_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getTransactionCount 一致验证!"):
            params = ["0x56Eddb7aa87536c09CCc2793473599fD21A8b17F","latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_count(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_count(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test
    
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getTransactionReceipt')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionReceipt_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getTransactionReceipt 一致验证!"):
            params = ["0x66a05cb59b330428945a4b3b691075dd7c9b23dd773f4a0ce2046f3eb5f5973b"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_receipt(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_transaction_receipt(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test
    
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getUncleByBlockHashAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleByBlockHashAndIndex_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getUncleByBlockHashAndIndex 一致验证!"):
            params = ["0x9c74f439c66de34b6d4486b21b41f13438f8e87a04bfd42488693a6a54eb48f3","0x0"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getUncleByBlockNumberAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleByBlockNumberAndIndex_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getUncleByBlockNumberAndIndex 一致验证!"):
            params = [hex(14064507),"0x0"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_by_block(params[0],params[1])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getUncleCountByBlockHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleCountByBlockHash_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getUncleCountByBlockHash 一致验证!"):
            params = ["0x452ffa22fc535bd4b7fa37850e66fd6795a3f1dbf3e557c4d329cc33bdc6c0ce"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getUncleCountByBlockNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleCountByBlockNumber_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getUncleCountByBlockNumber 一致验证!"):
            params = [hex(15097332)]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_uncle_count(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_getWork')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getWork_check(self, host_infura, host_test):

        with allure.step("节点WS eth_getWork 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.getWork
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.getWork
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_mining')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_mining_check(self, host_infura, host_test):

        with allure.step("节点WS eth_mining 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.mining
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.mining
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_hashrate')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_hashrate_check(self, host_infura, host_test):

        with allure.step("节点WS eth_hashrate 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.hashrate
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.hashrate
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_protocolVersion')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_protocolVersion_check(self, host_infura, host_test):

        with allure.step("节点WS eth_protocolVersion 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.protocol_version
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.protocol_version
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) > 0 and len(test)

    @pytest.mark.skip(reason="跳过")
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_sendRawTransaction')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_eth_sendRawTransactionsendRawTransaction_check(self, host_infura, host_test):

        with allure.step("节点WS eth_sendRawTransaction 一致验证!"):
            params = ["0xf869018203e882520894f17f52151ebef6c7334fad080c5704d77216b732881bc16d674ec80000801ba02da1c48b670996dcb1f447ef9ef00b33033c48a4fe938f420bec3e56bfd24071a062e0aa78a81bf0290afbc3a9d8e9a068e6d74caa66c5e0fa8a46deaae96b0833"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.send_raw_transaction(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.send_raw_transaction(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) > 0 and len(test)

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_submitWork')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_submitWork_check(self, host_infura, host_test):

        with allure.step("节点WS eth_submitWork 一致验证!"):
            params = ["0x0000000000000001","0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef","0xD1FE5700000000000000000000000000D1FE5700000000000000000000000000"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.submitWork(params[0],params[1],params[2])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.submitWork(params[0],params[1],params[2])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('eth_syncing')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_syncing_check(self, host_infura, host_test):

        with allure.step("节点WS eth_syncing 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.syncing
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.syncing
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('net_listening')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_listening_check(self, host_infura, host_test):

        with allure.step("节点WS net_listening 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.listening
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.listening
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('net_peerCount')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_peerCount_check(self, host_infura, host_test):

        with allure.step("节点WS net_peerCount 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.peer_count
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.peer_count
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura > 0 and test > 0

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('net_version')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_version_check(self, host_infura, host_test):

        with allure.step("节点WS net_version 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.version
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).net.version
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    # @allure.story("WS_ETH_Host_Check!!")
    # @allure.title('parity_nextNonce')
    # @pytest.mark.parametrize('host_infura,host_test', test_data)
    # def test_nextNonce_check(self, host_infura, host_test):

    #     with allure.step("节点WS parity_nextNonce 一致验证!"):
    #         params = []
    #         infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).
    #         logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
    #         test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.?????
    #         logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

    #         assert infura == test

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('web3_clientVersion')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_web3_clientVersion_check(self, host_infura, host_test):

        with allure.step("节点WS web3_clientVersion 一致验证!"):
            params = []
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).clientVersion
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).clientVersion
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) > 0 and len(test) > 0

    @allure.story("WS_ETH_Host_Check!!")
    @allure.title('Filter methods')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_Filter_check(self, host_infura, host_test):

        with allure.step("节点WS eth_newFilter 一致验证!"):
            params = [{"address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}]
            infura_filter = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura_filter))
            test_filter = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test_filter))

            assert len(infura_filter.filter_id) > 0 and len(test_filter.filter_id) > 0

        with allure.step("节点WS eth_newBlockFilter 一致验证!"):
            params = ["latest"]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura.filter_id) > 0 and len(test.filter_id) > 0

        with allure.step("节点WS eth_getFilterLogs 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_filter_logs(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_filter_logs(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) >= 0 and len(test) >= 0

        with allure.step("节点WS eth_getFilterChanges 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_filter_changes(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.get_filter_changes(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) >=0 and len(test) >= 0

        with allure.step("节点WS eth_uninstallFilter 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.uninstall_filter(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.uninstall_filter(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test

    # @allure.story("WS_ETH_Host_Check!!")
    # @allure.title('Subscription methods')
    # @pytest.mark.parametrize('host_infura,host_test', test_data)
    # def test_pppppp_check(self, host_infura, host_test):

    #     with allure.step("节点WS eth_subscribe 一致验证!"):
    #         params = ["newHeads"]
    #         infura = Web3(Web3.WebsocketProvider(host_infura,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.ppppp
    #         logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
    #         test = Web3(Web3.WebsocketProvider(host_test,websocket_kwargs={"ssl":ssl_context},websocket_timeout=timeout_ws)).eth.pppppp
    #         logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

    #         assert infura == test