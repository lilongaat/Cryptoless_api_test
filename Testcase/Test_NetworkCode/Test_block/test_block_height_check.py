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
        btc = Httpexplore.Block_explore.block_height("BTC")
        time = Conf.Config.now_time()
        if btc.status_code == 200:
            block_height = btc.json()["data"][0]["id"]
        else:
            block_height = "Serve Error " + str(btc.status_code)

        btc_graphql = Graphql.Graphql.getLatestBlock("BTC")
        time_ = Conf.Config.now_time()
        block_height_graphql = btc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("BTC")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "BTC"][0])

        logger.info("BTC Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        if abs(block_height - block_height_network) > 1:
            Httpfs.HttpFs.send_msg('BTC Block_Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/bitcoin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network))

    def test_block_height_doge():
        doge = Httpexplore.Block_explore.block_height("DOGE")
        time = Conf.Config.now_time()
        assert doge.status_code == 200
        block_height = doge.json()

        btc_graphql = Graphql.Graphql.getLatestBlock("DOGE")
        time_ = Conf.Config.now_time()
        block_height_graphql = btc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("DOGE")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "DOGE"][0])

        logger.info("DOGE Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('DOGE Height!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 1:
            Httpfs.HttpFs.send_msg(('DOGE Block_Height异常!\n' + "https://dogechain.info/api/simple查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    # def test_block_height_eth():
    #     eth = Graphql.Graphql.getLatestBlock("ETH")
    #     time = Conf.Config.now_time()
    #     assert eth.status_code == 200
    #     block_height = int(eth.json()["result"],16)

    #     eth_graphql = Graphql.Graphql.getLatestBlock("ETH")
    #     time_ = Conf.Config.now_time()
    #     block_height_graphql = eth_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

    #     networks = Http.HttpUtils.networks("ETH")
    #     block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "ETH"][0])

    #     logger.info("ETH Block_Height Gaps:" + str(abs(block_height - block_height_network)))

    #     # Httpfs.HttpFs.send_msg(('ETH Height!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    #     if abs(block_height - block_height_network) > 3:
    #         Httpfs.HttpFs.send_msg(('ETH Block_Height异常!\n' + "Etherscan Api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    def test_block_height_bsc():
        bsc = Httpexplore.Block_explore.block_height("BSC")
        time = Conf.Config.now_time()
        assert bsc.status_code == 200
        block_height = int(bsc.json()["result"])

        bsc_graphql = Graphql.Graphql.getLatestBlock("BSC")
        time_ = Conf.Config.now_time()
        block_height_graphql = bsc_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("BSC")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "BSC"][0])

        logger.info("BSC Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('BSC Height!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 3:
            Httpfs.HttpFs.send_msg(('BSC Block_Height异常!\n' + "https://blockchain.coinmarketcap.com/chain/binance-coin查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))
    
    def test_block_height_matic():
        matic = Httpexplore.Block_explore.block_height("MATIC")
        time = Conf.Config.now_time()
        assert matic.status_code == 200
        block_height = int(matic.json()["result"])

        matic_graphql = Graphql.Graphql.getLatestBlock("MATIC")
        time_ = Conf.Config.now_time()
        block_height_graphql = matic_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("MATIC")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "MATIC"][0])

        logger.info("MATIC Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('MATIC Height!\n' + "polygonscan api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 5:
            Httpfs.HttpFs.send_msg(('MATIC Block_Height异常!\n' + "polygonscan api查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    def test_block_height_atom():
        atom = Httpexplore.Block_explore.block_height("ATOM")
        time = Conf.Config.now_time()
        assert atom.status_code == 200
        block_height = int(atom.json()["block"]["last_commit"]["height"])

        atom_graphql = Graphql.Graphql.getLatestBlock("ATOM")
        time_ = Conf.Config.now_time()
        block_height_graphql = atom_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("ATOM")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "ATOM"][0])

        logger.info("ATOM Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('ATOM Height!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 3:
            Httpfs.HttpFs.send_msg(('ATOM Block_Height异常!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    def test_block_height_iris():
        iris = Httpexplore.Block_explore.block_height("IRIS")
        time = Conf.Config.now_time()
        assert iris.status_code == 200
        block_height = int(iris.json()["block"]["last_commit"]["height"])

        iris_graphql = Graphql.Graphql.getLatestBlock("IRIS")
        time_ = Conf.Config.now_time()
        block_height_graphql = iris_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("IRIS")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "IRIS"][0])

        logger.info("IRIS Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('IRIS Height!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 5:
            Httpfs.HttpFs.send_msg(('IRIS Block_Height异常!\n' + "Mintscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    def test_block_height_clv():
        clv = Httpexplore.Block_explore.block_height("CLV")
        time = Conf.Config.now_time()
        assert clv.status_code == 200
        block_height = clv.json()["data"]["count"]

        clv_graphql = Graphql.Graphql.getLatestBlock("CLV")
        time_ = Conf.Config.now_time()
        block_height_graphql = clv_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("CLV")
        block_height_network = int([n.get("blocks") for n in networks.json() if n.get("code") == "CLV"][0])

        logger.info("CLV Block_Height Gaps:" + str(abs(block_height - block_height_network)))

        # Httpfs.HttpFs.send_msg(('CLV Height!\n' + "https://clover.subscan.io/block查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

        if abs(block_height - block_height_network) > 5:
            Httpfs.HttpFs.send_msg(('CLV Block_Height异常!\n' + "Subscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

    def test_block_height_dot():
        dot = Httpexplore.Block_explore.block_height("DOT")
        time = Conf.Config.now_time()
        assert dot.status_code == 200
        block_height = dot.json()["data"]["blocks"][0]["block_num"]

        dot_graphql = Graphql.Graphql.getLatestBlock("DOT")
        time_ = Conf.Config.now_time()
        block_height_graphql = dot_graphql.json()["data"]["getLatestBlock"]["blockNumber"]

        networks = Http.HttpUtils.networks("DOT")
        block_height_network_list = ([n.get("blocks") for n in networks.json() if n.get("code") == "DOT"])
        if block_height_network_list == [None]:
            Httpfs.HttpFs.send_msg(('DOT Height!\n' + "Subscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network_list[0])))
        else:
            block_height_network = int(block_height_network_list[0])

            # logger.info("DOT Block_Height Gaps:" + str(abs(block_height - block_height_network)))
            if abs(block_height - block_height_network) > 10:
                Httpfs.HttpFs.send_msg(('DOT Height!\n' + "Subscan查询最新高度(" + time + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_ + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_ + "): " + str(block_height_network)))

if __name__ == '__main__':
    Test_block_height_check.test_block_height_btc()
    Test_block_height_check.test_block_height_doge()
    # Test_block_height_check.test_block_height_eth()
    Test_block_height_check.test_block_height_bsc()
    Test_block_height_check.test_block_height_matic()
    Test_block_height_check.test_block_height_atom()
    Test_block_height_check.test_block_height_iris()
    Test_block_height_check.test_block_height_clv()
    Test_block_height_check.test_block_height_dot()
    