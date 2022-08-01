from time import sleep
import os,sys
import pytest
import datetime
from apscheduler.schedulers.background import BackgroundScheduler


# 测试报告文件路径
report_file = 'Allure_Testfile_' + str(datetime.date.today())

#Holders-RPC Blances_Check
def job_test_holders_check():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders_check.py", '--alluredir=Report/' + report_file])

#Test_Stake_IRIS
def job_stake_iris():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Stake/Test_Stake_IRIS", '--alluredir=Report/' + report_file])

#Test_Stake_CLV
def job_stake_clv():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Stake/Test_Stake_CLV", '--alluredir=Report/' + report_file])

#Test_transfers_BTC
def job_transfer_btc():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_BTC", '--alluredir=Report/' + report_file])

#Test_transfers_ETH
def job_transfer_eth():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_ETH", '--alluredir=Report/' + report_file])

#Test_transfers_IRIS
def job_transfer_iris():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_transfers_IRIS", '--alluredir=Report/' + report_file])

#Test_transfers_CLV
def job_transfer_clv():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_clv", '--alluredir=Report/' + report_file])

#Assets_Recovery
def job_recovery():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers/test_recovery.py", '--alluredir=Report/' + report_file])

#Reports
def job_report(report_file):
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/' + report_file)


# # 任务调度器
# scheduler = BackgroundScheduler()
# # Stake
# scheduler.add_job(job_stake_iris,trigger='cron',second=9,minute=52,hour=21)
# scheduler.add_job(job_stake_clv,trigger='cron',second=0,minute=0,hour=6)
# # Transfers
# scheduler.add_job(job_transfer_btc,trigger='cron',second=0,minute=30,hour=6)
# scheduler.add_job(job_transfer_eth,trigger='cron',second=0,minute=30,hour=6)
# scheduler.add_job(job_transfer_iris,trigger='cron',second=0,minute=30,hour=6)
# scheduler.add_job(job_transfer_clv,trigger='cron',second=0,minute=30,hour=6)
# # Rcovery
# scheduler.add_job(job_recovery,trigger='cron',second=0,minute=30,hour=7)
# #Reports
# # scheduler.add_job(job_report,trigger='cron',second=0,minute=30,hour=8)
# scheduler.start()





# if __name__ == '__main__':
    # 死循环
    # for _ in cycle((None,)):
        # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py",'--clean-alluredir', '--alluredir=Report/allurefile'])
        # sleep(5)


    # 终端打开报告：allure serve + 报告存放路径
    # allure serve /Users/lilong/Documents/Test_Api/Report/allurefile

    # 直接打开报告
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure_Testfile')


