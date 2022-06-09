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

    test_users = [
        {
            'Authorization': 'eyJzaWduYXR1cmUiOiIweGRmMDcwN2YzZDlmOWU3MmVjMmVmMmM1NTVmMzU2MzlmMjBkOTJmZjU0OWIzODA5NjI4N2U0MWJiYmM2ZDMzOTM1ZDgzN2FlMGRiYjhjNDM3MzMwNDg4ZjYzNmZmYTAwYmRkNGYxM2Q5ZTkxNWQwZDUzODJkOGFmZDJiOGUyMDdhMWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogODcwNzA5Mzhcbklzc3VlZCBBdDogVGh1LCA5IEp1biAyMDIyIDE1OjAxOjI0IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBNb24sIDkgSnVuIDIwNDIgMTU6MDE6MjQgR01UIn0=',
        }
    ]

    @allure.story("Holders Rpc查询用户资产信息检查!")
    @pytest.mark.parametrize('param', test_users)
    def test_balances_check(self, param):
        Authorization = list(param.values())[0]
        # holders接口查询用户所有资产信息
        logger.info("查询用户的Holders！(Authorization:" + Authorization)
        res = Http.HttpUtils.http_get_holders_by_web3token(Authorization)
        res_time = Conf.Config.now_time()

        logger.info(res)

        for i in range(len(res)):
            logger.info("<--------------->" + "networkCode:"+res[i]["networkCode"]+" | symbol:"+res[i]["symbol"] +
                        " | address:"+res[i]["address"])
            logger.info("Holders查询余额:"+res[i]["quantity"])

            # RPC接口查询用户资产信息
            res_rpc = Httprpc.HttpRpcUtils.httprpc_getbalance(
                res[i]["networkCode"], res[i]["address"], 'latest')
            rpc_time = Conf.Config.now_time()
            logger.info("Rpc查询余额:" + res_rpc)

            # holders和Rpc资产信息对比
            if res[i]["quantity"] != res_rpc:
                # holders和Rpc资产信息不一致发消息到飞书
                Httpfs.HttpFs.send_msg('Holders Rpc查询余额!\n' + "networkCode:"+res[i]["networkCode"]+"  symbol:"+res[i]["symbol"]+"  address:"+res[i]
                                       ["address"] + '\n' + "Holders查询余额(查询时间:" + res_time + "):"+res[i]["quantity"] + '\n' + "Rpc查询余额(查询时间:" + rpc_time + "):" + res_rpc)
                logger.error('Holders Rpc查询余额不一致!')
            else:
                logger.info('Holders Rpc查询余额一致!')
