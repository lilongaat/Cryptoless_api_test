# import random
 
# #生成随机数，浮点类型
# a = random.uniform(10, 20)
# #控制随机数的精度round(数值，精度)，精度可以自行设定
# print(type(round(random.uniform(0,0.1), random.randint(17,18))))


# import datetime
from apscheduler.schedulers.background import BackgroundScheduler


def job1():
	print('job000')


# 任务调度器
scheduler = BackgroundScheduler()
# Account
scheduler.add_job(job1,trigger='cron',second=0,minute=20,hour=12)
scheduler.start()


# 每天 2 点 30 分 5 秒运行
# scheduler.add_job(job1,trigger='cron',second=0,minute=5,hour=12)
# scheduler.start()
# scheduler.shutdown(wait=False)


# list = [{"address":"0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be","amount":"0.000004","blockHash":"0xbf33a68a3f69d695cb6193e9ef894a875ca7c1ef597c9ce4c5f4ddf7eee3d3cd","blockHeight":"11131283","createdTime":"2022-08-02T09:01:25.000Z","hash":"0xa3e48161f494e1e35e63645df45eb18f909f02aa5ab7259a3988b52faf622ad8","id":"1554391908931289089","isReverted":False,"networkCode":"ETH-RINKEBY","symbol":"ETH","time":"2022-08-02T09:01:18.000Z","type":1,"updatedTime":"2022-08-02T09:01:25.000Z"},{"address":"0xbDb3bd7b3F3DAEADC58D00EF5f15ED9a476B8fe3","amount":"0.00002500002079","blockHash":"0xbf33a68a3f69d695cb6193e9ef894a875ca7c1ef597c9ce4c5f4ddf7eee3d3cd","blockHeight":"11131283","createdTime":"2022-08-02T09:01:25.000Z","hash":"0xa3e48161f494e1e35e63645df45eb18f909f02aa5ab7259a3988b52faf622ad8","id":"1554391908935483393","isReverted":False,"networkCode":"ETH-RINKEBY","symbol":"ETH","time":"2022-08-02T09:01:18.000Z","type":-1,"updatedTime":"2022-08-02T09:01:25.000Z"}]

# amount  = [t.get("amount") for t in list if t.get("address") == "0x6146ca4fc34aaA7a6f9D0417a9A4f10e41b6a7Be" and t.get("blockHeight") == "11131283"]
# print(amount)

# from unicodedata import decimal
# import numpy as np
# np.set_printoptions(suppress=True)

# import decimal
# be = '9999920626.836522719579'
# af = '9999912939.824328702024'
# am = 7687.012194017555

# bd_c = (decimal.Decimal(be))
# af_c = (decimal.Decimal(af))
# am_c =(decimal.Decimal(str(am)))
# assert bd_c - af_c == am_c

