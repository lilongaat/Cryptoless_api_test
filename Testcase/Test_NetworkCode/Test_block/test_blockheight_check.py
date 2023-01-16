from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Httprpc, Httpfs, Conf, Graphql, Httpexplore
from Common.Loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))


@allure.feature("Block Height!")
class Test_block_height_check:
    if env_type == 0: #测试
        test_data = [
            ("","BTC",3),
            ("","DOGE",3),
            ("","GOERLI",3),
            ("","BSC",5),
            ("","MATIC",5),
            ("","ATOM",5),
            ("","IRIS",5),
            ("","DOT",5),
            ("","CLV",5),
        ]
    elif env_type == 1: #生产
        test_data = [
            ("","BTC",3),
            ("","DOGE",3),
            ("","ETH",3),
            ("","BSC",3),
            ("","MATIC",3),
            ("","ATOM",5),
            ("","IRIS",5),
            ("","DOT",5),
            ("","CLV",5),
        ]

    @allure.story("Block Height Check!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,networkCode,gaps', test_data)
    def test_block_check(self,test_title,networkCode,gaps):

        with allure.step("浏览器查询块高"):
            block_explore = Httpexplore.Block_explore.block_height(networkCode)
            time_explore = Conf.Config.now_time()
            if block_explore.status_code == 200:
                if networkCode == "BTC":
                    block_height = block_explore.json()["data"][0]["id"]
                elif networkCode == "DOGE":
                    block_height = block_explore.json()
                elif networkCode == "ETH":
                    block_height = int(block_explore.json()["result"],16)
                elif networkCode == "GOERLI":
                    block_height = int(block_explore.json()["result"],16)
                elif networkCode == "BSC":
                    block_height = int(block_explore.json()["result"])
                elif networkCode == "MATIC":
                    block_height = int(block_explore.json()["result"])
                elif networkCode == "ATOM":
                    block_height = int(block_explore.json()["block"]["last_commit"]["height"])
                elif networkCode == "IRIS":
                    block_height = int(block_explore.json()["block"]["last_commit"]["height"])
                elif networkCode == "DOT":
                    block_height = block_explore.json()["data"]["blocks"][0]["block_num"]
                elif networkCode == "CLV":
                    if env_type == 0:
                        block_height = block_explore.json()["data"]["blocks"][0]["block_num"]
                    elif env_type == 1:
                        block_height = block_explore.json()["data"]["count"]
                else:
                    raise Exception("networkCode No Support")
            else:
                block_height = "Serve Error " + str(block_explore.status_code)

        logger.debug(block_height)

        with allure.step("Graphql查询块高"):
            block_graphql = Graphql.Graphql.getLatestBlock(networkCode)
            time_graphql = Conf.Config.now_time()
            if block_graphql.status_code == 200:
                block_height_graphql = block_graphql.json()["data"]["getLatestBlock"]["blockNumber"]
            else:
                block_height_graphql = "Serve Error " + str(block_graphql.status_code)

        with allure.step("Network查询块高"):
            networks = Http.HttpUtils.networks(networkCode)
            time_network = Conf.Config.now_time()
            if networks.status_code == 200:
                block_height_network_list = ([n.get("blocks") for n in networks.json() if n.get("code") == networkCode])
                if block_height_network_list == [None]:
                    Httpfs.HttpFs.send_msg((networkCode + ' Height!\n' + "浏览器查询最新高度(" + time_explore + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_graphql + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_network + "): " + str(block_height_network_list[0])))
                else:
                    block_height_network = int(block_height_network_list[0])
            else:
                block_height_network = "Serve Error " + str(networks.status_code)

        with allure.step("对比浏览器查询块高&Network查询块高"):
            if block_explore.status_code != 200 or block_graphql.status_code != 200 or networks.status_code != 200:
                Httpfs.HttpFs.send_msg(networkCode + ' Block_Height异常!\n' + "浏览器查询最新高度(" + time_explore + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_graphql + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_network + "): " + str(block_height_network))
            else:
                if abs(block_height - block_height_network) > gaps:
                    Httpfs.HttpFs.send_msg(networkCode + ' Block_Height异常!\n' + "浏览器查询最新高度(" + time_explore + "): " + str(block_height) + "\n" + "Graphql查询最新高度(" + time_graphql + "): " + str(block_height_graphql) + "\n" + "NetWork查询最新高度(" + time_network + "): " + str(block_height_network))
    

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
    