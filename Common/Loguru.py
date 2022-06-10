import logging
from loguru import logger
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Common import Conf

class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)

today = str(Conf.Config.now_time_day())
nowtime =  Conf.Config.now_time()

# 写入日志文件
logger.add("/Users/lilong/Documents/Test_Api/Report/log/" + "log-" + today + ".log",
                  rotation="00:00",#每天00:00创建新的日志文件
                  encoding="utf-8",#避免中文乱码
                  level="ERROR",#控制写入日志等级
                  enqueue=True,#异步写入
                  compression="zip",#日志压缩格式
                  retention="10 days")#日志最长保留时间
# 输出到控制台
logger.add(PropogateHandler(), format=nowtime + " | {message}")