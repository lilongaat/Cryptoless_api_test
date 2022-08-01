import os
import datetime
import pytest

path = "/Users/lilong/Documents/Test_Api/Testcase/Test_Swap/Test_Swap_MATIC"

if __name__ == '__main__':
    # 测试报告文件路径
    report_file = 'Allure_Testfile_' + str(datetime.date.today())

    pytest.main(["-vs", path,'--clean-alluredir', '--alluredir=Report/' + report_file])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/' + report_file)