import time
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import pytest

def test():
    now =  time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
    print(now_time)
def test_tick():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Transfers_ETH",'--clean-alluredir', '--alluredir=Report/Allure_Testfile'])

if __name__ == '__main__':
    scheduler = BlockingScheduler()
    # scheduler.add_job(test, 'interval', seconds=2, id=0)
    scheduler.add_job(test_tick, 'interval', seconds=3)
    scheduler.start()
