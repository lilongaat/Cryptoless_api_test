from time import sleep
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(
    os.path.abspath(__file__)))))
from Common import Http,Conf
from Common.Loguru import logger

from Config.readconfig import ReadConfig
env_type = int(ReadConfig().get_env('type'))

@allure.feature("Contacts!")
class Test_create_custodial_account:

    if env_type == 0: #测试
        test_data = [
            ("创建+查询+删除联系人","Goerli_contact_address","GOERLI","0x42B7F34ba0CdE45A5fc0C0B47022A535C01851e5"),
            ("ENS创建+查询+删除联系人","Goerli_contact_ens","GOERLI","lilong.eth"),
            ("批量创建+批量更新+查询+删除联系人",["Goerli_contacts_address","Goerli_contacts_address","MATIC_contacts_address"],["GOERLI","GOERLI","MATIC"],["0xc7854323871686DdA570fa7B0501338238C3D922","0x42E72659ac8535D4b2cBfa38e9039081451Eb373","0x42E72659ac8535D4b2cBfa38e9039081451Eb373"]),
        ]
    elif env_type == 1: #生产
        test_data = [
            ("创建+查询+删除联系人","name","ETH","0xeef04bfaf08a5b8b4aaf8d2e01f1519e507c9de6"),
            ("ENS创建+查询+删除联系人","name","ETH","okex.eth"),
            ("批量创建+批量更新+查询+删除联系人",["ETH_contacts_address","ETH_contacts_address","MATIC_contacts_address"],["ETH","ETH","MATIC"],["0x5ecddc1ac099074ae965d140a7c62bd71b7fc80a","0xc567789a9f58de064706540461d92c0ed7429924","0xc567789a9f58de064706540461d92c0ed7429924"]),
        ]

    @allure.story("Contacts Success!")
    @allure.title('{test_title}')
    @pytest.mark.parametrize('test_title,name,networkCode,address', test_data)
    def test_create_contacts(self, test_title,name,networkCode,address):
        logger.debug(type(address))
        
        if type(address) == str:
            with allure.step("创建联系人"):
                body = {
                    "address": address,
                    "name": "firstname",
                    "networkCode": networkCode
                }
                contactadd = Http.HttpUtils.contacts_add(body)
                assert contactadd.status_code == 200
                id = contactadd.json()['id']

            with allure.step("更新联系人名称"):
                body = {
                    "address": address,
                    "name": name,
                    "networkCode": networkCode
                }
                contactup = Http.HttpUtils.contacts_add(body)
                assert contactup.status_code == 200
                assert contactup.json()['name'] == name

            with allure.step("查询联系人"):
                contactquery = Http.HttpUtils.contacts_query(name,networkCode,address)
                assert contactquery.status_code == 200

            with allure.step("删除联系人"):
                contactdel = Http.HttpUtils.contacts_del(id)
                assert contactdel.status_code == 200

            with allure.step("查询已删除联系人"):
                contactquery2 = Http.HttpUtils.contacts_query(name,networkCode,address)
                assert contactquery2.status_code == 200
                assert len(contactquery2.json()['list']) == 0

            del id
        elif type(address) == list:
            with allure.step("批量创建联系人"):
                bodys = []
                ids=[]
                for i in range(len(address)):
                    bodys.append({
                        "address": address[i],
                        "name": "firstname",
                        "networkCode": networkCode[i]
                    })
                contactss = Http.HttpUtils.contacts_add_batch(bodys)
                assert contactss.status_code == 200
                for j in range(len(contactss.json())):
                    ids.append(contactss.json()[j]['id'])

            with allure.step("批量修改联系人名称"):
                bodys = []
                for i in range(len(address)):
                    bodys.append({
                        "address": address[i],
                        "name": name[i],
                        "networkCode": networkCode[i]
                    })
                contactss = Http.HttpUtils.contacts_add_batch(bodys)
                assert contactss.status_code == 200

            with allure.step("删除联系人"):
                for a in range(len(ids)):
                    contactdels = Http.HttpUtils.contacts_del(ids[a])
                    assert contactdels.status_code == 200

            with allure.step("查询已删除联系人"):
                for b in range(len(name)):
                    contactquerys2 = Http.HttpUtils.contacts_query(name[b],networkCode[b],address[b])
                    assert contactquerys2.status_code == 200
                    assert len(contactquerys2.json()['list']) == 0


        
            

if __name__ == '__main__':
    path = os.path.abspath(__file__) + ""
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    # os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')
