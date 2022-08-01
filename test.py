# import random
 
# #生成随机数，浮点类型
# a = random.uniform(10, 20)
# #控制随机数的精度round(数值，精度)，精度可以自行设定
# print(round(random.uniform(0,1), random.randint(17,18)))


import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def job1():
	print('job1')


scheduler = BackgroundScheduler(daemon=True)
scheduler.start()

# 每天 2 点 30 分 5 秒运行
scheduler.add_job(job1,trigger='cron',second=5,minute=30,hour=21)
scheduler.start()
scheduler.shutdown(wait=False)