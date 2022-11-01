import csv
import datetime
from decimal import Decimal
from gevent import config
from secp256k1 import PrivateKey
import time
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig


class Config():

    @staticmethod
    #读取csv文件前n行
    def reader_csv(filepath:str, rownum:int):
        data = []
        with open(filepath) as csvfile:
            reader = csv.reader(csvfile)
            for i,row in enumerate(reader):
                data.append(row[0])
                if(i >= (rownum - 1)):
                    break
        return data

    @staticmethod
    # 获取当前时间戳
    def now_timestamp():
        # ticks = time.time() #原始时间戳
        ticks = int(time.time())  # 秒级时间戳
        # ticks = int(round(time.time() * 1000))#毫秒级时间戳
        return ticks
    
    @staticmethod
    # 获取当前日期
    def now_time_day():
        today = datetime.date.today()
        return today

    @staticmethod
    # 获取当前时间
    def now_time_second():
        now =  time.localtime()
        now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)
        return now_time

    @staticmethod
    # 获取当前时间到微秒
    def now_time():
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

    @staticmethod
    # 获取定义精度的随机数
    def random_amount(decimals:int):
        num = random.randint(1,9)
        a = '0.'
        for i in range(1,decimals):
            a = a + '0'
        random_amount = a + str(num)
        return random_amount

    @staticmethod
    # fee转换精度
    def amount_decimals(fee:str,decimals:int):
        amount_decimals = int(fee)/(10**decimals) #科学计数法
        amount = ('{:.' + str(decimals) + 'f}').format(amount_decimals)
        return amount

    @staticmethod
    # sign
    def sign(privkey_str: str, hash_str: str):
        privkey = PrivateKey(bytes(bytearray.fromhex(privkey_str)), raw=True)
        msg = bytes(bytearray.fromhex(hash_str))

        # 签名
        sig = privkey.ecdsa_sign_recoverable(msg, raw=True)
        # 序列化
        sig_tuple = privkey.ecdsa_recoverable_serialize(sig)

        signature = bytes.hex(sig_tuple[0]) + "0" + str(sig_tuple[1])

        return signature

    @staticmethod
    def fee_evm(gas:str, gasPrice:str):
        gas_int = int(gas,16)
        gasPrice_int = int(gasPrice,16)
        gasfee = Decimal(gas_int)*Decimal(gasPrice_int)/Decimal(10**18)
        return gasfee

if __name__ == '__main__':
    # print(Config.now_timestamp())
    # print(Config.now_time_day())
    # print(Config.now_time_second())
    # print(Config.now_time())
    # print(type(Config.random_amount(18)),Config.random_amount(18))
    # print(Config.reader_csv("/Users/lilong/Documents/Test_Api/Address/Top/BTC.csv",10))
    

    privkey = '4d87c72cee9d4b257368f448f4f7406d0ce98947eb30fcaa8194319303534b13'
    hash = 'a4a2fcd041343ce2eb27935993273ed72633360f2e7ec57ecf0c3a4ffc309182'
    print(Config.sign(privkey, hash))

    print(Config.fee_evm("0x45c80","0x12c262656"))