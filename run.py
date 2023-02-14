from time import sleep
import os,sys
import pytest
import datetime

from apscheduler.schedulers.background import BlockingScheduler

from Common.Conf import Config
from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

path_ = os.path.abspath(__file__) + ""
path = path_.split("/run.py")[0]
print(path)

# 测试报告文件路径
# report_file = 'Allure_Testfile_' + str(datetime.date.today())
if env_type == 0:
    report_file = 'Allure_normal'
    port = '42431'
elif env_type == 1:
    report_file = 'Allure'
    port = '42432'


# Update token
def job_update_token():
    pytest.main(["-vs", path + "/Testcase/test_update_ authorization.py"])

# Testcase Block_check
def job_test_block():
    pytest.main(["-vs", path + "/Testcase/Test_NetworkCode/Test_block/test_blockheight_check.py"])

# Testcase Prices_check
def job_test_prices():
    pytest.main(["-vs", path + "/Testcase/Test_NetworkCode/Test_price/test_price_check.py"])

# Testcase Test_User
def job_test_user():
    pytest.main(["-vs", path + "/Testcase/Test_User",'--clean-alluredir', '--alluredir=Report/' + report_file])

# Testcase Test_Account
def job_test_account():
    pytest.main(["-vs", path + "/Testcase/Test_Account", '--alluredir=Report/' + report_file])

# Testcase rich_holder_check
def job_test_rich():
    pytest.main(["-vs", path + "/Testcase/Test_Top_Holders_Check", '--alluredir=Report/' + report_file])

# Testcase Test_Transfer
def job_transfer_transfer():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Transfer", '--alluredir=Report/' + report_file])

# Testcase Test_Stake
def job_transfer_Stake():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Stake", '--alluredir=Report/' + report_file])

# Testcase Test_Swap
def job_transfer_Swap():
    pytest.main(["-vs", path + "/Testcase/Test_Cloud/Test_Swap", '--alluredir=Report/' + report_file])

# port
def job_kill_port():
    command='''kill -9 $(netstat -nlp | grep :'''+str(port)+''' | awk '{print $7}' | awk -F"/" '{ print $1 }')'''
    os.system(command)
    os.exit()
    # Config.kill_process(port)

# Allure
def job_allure():
    os.system(f'allure serve ' + path + '/Report/' + report_file + ' -p ' + port)


if __name__ == "__main__":
    scheduler = BlockingScheduler(timezone="Asia/Shanghai")

    # 间隔时间运行
    scheduler.add_job(job_test_rich,'interval',seconds=600)
    scheduler.add_job(job_test_prices,'interval',seconds=600)
    # 固定时间运行
    scheduler.add_job(job_update_token, 'cron', hour=8, minute=00)
    scheduler.add_job(job_test_user, 'cron', hour=8, minute=1)
    scheduler.add_job(job_test_account, 'cron', hour=8, minute=20)
    scheduler.add_job(job_test_rich, 'cron', hour=8, minute=25)
    scheduler.add_job(job_transfer_transfer, 'cron', hour=8, minute=40)
    scheduler.add_job(job_transfer_Swap, 'cron', hour=9, minute=20)
    scheduler.add_job(job_transfer_Stake, 'cron', hour=9, minute=40)
    scheduler.add_job(job_kill_port,'cron', hour=10, minute=00)
    scheduler.add_job(job_allure, 'cron', hour=10, minute=1)
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


