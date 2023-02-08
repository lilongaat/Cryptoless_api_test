import redis
import sys,os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loguru import logger
from Config.readconfig import ReadConfig

env_type = int(ReadConfig().get_env('type'))
if env_type == 0: # Debug
    redis_host = str(ReadConfig().get_debug('redis_host'))
    redis_port = int(ReadConfig().get_debug('redis_port'))
    redis_password = str(ReadConfig().get_debug('redis_password'))
elif env_type == 1: # Release
    redis_host = str(ReadConfig().get_release('redis_host'))
    redis_port = int(ReadConfig().get_release('redis_port'))
    redis_password = str(ReadConfig().get_release('redis_password'))


class Redis:
    @staticmethod
    def get_verifycode(email:str,):
        r = redis.Redis(host=redis_host,port=redis_port,db=0,password=redis_password,decode_responses=True)
        key = "cryptoless:escrow:message:send:valid:" + email
        verifycode = r.get(key).strip('"')
        return verifycode



if __name__ == '__main__':
    print(type(Redis.get_verifycode("123456@qq.com")),Redis.get_verifycode("123456@qq.com"))


