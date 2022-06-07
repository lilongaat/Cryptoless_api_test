import logging
from loguru import logger
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Common import Conf

class PropogateHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)

nowtime =  Conf.Config.now_time()
logger.add(PropogateHandler(), format=nowtime + " | {message}")