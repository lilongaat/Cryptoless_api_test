import secp256k1
import time

class Config():

    @staticmethod
    # 获取当前时间戳
    def now_timestamp():
        # ticks = time.time() #原始时间戳
        ticks = int(time.time()) #秒级时间戳
        # ticks = int(round(time.time() * 1000))#毫秒级时间戳
        return ticks
    

    @staticmethod
    # 获取当前时间到微秒
    def now_time():
        ct = time.time()
        local_time = time.localtime(ct)
        data_head = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
        data_secs = (ct - int(ct)) * 1000000
        time_stamp = "%s.%03d" % (data_head, data_secs)
        return time_stamp

if __name__ == '__main__':
    print(Config.now_timestamp())
    print(Config.now_time())
