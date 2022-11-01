from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Httprpc, Httpfs, Conf, Graphql, Httpexplore
from Common.Loguru import logger

web3token = "eyJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTU4MzAxOTk1NTUzMDg5NTM2MVxuSXNzdWVkIEF0OiBUaHUsIDIwIE9jdCAyMDIyIDA4OjU5OjAzIEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBTdW4sIDE3IE9jdCAyMDMyIDA4OjU5OjAzIEdNVCIsInNpZ25hdHVyZSI6IjB4MDA4NTA0NmM1YmYwYWFkZjkwMjIyMWFhNGU0OTFjODllYTU5ZTAxZGQ2ODIwNTdkMDU0Y2U2MzcyNTdkYTE2ZTIyNTJlMzYxYWJmNjE4ZmEwOWJmODVmYjEwM2RjMmZhYzg4MzFkODNmMDcwNGZlMjdhZmUzYTdjYWY0NGE2YjYxYyJ9"

class Test_price_check:
    
    def test_price_btc():
        btc = Httpexplore.BTC.block()
        time = Conf.Config.now_time()
        assert btc.status_code == 200
        price = btc.json()["data"][0]["quote"]["price"]

        networks = Http.HttpUtils.get_networks(web3token)
        price_ = [n.get()]


        # Httpfs.HttpFs.send_msg('BTC Height!\n' + "https://blockchain.coinmarketcap.com/chain/bitcoin查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql))

        # if abs(price - price_graphql) > 1:
        #     Httpfs.HttpFs.send_msg('BTC Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/bitcoin查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql))

    def test_price_doge():
        doge = Httpexplore.DOGE.block()
        time = Conf.Config.now_time()
        assert doge.status_code == 200
        price = doge.json()

        btc_graphql = Graphql.Graphql.getLatestBlock("DOGE")
        time_ = Conf.Config.now_time()
        price_graphql = btc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('DOGE Height!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 1:
            Httpfs.HttpFs.send_msg(('DOGE Height异常!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

    def test_price_eth():
        eth = Httpexplore.ETH.block_etherscanapi()
        time = Conf.Config.now_time()
        assert eth.status_code == 200
        price = int(eth.json()["result"],16)

        eth_graphql = Graphql.Graphql.getLatestBlock("ETH")
        time_ = Conf.Config.now_time()
        price_graphql = eth_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('ETH Height!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 3:
            Httpfs.HttpFs.send_msg(('ETH Height异常!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

    def test_price_bsc():
        bsc = Httpexplore.BSC.block()
        time = Conf.Config.now_time()
        assert bsc.status_code == 200
        price = int(bsc.json()["result"])

        bsc_graphql = Graphql.Graphql.getLatestBlock("BSC")
        time_ = Conf.Config.now_time()
        price_graphql = bsc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('BSC Height!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 3:
            Httpfs.HttpFs.send_msg(('BSC Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))
    
    def test_price_matic():
        matic = Httpexplore.MATIC.block()
        time = Conf.Config.now_time()
        assert matic.status_code == 200
        price = int(matic.json()["result"])

        matic_graphql = Graphql.Graphql.getLatestBlock("MATIC")
        time_ = Conf.Config.now_time()
        price_graphql = matic_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('MATIC Height!\n' + "polygonscan api查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 5:
            Httpfs.HttpFs.send_msg(('MATIC Height异常!\n' + "polygonscan api查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

    def test_price_atom():
        atom = Httpexplore.ATOM.block()
        time = Conf.Config.now_time()
        assert atom.status_code == 200
        price = atom.json()["price"]

        atom_graphql = Graphql.Graphql.getLatestBlock("ATOM")
        time_ = Conf.Config.now_time()
        price_graphql = atom_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('ATOM Height!\n' + "Mintscan查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 3:
            Httpfs.HttpFs.send_msg(('ATOM Height异常!\n' + "Mintscan查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

    def test_price_clv():
        clv = Httpexplore.CLV.block()
        time = Conf.Config.now_time()
        assert clv.status_code == 200
        price = clv.json()["data"]["count"]

        clv_graphql = Graphql.Graphql.getLatestBlock("CLV")
        time_ = Conf.Config.now_time()
        price_graphql = clv_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('CLV Height!\n' + "https://clover.subscan.io/block查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

        if abs(price - price_graphql) > 5:
            Httpfs.HttpFs.send_msg(('CLV Height异常!\n' + "https://clover.subscan.io/block查询最新高度(" + time + "): " + str(price) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(price_graphql)))

if __name__ == '__main__':
    Test_price_check.test_price_btc()
    # Test_price_check.test_price_doge()
    # Test_price_check.test_price_eth()
    # Test_price_check.test_price_bsc()
    # Test_price_check.test_price_matic()
    # Test_price_check.test_price_atom()
    # Test_price_check.test_price_clv()