from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler


def func(name):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(now + f" Hello world, {name}")


scheduler = BlockingScheduler()
# 三秒执行一次
scheduler.add_job(func, 'interval', seconds=3, args=["desire"])
scheduler.start()
