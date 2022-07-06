from itertools import cycle
from time import sleep
import os,sys
import pytest
from apscheduler.schedulers.blocking import BlockingScheduler

class Run():
    #Holders-RPC Blances_Check
    def job_test_holders_check():
        pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders_check.py", '--alluredir=Report/allurefile'])
    
    #Test_transfers_ETH
    def job_transfer_eth():
        pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_ETH",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])

    #Test_transfers_IRIS
    def job_transfer_iris():
        pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_transfers_IRIS",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])


if __name__ == '__main__':
    # sched_cycle = BlockingScheduler()
    # sched_cycle.add_job(Run.job_transfer_iris, 'interval', seconds=5)
    # sched_cycle.start()
    
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers/Test_Transfers_ETH",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers/Test_Transfers_IRIS", '--alluredir=Report/Allure_Testfile'])
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers/Test_Transfers_BTC", '--alluredir=Report/Allure_Testfile'])
    # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Cross_chain/Test_bsc_clv",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])
    # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Cross_chain/Test_bsc_matic", '--alluredir=Report/Allure_Testfile'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure_Testfile')
    





# if __name__ == '__main__':
    # 死循环
    # for _ in cycle((None,)):
        # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py",'--clean-alluredir', '--alluredir=Report/allurefile'])
        # sleep(5)


    # 终端打开报告：allure serve + 报告存放路径
    # allure serve /Users/lilong/Documents/Test_Api/Report/allurefile

    # 直接打开报告
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure_Testfile')


