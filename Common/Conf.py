import datetime
from secp256k1 import PrivateKey
import time
import random


class Config():

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


if __name__ == '__main__':
    # print(Config.now_timestamp())
    # print(Config.now_time_day())
    # print(Config.now_time_second())
    # print(Config.now_time())
    # print(type(Config.random_amount(18)),Config.random_amount(18))
    
    # BTC:dd4e89dbb052b5ba7981c3353b24a0740f6bbc7bfffc20e4808ddb1d42bee65b
    # ETH:ae0f28a2d98211ea6f656ecffa8a821235f78354921d63346c6be48a52610187
    # IRIS:49f38a07d4d0e72d9ecde2baae0506a6aa9718a06a82371eafa30105180ebd85
    # CLV:053d329fb54f8ab36473e74fd4905644a4d5857836274d3116675bad4cfa4273
    privkey = 'f4e19e0bcb5ce78fcc7ca918bd6ef8248a5a832fa532c56727bef5473ea5e6c9'
    hash = 'dc4fad97e84bb9a0b478b55fcd0d460e6de7172e5d46b516083ed70508ecf4d5'
    print(Config.sign(privkey, hash))