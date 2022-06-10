from itertools import cycle
from time import sleep
import os,sys
import pytest
from apscheduler.schedulers.blocking import BlockingScheduler

#Holders-RPC Blances_Check
def job_test_holders_check():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders_check.py", '--alluredir=Report/allurefile'])
 
#Test_ETH_transfers
def job_test_transfer():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_ETH",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure_Testfile')

if __name__ == '__main__':
    sched_cycle = BlockingScheduler()
    # sched_cycle.add_job(job_test_holders_check, 'interval', seconds=10)
    sched_cycle.add_job(job_test_transfer, 'interval', seconds=5, max_instances=10)
    sched_cycle.start()




# if __name__ == '__main__':
    # 死循环
    # for _ in cycle((None,)):
        # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py",'--clean-alluredir', '--alluredir=Report/allurefile'])
        # sleep(5)


    # 打开报告命令：allure serve + 报告存放路径
    # allure serve /Users/lilong/Documents/Test_Api/Report/allurefile


