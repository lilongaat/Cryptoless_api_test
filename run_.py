import os
import datetime
import pytest

path = os.path.abspath(__file__) + ""
print(path.split("/run_.py")[0])

path_account = path.split("/run_.py")[0] + "/Testcase/Test_Account" 
print(path_account)

path_transfer = path.split("/run_.py")[0] + "/Testcase/Test_Cloud/Test_Transfer"

path_stake = path.split("/run_.py")[0] + "/Testcase/Test_Cloud/Test_Stake"

path_swap = path.split("/run_.py")[0] + "/Testcase/Test_Cloud/Test_Swap"


if __name__ == '__main__':
    # 测试报告文件路径
    report_file = 'Allure_Testfile_' + str(datetime.date.today())

    # pytest.main(["-vs", path_account, '--alluredir=Report/' + report_file])
    pytest.main(["-vs", path_transfer, '--alluredir=Report/' + report_file])
    # pytest.main(["-vs", path_stake, '--alluredir=Report/' + report_file])
    # pytest.main(["-vs", path_swap, '--alluredir=Report/' + report_file])
    # pytest.main(["-vs", path_swap,'--clean-alluredir', '--alluredir=Report/' + report_file])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/' + report_file)