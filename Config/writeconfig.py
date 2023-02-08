import os
import configparser
import readconfig
env_type = int(readconfig.ReadConfig().get_env('type'))

config_path = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'config.ini')
config = configparser.ConfigParser()#调用外部的读取配置文件的方法
config.read(config_path, encoding='utf-8')

class WriteConfig():
    def update_config(self, name, vaule_):
        if env_type == 0:
            env_value = 'Debug'
        elif env_type == 1:
            env_value = 'Release'
        config[env_value][name] = vaule_
        with open(config_path, 'w') as configfile: config.write(configfile)
        value = config.get(env_value, name)
        return value

 
if __name__ == '__main__':
    print(WriteConfig().update_config('tester','uuhu'))