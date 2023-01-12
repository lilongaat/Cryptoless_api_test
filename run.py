from time import sleep
import os,sys
import pytest
import datetime


from apscheduler.schedulers.background import BlockingScheduler

path = os.path.abspath(__file__) + ""
print(path.split("/run.py")[0])

# 测试报告文件路径
report_file = 'Allure_Testfile_' + str(datetime.date.today())



# Testcase Block_check
def job_test_block():
    pytest.main(["-vs", path + "/Testcase/Test_NetworkCode/Test_block/test_blockheight_check.py"])


# Testcase Test_User
def job_test_user():
    pytest.main(["-vs", path + "/Testcase/Test_User", '--alluredir=Report/' + report_file])

# Testcase Test_Account
def job_test_account():
    pytest.main(["-vs", path + "/Testcase/Test_Account", '--alluredir=Report/' + report_file])

# Testcase Test_Transfer
def job_transfer_transfer():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Transfer", '--alluredir=Report/' + report_file])

# Testcase Test_Stake
def job_transfer_Stake():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Stake", '--alluredir=Report/' + report_file])

# Testcase Test_Swap
def job_transfer_Swap():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Swap", '--alluredir=Report/' + report_file])


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

    scheduler.add_job(job_test_block,'interval',minute=10)
    
    scheduler.add_job(job_test_user, 'cron', hour=12, minute=00)
    scheduler.add_job(job_test_account, 'cron', hour=12, minute=10)
    scheduler.add_job(job_transfer_transfer, 'cron', hour=12, minute=20)
    scheduler.add_job(job_transfer_Swap, 'cron', hour=12, minute=50)
    scheduler.add_job(job_transfer_Stake, 'cron', hour=13, minute=10)
    scheduler.start()





# if __name__ == '__main__':
    # 死循环
    # for _ in cycle((None,)):
        # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py",'--clean-alluredir', '--alluredir=Report/allurefile'])
        # sleep(5)


    # 终端打开报告：allure serve + 报告存放路径
    # allure serve /Users/lilong/Documents/Test_Api/Report/allurefile

    # 直接打开报告
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure_Testfile')


