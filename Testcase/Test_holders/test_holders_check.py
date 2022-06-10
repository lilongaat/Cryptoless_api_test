from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__)))))
from Common import Http, Httprpc, Httpfs, Conf
from Common.Loguru import logger


@allure.feature("Holders_Checks!")
class Test_holders_check:

    test_data = [
        {
            'Authorization': 'eyJzaWduYXR1cmUiOiIweGRmMDcwN2YzZDlmOWU3MmVjMmVmMmM1NTVmMzU2MzlmMjBkOTJmZjU0OWIzODA5NjI4N2U0MWJiYmM2ZDMzOTM1ZDgzN2FlMGRiYjhjNDM3MzMwNDg4ZjYzNmZmYTAwYmRkNGYxM2Q5ZTkxNWQwZDUzODJkOGFmZDJiOGUyMDdhMWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogODcwNzA5Mzhcbklzc3VlZCBBdDogVGh1LCA5IEp1biAyMDIyIDE1OjAxOjI0IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBNb24sIDkgSnVuIDIwNDIgMTU6MDE6MjQgR01UIn0=',
        }
    ]

    @allure.story("Holders Rpc查询用户资产信息检查!")
    @pytest.mark.parametrize('param', test_data)
    def test_balances_check(self, param):
        Authorization = list(param.values())[0]

# 第一次Holders、Rpc余额Check，余额不一致的地址写入数组-"holders_diff"

        holders_diff = []

        # holders接口查询用户所有资产信息
        res = Http.HttpUtils.get_holders(Authorization=Authorization)

        for i in range(len(res)):
            # Check：ETH网络ETH资产
            if res[i]["networkCode"] == res[i]["symbol"] == 'ETH':

                # RPC接口查询地址资产信息
                res_rpc = Httprpc.HttpRpcUtils.Eth_getbalance(
                    res[i]["networkCode"], res[i]["address"], "latest")

                logger.info(('Holders Rpc查询余额!\n' + "networkCode:"+res[i]["networkCode"]+"  symbol:"+res[i]["symbol"]+"  address:"+res[i]
                             ["address"] + '\n' + "Holders查询余额:"+res[i]["quantity"] + '\n' + "Rpc查询余额:" + res_rpc))

                if res[i]["quantity"] != res_rpc:
                    # holders和Rpc资产信息对比，余额不一致的地址写入数组-"holders_diff"
                    holders_diff.append(res[i]["address"])
            else:
                logger.info("networkCode:" + res[i]["networkCode"] +
                            " | symbol:" + res[i]["symbol"] + " | symbol:" + res[i]["address"] + ' | Rpc查询余额暂不支持!')

        if len(holders_diff) > 0:
            sleep(10)

# 数组-"holders_diff"内地址Holders、Rpc余额Check，余额不一致时飞书报警
            for h in range(len(holders_diff)):

                # Holdes查询地址资产信息
                res_ag = Http.HttpUtils.get_holders(
                    Authorization=Authorization, address=holders_diff[h])
                res_ag_time = Conf.Config.now_time()

                for r in range(len(res_ag)):
                    # Check：ETH网络ETH资产
                    if res_ag[r]["networkCode"] == res_ag[r]["symbol"] == "ETH":
                        # RPC接口查询地址资产信息
                        res_rpc_ag = Httprpc.HttpRpcUtils.Eth_getbalance(
                            res_ag[r]["networkCode"], res_ag[r]["address"], "latest")
                        res_rpc_ag_time = Conf.Config.now_time()

                        if res_ag[r]["quantity"] != res_rpc_ag:
                            # holders和Rpc资产信息对比，余额不一致时飞书报警
                            Httpfs.HttpFs.send_msg(('Holders Rpc查询余额不一致!\n' + "networkCode:"+res_ag[r]["networkCode"]+"  symbol:"+res_ag[r]["symbol"]+"  address:"+res_ag[r]
                                                    ["address"] + '\n' + "Holders查询余额(查询时间:" + res_ag_time + "):"+res_ag[r]["quantity"] + '\n' + "Rpc查询余额(查询时间:" + res_rpc_ag_time + "):" + res_rpc_ag))
                    else:
                        logger.info("networkCode:" + res[i]["networkCode"] +
                            " | symbol:" + res[i]["symbol"] + " | symbol:" + res[i]["address"] + ' | Rpc查询余额暂不支持!')
