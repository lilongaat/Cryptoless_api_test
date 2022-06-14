import datetime
import secp256k1
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
        for i in range(2,decimals):
            a = a + '0'
        random_amount = a + str(num)
        return random_amount


    @staticmethod
    # sign
    def sign(privkey_str: str, hash_str: str):
        privkey = secp256k1.PrivateKey(bytes(bytearray.fromhex(privkey_str)))
        msg = bytes(bytearray.fromhex(hash_str))
        sig = privkey.ecdsa_sign_recoverable(msg)
        sig_tuple = secp256k1.ECDSA().ecdsa_recoverable_serialize(sig)
        signature = bytes.hex(sig_tuple[0]) + "0" + str(sig_tuple[1])
        return signature



if __name__ == '__main__':
    # print(Config.now_timestamp())
    # print(Config.now_time_day())
    # print(Config.now_time_second())
    # print(Config.now_time())
    # print(type(Config.random_amount(18)),Config.random_amount(18))
    
    privkey = '1dfb5db671e7d68dda061d8a7e79a57ed9e27449d6e934c3286978ee2873a435'
    hash = '6b797f3b17ef9d4dd434c51aabf687eb9f3a18b811c4735e6389cd2ec5a4c386'
    print(len(Config.sign(privkey, hash)))
    print(Config.sign(privkey, hash))