import ssl
from threading import TIMEOUT_MAX
from async_timeout import timeout, timeout_at
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
from Common import Httprpc
from Common.Loguru import logger


@allure.feature("Host_Checks!")
class Test_host_check:

    test_data = [
            # infura                                                        # 测试的节点
            ("https://mainnet.infura.io/v3/f8167b1c15ae4716976dd317d03b3e7f","https://eth-mainnet.cryptoless.io/v1")
    ]

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_accounts')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_account_check(self, host_infura, host_test):
        
        with allure.step("节点eth_accounts一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_accounts(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_accounts(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_blockNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_blockNumber_check(self, host_infura, host_test):
        
        with allure.step("节点eth_blockNumber一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_blockNumber(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_blockNumber(host_test)
            assert test.status_code ==200 

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            # 转10进制
            assert -3 < (int(infura.json()["result"],16) - int(test.json()["result"],16)) < 3

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_call')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_call_check(self, host_infura, host_test):
        
        with allure.step("节点eth_call一致验证!"):
            pyload = {
                "from": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
                "to": "0x070e49b9818c2ba83e5035088c5796e328e414fc",
                "gas": "0x76c0",
                "gasPrice": "0x9184e72a000",
                "value": "0x9184e72a",
                "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
            }
            blocknum = "latest"
            infura = Httprpc.HttpRpcEth_Utils.eth_call(host_infura,pyload,blocknum)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_call(host_test,pyload,blocknum)
            assert test.status_code ==200 

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_estimateGas')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_estimateGas_check(self, host_infura, host_test):
        
        with allure.step("节点eth_estimateGas一致验证!"):
            pyload = {
                "from": "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F",
                "to": "0x070e49b9818c2ba83e5035088c5796e328e414fc",
                "gas": "0x76c0",
                "gasPrice": "0x9184e72a000",
                "value": "0x9184e72a",
                "data": "0xd46e8dd67c5d32be8d46e8dd67c5d32be8058bb8eb970870f072445675058bb8eb970870f072445675"
            }
            infura = Httprpc.HttpRpcEth_Utils.eth_estimateGas(host_infura,pyload)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_estimateGas(host_test,pyload)
            assert test.status_code ==200 

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_chainId')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_chainId_check(self, host_infura, host_test):
        with allure.step("节点eth_chainId一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_chainId(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_chainId(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_feeHistory')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_feeHistory_check(self, host_infura, host_test):
        with allure.step("节点eth_feeHistory一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_feeHistory(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_feeHistory(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_gasPrice')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_gasPrice_check(self, host_infura, host_test):
        with allure.step("节点eth_gasPrice一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_gasPrice(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_gasPrice(host_test)
            assert test.status_code == 200

            assert -10 < (int(infura.json()["result"],16) - int(test.json()["result"],16)) < 10

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getbalance')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getbalance_check(self, host_infura, host_test):
        with allure.step("节点eth_getbalance一致验证!"):
            address = "0x56eddb7aa87536c09ccc2793473599fd21a8b17f"
            infura = Httprpc.HttpRpcEth_Utils.eth_getbalance(host_infura,address,"latest")
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getbalance(host_test,address,"latest")
            assert test.status_code == 200

            assert int(infura.json()["result"],16) == int(test.json()["result"],16)

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getBlockByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockByHash_check(self, host_infura, host_test):
        with allure.step("节点eth_getBlockByHash一致验证!"):
            hash = "0x6744d872694e16a499df50164fabcfcd8c3a3dc1a7961223afd7578dc3c8ac6d"
            infura = Httprpc.HttpRpcEth_Utils.eth_getBlockByHash(host_infura,hash,False)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getBlockByHash(host_test,hash,False)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert infura.json()["result"]["difficulty"] == test.json()["result"]["difficulty"]
            assert infura.json()["result"]["extraData"] == test.json()["result"]["extraData"]
            assert infura.json()["result"]["gasLimit"] == test.json()["result"]["gasLimit"]
            assert infura.json()["result"]["gasUsed"] == test.json()["result"]["gasUsed"]
            assert infura.json()["result"]["hash"] == test.json()["result"]["hash"]
            assert infura.json()["result"]["logsBloom"] == test.json()["result"]["logsBloom"]
            assert infura.json()["result"]["miner"] == test.json()["result"]["miner"]
            assert infura.json()["result"]["mixHash"] == test.json()["result"]["mixHash"]
            assert infura.json()["result"]["nonce"] == test.json()["result"]["nonce"]
            assert infura.json()["result"]["number"] == test.json()["result"]["number"]
            assert infura.json()["result"]["receiptsRoot"] == test.json()["result"]["receiptsRoot"]
            assert infura.json()["result"]["sha3Uncles"] == test.json()["result"]["sha3Uncles"]
            assert infura.json()["result"]["size"] == test.json()["result"]["size"]
            assert infura.json()["result"]["stateRoot"] == test.json()["result"]["stateRoot"]
            assert infura.json()["result"]["timestamp"] == test.json()["result"]["timestamp"]
            assert infura.json()["result"]["totalDifficulty"] == test.json()["result"]["totalDifficulty"]
            assert infura.json()["result"]["transactions"] == test.json()["result"]["transactions"]
            assert infura.json()["result"]["transactionsRoot"] == test.json()["result"]["transactionsRoot"]
            assert infura.json()["result"]["uncles"] == test.json()["result"]["uncles"]

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getBlockByNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockByNumber_check(self, host_infura, host_test):
        with allure.step("节点eth_getBlockByNumber一致验证!"):
            blocknumber = 15171844
            infura = Httprpc.HttpRpcEth_Utils.eth_getBlockByNumber(host_infura,hex(blocknumber),False)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getBlockByNumber(host_test,hex(blocknumber),False)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert infura.json()["result"]["difficulty"] == test.json()["result"]["difficulty"]
            assert infura.json()["result"]["extraData"] == test.json()["result"]["extraData"]
            assert infura.json()["result"]["gasLimit"] == test.json()["result"]["gasLimit"]
            assert infura.json()["result"]["gasUsed"] == test.json()["result"]["gasUsed"]
            assert infura.json()["result"]["hash"] == test.json()["result"]["hash"]
            assert infura.json()["result"]["logsBloom"] == test.json()["result"]["logsBloom"]
            assert infura.json()["result"]["miner"] == test.json()["result"]["miner"]
            assert infura.json()["result"]["mixHash"] == test.json()["result"]["mixHash"]
            assert infura.json()["result"]["nonce"] == test.json()["result"]["nonce"]
            assert infura.json()["result"]["number"] == test.json()["result"]["number"]
            assert infura.json()["result"]["receiptsRoot"] == test.json()["result"]["receiptsRoot"]
            assert infura.json()["result"]["sha3Uncles"] == test.json()["result"]["sha3Uncles"]
            assert infura.json()["result"]["size"] == test.json()["result"]["size"]
            assert infura.json()["result"]["stateRoot"] == test.json()["result"]["stateRoot"]
            assert infura.json()["result"]["timestamp"] == test.json()["result"]["timestamp"]
            assert infura.json()["result"]["totalDifficulty"] == test.json()["result"]["totalDifficulty"]
            assert infura.json()["result"]["transactions"] == test.json()["result"]["transactions"]
            assert infura.json()["result"]["transactionsRoot"] == test.json()["result"]["transactionsRoot"]
            assert infura.json()["result"]["uncles"] == test.json()["result"]["uncles"]

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getBlockTransactionCountByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockTransactionCountByHash_check(self, host_infura, host_test):
        with allure.step("节点eth_getBlockTransactionCountByHash一致验证!"):
            hash = "0x6744d872694e16a499df50164fabcfcd8c3a3dc1a7961223afd7578dc3c8ac6d"
            infura = Httprpc.HttpRpcEth_Utils.eth_getBlockTransactionCountByHash(host_infura,hash)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getBlockTransactionCountByHash(host_test,hash)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getBlockTransactionCountByNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getBlockTransactionCountByNumber_check(self, host_infura, host_test):
        with allure.step("节点eth_getBlockTransactionCountByNumber一致验证!"):
            blocknumber = 15171844
            infura = Httprpc.HttpRpcEth_Utils.eth_getBlockTransactionCountByNumber(host_infura,hex(blocknumber))
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getBlockTransactionCountByNumber(host_test,hex(blocknumber))
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getCode')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getCode_check(self, host_infura, host_test):
        with allure.step("节点eth_getCode一致验证!"):
            address = "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F"
            blocknumber = "pending"
            infura = Httprpc.HttpRpcEth_Utils.eth_getCode(host_infura,address,blocknumber)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getCode(host_test,address,blocknumber)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getLogs')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getLogs_check(self, host_infura, host_test):
        with allure.step("节点eth_getLogs一致验证!"):
            address = "0x88e6a0c2ddd26feeb64f039a2c41296fcb3f5640"
            blockHash = "0xb8704fdcd36a122797928a657554dbe1c312ff562d762d3accb828d3205025a4"
            topics = [
                "0xc42079f94a6350d7e6235f29174924f928cc2ac818eb64fed8004e115fbcca67"
            ]
            infura = Httprpc.HttpRpcEth_Utils.eth_getLogs(host_infura,address,blockHash,topics)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getLogs(host_test,address,blockHash,topics)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getStorageAt')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getStorageAt_check(self, host_infura, host_test):
        with allure.step("节点eth_getStorageAt一致验证!"):
            address = "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F"
            storageposition = "0x6661e9d6d8b923d5bbaab1b96e1dd51ff6ea2a93520fdc9eb75d059238b8c5e9"
            infura = Httprpc.HttpRpcEth_Utils.eth_getStorageAt(host_infura,address,storageposition,"latest")
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getStorageAt(host_test,address,storageposition,"latest")
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByBlockHashAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockHashAndIndex_check(self, host_infura, host_test):
        with allure.step("节点eth_getTransactionByBlockHashAndIndex一致验证!"):
            blockhash = "0xb8704fdcd36a122797928a657554dbe1c312ff562d762d3accb828d3205025a4"
            index = "0x0"
            infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionByBlockHashAndIndex(host_infura,blockhash,index)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getTransactionByBlockHashAndIndex(host_test,blockhash,index)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByBlockNumberAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockNumberAndIndex_check(self, host_infura, host_test):
        with allure.step("节点eth_getTransactionByBlockNumberAndIndex一致验证!"):
            blocknumber = 15178549
            index = "0x0"
            infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionByBlockNumberAndIndex(host_infura,hex(blocknumber),index)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getTransactionByBlockNumberAndIndex(host_test,hex(blocknumber),index)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getTransactionByHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByHash_check(self, host_infura, host_test):
        with allure.step("节点eth_getTransactionByHash一致验证!"):
            hash = "0x66a05cb59b330428945a4b3b691075dd7c9b23dd773f4a0ce2046f3eb5f5973b"
            infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionByHash(host_infura,hash)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getTransactionByHash(host_test,hash)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert infura.json()["result"]["blockHash"] == test.json()["result"]["blockHash"]
            assert infura.json()["result"]["blockNumber"] == test.json()["result"]["blockNumber"]
            assert infura.json()["result"]["from"] == test.json()["result"]["from"]
            assert infura.json()["result"]["gas"] == test.json()["result"]["gas"]
            assert infura.json()["result"]["gasPrice"] == test.json()["result"]["gasPrice"]
            assert infura.json()["result"]["hash"] == test.json()["result"]["hash"]
            assert infura.json()["result"]["input"] == test.json()["result"]["input"]
            assert infura.json()["result"]["nonce"] == test.json()["result"]["nonce"]
            assert infura.json()["result"]["r"] == test.json()["result"]["r"]
            assert infura.json()["result"]["s"] == test.json()["result"]["s"]
            assert infura.json()["result"]["to"] == test.json()["result"]["to"]
            assert infura.json()["result"]["transactionIndex"] == test.json()["result"]["transactionIndex"]
            assert infura.json()["result"]["type"] == test.json()["result"]["type"]
            assert infura.json()["result"]["v"] == test.json()["result"]["v"]
            assert infura.json()["result"]["value"] == test.json()["result"]["value"]


    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getTransactionCount')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionCount_check(self, host_infura, host_test):
        with allure.step("节点eth_getTransactionCount一致验证!"):
            address = "0x56Eddb7aa87536c09CCc2793473599fD21A8b17F"
            # blockNumber = 14982566
            infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionCount(host_infura,address,"latest")
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getTransactionCount(host_test,address,"latest")
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getTransactionReceipt')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionReceipt_check(self, host_infura, host_test):
        with allure.step("节点eth_getTransactionReceipt一致验证!"):
            hash = "0x66a05cb59b330428945a4b3b691075dd7c9b23dd773f4a0ce2046f3eb5f5973b"
            infura = Httprpc.HttpRpcEth_Utils.eth_getTransactionReceipt(host_infura,hash)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getTransactionReceipt(host_test,hash)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getUncleByBlockHashAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockHashAndIndex_check(self, host_infura, host_test):
        with allure.step("节点eth_getUncleByBlockHashAndIndex一致验证!"):
            blockhash = "0x9c74f439c66de34b6d4486b21b41f13438f8e87a04bfd42488693a6a54eb48f3"
            index = "0x0"
            infura = Httprpc.HttpRpcEth_Utils.eth_getUncleByBlockHashAndIndex(host_infura,blockhash,index)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getUncleByBlockHashAndIndex(host_test,blockhash,index)
            assert test.status_code == 200

            assert infura.json()["id"] == test.json()["id"]

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getUncleByBlockNumberAndIndex')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getTransactionByBlockNumberAndIndex_check(self, host_infura, host_test):
        with allure.step("节点eth_getUncleByBlockNumberAndIndex一致验证!"):
            blocknumber = 15178549
            index = "0x0"
            infura = Httprpc.HttpRpcEth_Utils.eth_getUncleByBlockNumberAndIndex(host_infura,hex(blocknumber),index)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getUncleByBlockNumberAndIndex(host_test,hex(blocknumber),index)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getUncleCountByBlockHash')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleCountByBlockHash_check(self, host_infura, host_test):
        with allure.step("节点eth_getUncleCountByBlockHash一致验证!"):
            Blockhash = "0x452ffa22fc535bd4b7fa37850e66fd6795a3f1dbf3e557c4d329cc33bdc6c0ce"
            infura = Httprpc.HttpRpcEth_Utils.eth_getUncleCountByBlockHash(host_infura,Blockhash)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getUncleCountByBlockHash(host_test,Blockhash)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getUncleCountByBlockNumber')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getUncleCountByBlockNumber_check(self, host_infura, host_test):
        with allure.step("节点eth_getUncleCountByBlockNumber一致验证!"):
            blocknumber  = 15097332
            infura = Httprpc.HttpRpcEth_Utils.eth_getUncleCountByBlockNumber(host_infura,hex(blocknumber))
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getUncleCountByBlockNumber(host_test,hex(blocknumber))
            assert test.status_code == 200

            assert infura.json() == test.json()

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_getWork')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_getWork_check(self, host_infura, host_test):
        with allure.step("节点eth_getWork一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_getWork(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_getWork(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_mining')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_mining_check(self, host_infura, host_test):
        with allure.step("节点eth_mining一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_mining(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_mining(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_hashrate')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_hashrate_check(self, host_infura, host_test):
        with allure.step("节点eth_hashrate一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_hashrate(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_hashrate(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_protocolVersion')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_protocolVersion_check(self, host_infura, host_test):
        with allure.step("节点eth_protocolVersion一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_protocolVersion(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_protocolVersion(host_test)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert "result" in infura.json()
            assert "result" in test.json()

    @pytest.mark.skip(reason="跳过")
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_sendRawTransaction')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_sendRawTransaction_check(self, host_infura, host_test):
        with allure.step("节点 eth_sendRawTransaction 一致验证!"):
            rawtx = "0xf869018203e882520894f17f52151ebef6c7334fad080c5704d77216b732881bc16d674ec80000801ba02da1c48b670996dcb1f447ef9ef00b33033c48a4fe938f420bec3e56bfd24071a062e0aa78a81bf0290afbc3a9d8e9a068e6d74caa66c5e0fa8a46deaae96b0833"
            infura = Httprpc.HttpRpcEth_Utils.eth_sendRawTransaction(host_infura,rawtx)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_sendRawTransaction(host_test,rawtx)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert "error" in infura.json()
            assert "error" in test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_submitWork')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_syncing_check(self, host_infura, host_test):
        with allure.step("节点eth_submitWork一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_submitWork(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_submitWork(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('eth_syncing')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_syncing_check(self, host_infura, host_test):
        with allure.step("节点eth_syncing一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.eth_syncing(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.eth_syncing(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('net_listening')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_listening_check(self, host_infura, host_test):
        with allure.step("节点net_listening一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.net_listening(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.net_listening(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('net_peerCount')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_peerCount_check(self, host_infura, host_test):
        with allure.step("节点net_peerCount一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.net_peerCount(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.net_peerCount(host_test)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert "result" in infura.json()
            assert "result" in test.json()
 
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('net_version')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_version_check(self, host_infura, host_test):
        with allure.step("节点net_version一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.net_version(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.net_version(host_test)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @pytest.mark.xfail("暂不支持调用!")
    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('parity_nextNonce')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_parity_nextNonce_check(self, host_infura, host_test):
        with allure.step("节点parity_nextNonce一致验证!"):
            address = "0x56eddb7aa87536c09ccc2793473599fd21a8b17f"
            infura = Httprpc.HttpRpcEth_Utils.parity_nextNonce(host_infura,address)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.parity_nextNonce(host_test,address)
            assert test.status_code == 200

            assert infura.json() == test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('web3_clientVersion')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_web3_clientVersion_check(self, host_infura, host_test):
        with allure.step("节点web3_clientVersion一致验证!"):
            infura = Httprpc.HttpRpcEth_Utils.web3_clientVersion(host_infura)
            assert infura.status_code == 200
            test = Httprpc.HttpRpcEth_Utils.web3_clientVersion(host_test)
            assert test.status_code == 200

            assert infura.json()["jsonrpc"] == test.json()["jsonrpc"]
            assert infura.json()["id"] == test.json()["id"]
            assert "result" in infura.json()
            assert "result" in test.json()

    @allure.story("RPC_ETH_Host_Check!!")
    @allure.title('Filter methods')
    @pytest.mark.parametrize('host_infura,host_test', test_data)
    def test_Filter_check(self, host_infura, host_test):

        with allure.step("节点WS eth_newFilter 一致验证!"):
            params = [{"address":"0xdAC17F958D2ee523a2206206994597C13D831ec7"}]
            infura_filter = Web3(Web3.HTTPProvider(host_infura,request_kwargs={'timeout': 100})).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura_filter))
            test_filter = Web3(Web3.HTTPProvider(host_test,request_kwargs={'timeout': 100})).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test_filter))

            assert len(infura_filter.filter_id) > 0 and len(test_filter.filter_id) > 0

        with allure.step("节点WS eth_newBlockFilter 一致验证!"):
            params = ["latest"]
            infura = Web3(Web3.HTTPProvider(host_infura,request_kwargs={'timeout': 100})).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.HTTPProvider(host_test,request_kwargs={'timeout': 100})).eth.filter(params[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura.filter_id) > 0 and len(test.filter_id) > 0

        with allure.step("节点WS eth_getFilterLogs 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.HTTPProvider(host_infura,request_kwargs={'timeout': 100})).eth.get_filter_logs(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.HTTPProvider(host_test,request_kwargs={'timeout': 100})).eth.get_filter_logs(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) >= 0 and len(test) >= 0

        with allure.step("节点WS eth_getFilterChanges 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.HTTPProvider(host_infura,request_kwargs={'timeout': 100})).eth.get_filter_changes(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.HTTPProvider(host_test,request_kwargs={'timeout': 100})).eth.get_filter_changes(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert len(infura) >=0 and len(test) >= 0

        with allure.step("节点WS eth_uninstallFilter 一致验证!"):
            params_infura = [infura_filter.filter_id]
            params_test = [test_filter.filter_id]
            infura = Web3(Web3.HTTPProvider(host_infura,request_kwargs={'timeout': 100})).eth.uninstall_filter(params_infura[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_infura + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(infura))
            test = Web3(Web3.HTTPProvider(host_test,request_kwargs={'timeout': 100})).eth.uninstall_filter(params_test[0])
            logger.info("<-----Rquest----->"+"\n"+"Url:"+host_test + "\n"+"params:"+str(params)+"\n"+"<-----Response----->" + "\n"+str(test))

            assert infura == test