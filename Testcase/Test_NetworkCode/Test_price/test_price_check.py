from decimal import Decimal
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


@allure.feature("Prices Height!")
class Test_price_height_check:
    if env_type == 0: #测试
        test_data = [
            ('CRV'), 
            ('SUSHI'), 
            ('DOGE'), 
            ('NEXO'), 
            ('SAND'), 
            ('THETA'), 
            ('BAL'), 
            ('BNT'),
            ('ZRX'),
            ('BAT'), 
            ('YFI'), 
            ('GRT'), 
            ('COMP'), 
            ('DAI'), 
            ('MKR'), 
            ('OMG'), 
            ('LINK'), 
            ('UNI'), 
            ('MATIC'), 
            ('IRIS'), 
            ('ATOM'), 
            ('DOT'), 
            ('CLV'), 
            ('BNB'), 
            ('ETH'), 
            ('BTC'),
            ]
    elif env_type == 1: #生产
        test_data = [
            ('CRV'), 
            ('SUSHI'), 
            ('DOGE'), 
            ('NEXO'), 
            ('SAND'), 
            ('THETA'), 
            ('BAL'), 
            ('BNT'),
            ('ZRX'),
            ('BAT'), 
            ('YFI'), 
            ('GRT'), 
            ('COMP'), 
            ('DAI'), 
            ('MKR'), 
            ('OMG'), 
            ('LINK'), 
            ('UNI'), 
            ('MATIC'), 
            ('IRIS'), 
            ('ATOM'), 
            ('DOT'), 
            ('CLV'), 
            ('BNB'), 
            ('ETH'), 
            ('BTC'),
        ]

    @allure.story("prices Height Check!")
    # @allure.title('{test_title}')
    @pytest.mark.parametrize('symbol,', test_data)
    def test_price_check(self,symbol,):

        with allure.step("币安查询价格"):
            bn_price = Httpexplore.BN.BN_price(symbol)
            time_bn = Conf.Config.now_time()
            if bn_price.status_code == 200:
                symbol_bn_price = bn_price.json()["price"]
            else:
                symbol_bn_price = "None"

        with allure.step("network查询价格"):
            price = Http.HttpUtils.assets(symbol=symbol)
            time_assert = Conf.Config.now_time()
            if price.status_code == 200:
                symbol_price_list = [p.get("price") for p in price.json()['list']]
                # logger.debug(symbol_price_list)
                if len(symbol_price_list) == 0:
                    symbol_price = "None"
                else:
                    symbol_price = symbol_price_list[0]
            else:
                symbol_price = "Serve Error " +  str(price.status_code)

        with allure.step("对比币安和assert价格差距"):
            if symbol_bn_price == "None" or symbol_price == "None" or price.status_code != 200:
                Httpfs.HttpFs.send_msg(symbol + ' Symbol_Price异常!\n' + "币安Api查询价格(" + time_bn + "): " + str(symbol_bn_price) + "\n" + "assert查询最新价格(" + time_assert + "): " + str(symbol_price))
            elif (abs(1- (Decimal(symbol_price)/Decimal(symbol_bn_price))))*100 > 3:
                Httpfs.HttpFs.send_msg(symbol + ' Symbol_Price异常!\n' + "币安Api查询价格(" + time_bn + "): " + str(symbol_bn_price) + "\n" + "assert查询最新价格(" + time_assert + "): " + str(symbol_price))




            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
    