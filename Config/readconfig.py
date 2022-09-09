import os
import configparser

config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.ini')
config = configparser.ConfigParser()#调用外部的读取配置文件的方法
config.read(config_path, encoding='utf-8')

class ReadConfig():
 
    def get_debug(self, name):
        value = config.get('Debug', name)
        return value

    def get_debug_rpc(self, name):
        value = config.get('Debug_rpc', name)
        return value

    def get_release(self, name):
        value = config.get('Release', name)
        return value

    def get_release_rpc(self, name):
        value = config.get('Release_rpc', name)
        return value
 
 
if __name__ == '__main__':
    print('private_debug中的tester值为:', ReadConfig().get_debug('tester'))
    print('private_debug中的tester值为:', ReadConfig().get_debug_rpc('eth'))