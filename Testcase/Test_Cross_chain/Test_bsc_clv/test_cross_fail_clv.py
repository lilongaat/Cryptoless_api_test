from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))))
from Common import Http, Conf
from Common.Loguru import logger


@allure.feature("Cross_Chain_Success!")
class Test_cross_success_usdc:
    test_data = [
        # 测试
        ("CLV在CLVP-BSC间跨链交易(maximum)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],"CLV-P","CLV","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","BSC","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","maximum",400),
        ("CLV在BSC-CLVP间跨链交易(maximum)!",["2f5dbc9722a4c23977e188565eaacb51b905e11927a5089f84df1c4aa1f07b0e"],"BSC","CLV","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","CLV-P","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","maximum",400),
        ("CLV在CLVP-BSC间跨链交易(maximum)!",["ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187"],"CLV-P","CLV","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","BSC","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","100000",400),
        ("CLV在BSC-CLVP间跨链交易(maximum)!",["2f5dbc9722a4c23977e188565eaacb51b905e11927a5089f84df1c4aa1f07b0e"],"BSC","CLV","0x8d2cc82494299e0b9865d7bfd6131c1ab0c2c4f1","CLV-P","0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","100000",400),
    ]

    @allure.story("Cross_Chain_Success!")
    @allure.title('跨链交易:{test_title}')
    @pytest.mark.parametrize('test_title,privatekey,networkCode,symbol,from_add,tonetworkCode,to_add,amount,status_code_check', test_data)
    def test_crosschain(self,test_title,privatekey,networkCode,symbol,from_add,tonetworkCode,to_add,amount,status_code_check):
        
        with allure.step("构建交易——cross chain:{networkCode}-->{tonetworkCode}"):
            res = Http.HttpUtils.post_crosschain(networkCode,symbol,from_add,tonetworkCode,to_add,amount)
            assert res.status_code == status_code_check