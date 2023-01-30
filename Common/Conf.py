import csv
import datetime
from decimal import Decimal
from bitcoin import *
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
    #  witnessScript
    def witnessScript(publickeys: list,threshold: int=2):
        witnessScript = mk_multisig_script(publickeys,threshold)
        return witnessScript

    @staticmethod
    #  EVM gasfee计算
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
    

    # privkey1 = 'dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da'
    # privkey2 = '0fbde0fc6a050c10f98ea3fd2921d2b52780667eed2871a132b60c7aab3ff51d'
    # privkey3 = '71b037b45f7d0d35685ff8b68fe0187bf8849c64e6571e0687bf548bc5f0b716'
    # privkey_m = '9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38'
    # hash = '6660564a1b1ed0fb90da99b8562a5c80b8cc1a089fe246c49adae4a5985bc5af'
    # print(Config.sign(privkey1, hash))
    # print(Config.sign(privkey2, hash))
    # print(Config.sign(privkey3, hash))
    # print(Config.sign(privkey_m, hash))

    # privkey = '9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38'
    # hash = '307f98e99df420b142059cf9e6ae8ab8ade0f639d951e824e3340e4354138ad5'
    # print(Config.sign(privkey, hash))


    # print(Config.fee_evm("0x5208","0x1dcd65000"))


    privkey1 = '9cbca176aff8c48ebd9a27c31455e34ebc86e25a17e22b3d65a716fc851ada38'
    # privkey2 = '2f0b3e997953188f8dd6c1eca798be943f6fabb783e2b2cc82275e98a8126442'
    # privkey3 = 'dfdd81763f70078be8c85fe2454de11e7bcf98696c748d133dea50ec7c166a6f'
    hash = '2fce68f4b802f6c95dcafae81c72e339daed4c190b7f17f2cd65bf3d7b046946'
    print(Config.sign(privkey1, hash))
    # print(Config.sign(privkey2, hash))
    # print(Config.sign(privkey3, hash))