
import os
import pytest


if __name__ == '__main__':
    path = "/Users/lilong/Documents/Test_Api/Testcase/Test_Top_Holders_Check/Test_obaccount_holder.py"
    pytest.main(["-vs", path,'--clean-alluredir','--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')