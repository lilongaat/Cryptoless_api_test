import allure
import pytest
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Common import Http
from Common.Loguru import logger

@allure.feature("Holders测试！")
class Test_holders_check:

    test_data = [
    {
        'Authorization': 'eyJzaWduYXR1cmUiOiIweDk2Y2E5NDU2MTMyMDUwY2YwMzM3YTZhMDYxMmZlZTFhMmZjZWYxNmU3YmU4YzA0MmM5OWI4OWYxZDUzZWE5NTA2ZjZjZWRmNDU3ZTA3MGEzYjdhYjE5Y2QyYmNiMzdmMWZiNWFiZGM2MmVhYmE0NzJhNDZiNWU5NjE1MmZiYzE2MWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTU4NTQyNlxuSXNzdWVkIEF0OiBUdWUsIDcgSnVuIDIwMjIgMTg6MjM6MjYgR01UXG5FeHBpcmF0aW9uIFRpbWU6IFNhdCwgNyBKdW4gMjA0MiAxODoyMzoyNiBHTVQifQ==',
    }
]
    
    @allure.story("查询用户Holders！")
    @pytest.mark.parametrize('param', test_data)
    def test_test01(self,param):
        Authorization = list(param.values())[0]
        logger.info("查询用户(Authorization:" + Authorization + ")的Holders！")
        res = Http.HttpUtils.http_get_holders_by_web3token(Authorization)

        for i in range(len(res)):
            logger.info(res[i])
            # logger.info("networkCode:"+res[i]["networkCode"])
            # logger.info("symbol:"+res[i]["symbol"])
            # logger.info("address:"+res[i]["address"])
            # logger.info("quantity"+res[i]["quantity"])
            assert res[i]["quantity"] == res[i]["quantity"]