from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Httprpc, Httpfs, Conf, Graphql, Httpexplore
from Common.Loguru import logger


class Test_block_height_check:
    
    def test_block_height_btc():
        btc = Httpexplore.BTC.block()
        time = Conf.Config.now_time()
        assert btc.status_code == 200
        block_height = btc.json()["data"][0]["height"]

        btc_graphql = Graphql.Graphql.getLatestBlock("BTC")
        time_ = Conf.Config.now_time()
        block_height_graphql = btc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # block_height_network = Http.HttpUtils.get_networks()
        # assert block_height_network.status_code == 200
        # block_height_network = int([b.get('blocks') for b in block_height_network.json() if b.get('code') == 'BTC'][0])

        # Httpfs.HttpFs.send_msg('BTC Height!\n' + "https://blockchain.coinmarketcap.com/chain/bitcoin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql))

        if abs(block_height - block_height_graphql) > 1:
            Httpfs.HttpFs.send_msg('BTC Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/bitcoin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql))

    def test_block_height_doge():
        doge = Httpexplore.DOGE.block()
        time = Conf.Config.now_time()
        assert doge.status_code == 200
        block_height = doge.json()

        btc_graphql = Graphql.Graphql.getLatestBlock("DOGE")
        time_ = Conf.Config.now_time()
        block_height_graphql = btc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('DOGE Height!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 1:
            Httpfs.HttpFs.send_msg(('DOGE Height异常!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

    def test_block_height_eth():
        eth = Httpexplore.ETH.block_etherscanapi()
        time = Conf.Config.now_time()
        assert eth.status_code == 200
        block_height = int(eth.json()["result"],16)

        eth_graphql = Graphql.Graphql.getLatestBlock("ETH")
        time_ = Conf.Config.now_time()
        block_height_graphql = eth_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('ETH Height!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 3:
            Httpfs.HttpFs.send_msg(('ETH Height异常!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

    def test_block_height_bsc():
        bsc = Httpexplore.BSC.block()
        time = Conf.Config.now_time()
        assert bsc.status_code == 200
        block_height = int(bsc.json()["result"])

        bsc_graphql = Graphql.Graphql.getLatestBlock("BSC")
        time_ = Conf.Config.now_time()
        block_height_graphql = bsc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('BSC Height!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 3:
            Httpfs.HttpFs.send_msg(('BSC Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))
    
    def test_block_height_matic():
        matic = Httpexplore.MATIC.block()
        time = Conf.Config.now_time()
        assert matic.status_code == 200
        block_height = int(matic.json()["result"])

        matic_graphql = Graphql.Graphql.getLatestBlock("MATIC")
        time_ = Conf.Config.now_time()
        block_height_graphql = matic_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('MATIC Height!\n' + "polygonscan api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 5:
            Httpfs.HttpFs.send_msg(('MATIC Height异常!\n' + "polygonscan api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

    def test_block_height_atom():
        atom = Httpexplore.ATOM.block()
        time = Conf.Config.now_time()
        assert atom.status_code == 200
        block_height = atom.json()["block_height"]

        atom_graphql = Graphql.Graphql.getLatestBlock("ATOM")
        time_ = Conf.Config.now_time()
        block_height_graphql = atom_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('ATOM Height!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 3:
            Httpfs.HttpFs.send_msg(('ATOM Height异常!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

    def test_block_height_clv():
        clv = Httpexplore.CLV.block()
        time = Conf.Config.now_time()
        assert clv.status_code == 200
        block_height = clv.json()["data"]["count"]

        clv_graphql = Graphql.Graphql.getLatestBlock("CLV")
        time_ = Conf.Config.now_time()
        block_height_graphql = clv_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        # Httpfs.HttpFs.send_msg(('CLV Height!\n' + "https://clover.subscan.io/block查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

        if abs(block_height - block_height_graphql) > 5:
            Httpfs.HttpFs.send_msg(('CLV Height异常!\n' + "https://clover.subscan.io/block查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql)))

if __name__ == '__main__':
    Test_block_height_check.test_block_height_btc()
    Test_block_height_check.test_block_height_doge()
    Test_block_height_check.test_block_height_eth()
    Test_block_height_check.test_block_height_bsc()
    Test_block_height_check.test_block_height_matic()
    Test_block_height_check.test_block_height_atom()
    Test_block_height_check.test_block_height_clv()