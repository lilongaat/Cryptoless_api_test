import sys,os,json
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Common import Http,Httprpc
from Common.Loguru import logger

class Test_holders_check:
    
    def test_test01(Authorization):
        logger.info("查询用户的Holders！(Authorization:" + Authorization)
        res = Http.HttpUtils.http_get_holders_by_web3token(Authorization)


        for i in range(len(res)):
            # logger.info(res[i])
            logger.info("networkCode:"+res[i]["networkCode"])
            logger.info("symbol:"+res[i]["symbol"])
            logger.info("address:"+res[i]["address"])
            logger.info("quantity"+res[i]["quantity"])
            assert res[i]["quantity"] == res[i]["quantity"]


if __name__ == '__main__':
    # 没有资产
    Authorization = 'eyJzaWduYXR1cmUiOiIweDEzMDZjNGRlMzhjNTE2ZTg0ZDkyMmRjMWJjZjcyNGE5MjgxMGI5MjM3NTdhZDBiZDdjZGEzNzRiMGEyOGExMTg1Njk5MDliZTQ5NDMwNzcyZjgzNzI5M2U1MjU5ZGRlNDk1ZWJiMzViNzgzOTAwYzU2MTkxNWI2OGU1ZTY0MWQ1MWMiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogOTExMzczNDNcbklzc3VlZCBBdDogV2VkLCA4IEp1biAyMDIyIDEwOjIyOjA5IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBTdW4sIDggSnVuIDIwNDIgMTA6MjI6MDkgR01UIn0='
    # 全部资产
    Authorization1 = 'eyJzaWduYXR1cmUiOiIweDk2Y2E5NDU2MTMyMDUwY2YwMzM3YTZhMDYxMmZlZTFhMmZjZWYxNmU3YmU4YzA0MmM5OWI4OWYxZDUzZWE5NTA2ZjZjZWRmNDU3ZTA3MGEzYjdhYjE5Y2QyYmNiMzdmMWZiNWFiZGM2MmVhYmE0NzJhNDZiNWU5NjE1MmZiYzE2MWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTU4NTQyNlxuSXNzdWVkIEF0OiBUdWUsIDcgSnVuIDIwMjIgMTg6MjM6MjYgR01UXG5FeHBpcmF0aW9uIFRpbWU6IFNhdCwgNyBKdW4gMjA0MiAxODoyMzoyNiBHTVQifQ=='

    Test_holders_check.test_test01(Authorization1)