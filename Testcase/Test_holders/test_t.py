import allure
import pytest
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from Common.Loguru import logger

test_data = [
    {
        'Authorization': 'admin00',
    },
    {
        'Authorization': 'admi11n',
    },
    {
        'Authorization': 'admi22',
    },
    {
        'Authorization': 'admin33',
    },
]

@allure.feature("测试！")
class Test_tee:
    
    @pytest.mark.parametrize('param', test_data)
    def test_tyu(self,param): # 和上面的'param'一致
        logger.info(list(param.values())[0]) # 每个字典取值value

