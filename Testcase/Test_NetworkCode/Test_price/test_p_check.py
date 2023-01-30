from time import sleep
from decimal import Decimal
import json
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

    def test_price_check():

        symbol_list = []
        cryptocurrencies = Http.HttpUtils.assets(size="100")
        for i in range(len(cryptocurrencies.json()['list'])):
            symbol_list.append(cryptocurrencies.json()['list'][i]["symbol"])
        print(symbol_list)

        symbol_list = ['CRV', 'SUSHI', 'DOGE', 'NEXO', 'SAND', 'THETA', 'BAL', 'BNT', 'ZRX', 'BAT', 'YFI', 'GRT', 'COMP', 'DAI', 'MKR', 'OMG', 'LINK', 'UNI', 'MATIC', 'IRIS', 'ATOM', 'DOT', 'CLV', 'BNB', 'ETH', 'BTC']
        Dsymbol_list = ['LEO', 'HT', 'WBTC', 'BTT']

        # symbol_price_caps = {}
        # for i in range(len(symbol_list)):

        #     symbol = symbol_list[i]
        #     cryptocurrencies = Http.HttpUtils.get_cryptocurrencies(symbol)
        #     symbol_price = cryptocurrencies.json()[0]["price"]

        #     bn_price = Httpexplore.BN.BN_price(symbol)
        #     assert bn_price.status_code == 200
        #     symbol_bn_price = bn_price.json()["price"]

        #     p =  (abs(1- (Decimal(symbol_price)/Decimal(symbol_bn_price))))*100 # 价格差距百分比
        #     if  p > 3:
        #         symbol_price_caps.update({symbol+"_price":symbol_price,symbol+"_BN_price":symbol_bn_price,symbol+"_percent_gap":str(Decimal(p).quantize(Decimal("0.00")))+"%"})

        # # Httpfs.HttpFs.send_msg('Price 异常!\n' + str(symbol_price_caps))
        # if len(symbol_price_caps) > 0:
        #     Httpfs.HttpFs.send_msg('Price 差距大于3%!\n' + str(symbol_price_caps))


if __name__ == '__main__':
    Test_price_check.test_price_check()