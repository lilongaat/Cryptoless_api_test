from time import sleep
from bitcoin import *
from bitcoinlib.keys import HDKey
from bitcoinlib.wallets import Wallet
import requests
from Conf import Config
import decimal
import random



# k1 = random_key()
# k2 = random_key()
# p1 = privkey_to_pubkey(k1)
# p2 = privkey_to_pubkey(k2)
# # print(p1,p2)

# pubs = [
#     "02f44bce3eecd274e7aa24ec975388d12905dfc670a99b16e1d968e6ab5f69b266",
#     "0377155e520059d3b85c6afc5c617b7eb519afadd0360f1ef03aff3f7e3f5438dd"
#     ]

# s = mk_multisig_script(pubs,2)
# print(s)

# # s_ = mk_multisig_script(pubs,2,2)
# # print(s_)


# # script =  mk_multisig_script(pubs, 2, 2)
# # address = scriptaddr(script)
# # print(address)




# # 20181002
# mnemonic = "cry buyer grain save vault sign lyrics rhythm music fury horror mansion"
# name = "test"+str(Config.now_timestamp())
# w = Wallet.create(name, keys=mnemonic, network='bitcoin')
# k = w.key_for_path([0, 310])
# print(k.address)


mnemonic = "cry buyer grain save vault sign lyrics rhythm music fury horror mansion"
for i in range(20181002):
    for j in range(20181002):
        sleep(1)
        name = "test"+ str(Config.now_timestamp()) + str(random.randint(0,10000))
        w = Wallet.create(name, keys=mnemonic, network='bitcoin')
        k = w.key_for_path([i, j])
        address = k.address
        url = "https://blockchain.coinmarketcap.com/api/address?address="+address+"&symbol=BTC&start=1&limit=10"
        payload={}
        headers = {
        'Cookie': 'next-i18next=en'
        }
        response = requests.request("GET", url, headers=headers, data=payload)
        received = decimal.Decimal(response.json()["amount_received"])
        balance = decimal.Decimal(response.json()["balance"])
        if received > 0:
            print(str(i) + " + " + str(j) + "+ address:" + address + "  +received:" + str(received))
        if balance > 0:
            print("<--------->" + "\n" + str(i) + " + " + str(j))