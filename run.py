from itertools import cycle
from time import sleep
import pytest
from apscheduler.schedulers.blocking import BlockingScheduler

def job_test_holders():
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py", '--alluredir=Report/allurefile'])
 
def job_test():
    print('tttt!')

if __name__ == '__main__':
    sched = BlockingScheduler()
    sched.add_job(job_test_holders, 'interval', seconds=5)
    # sched.add_job(job_test, 'interval', seconds=3)
    sched.start()




# if __name__ == '__main__':
    # 死循环，休眠时间后进行
    # for _ in cycle((None,)):
        # pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_holders/test_holders.py",'--clean-alluredir', '--alluredir=Report/allurefile'])
        # sleep(5)


    # 打开报告命令：allure serve + 报告存放路径
    # allure serve /Users/lilong/Documents/Test_Api/Report/allurefile


