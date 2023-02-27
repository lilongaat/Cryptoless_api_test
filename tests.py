# # -*- coding: utf-8 -*-
# import requests
# import json
 
# url = 'http://54.169.157.249:8888/context/api/webhooks/'
# headers = {'Content-Type': 'application/json;charset=utf-8','Authorization':'eyJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTYxOTg4OTM3ODkxMzYyNDA2NVxuSXNzdWVkIEF0OiBNb24sIDMwIEphbiAyMDIzIDAyOjQ0OjU4IEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBUaHUsIDI3IEphbiAyMDMzIDAyOjQ0OjU4IEdNVCIsInNpZ25hdHVyZSI6IjB4MjY5ODRiNzUyNjUwYjQ5OTMyMTJhMThhZTVjNTM0MWE3NDhkMjUwMzMzN2MxMmZkNWQxMDAxOGI4MGNhM2E5NjIzZDIwYTU4ZTA4Zjc0NWI0ODViMTNjZTEzNzA1YjEyZDdjNzQ4ZmI2YjVjYTUxMzg3NDc0NjdlY2JlNWQ0YWYxYyJ9'}
# data = {"definitions":{"eventsFilter":["balance-transaction-updated"]}}
# w = requests.post(url=url,headers=headers,json=data).content
# print(w)


# import os

# def killport(port):
#     '''root authority is required'''
#     command='''kill -9 $(netstat -nlp | grep :'''+str(port)+''' | awk '{print $7}' | awk -F"/" '{ print $1 }')'''
#     os.system(command)
    
# killport(62626)

# def get_pid(port):
# 	#其中\"为转义"
#     pid = os.popen("netstat -nlp | grep :%s | awk '{print $7}' | awk -F\" / \" '{ print $1 }'" % (port)).read().split('/')[0]
#     return int(pid)

# get_pid("50720")

# pid=os.system('netstat -aon|findstr "50720"')#25端口号
# print(pid)#输出进程

# port = "50720"
# command="kill -9 $(netstat -nlp | grep :"+str(port)+" | awk '{print $7}' | awk -F'/' '{{ print $1 }}')"
# os.system(command)

# out=os.system('tasklist|findstr "3316"')#3316进是程
# print(out)#输出程序名字
# out=os.system('taskkill /f /t /im MESMTPC.exe')#MESMTPC.exe程序名字
# print(out)#

# import websocket

# def on_message(wsapp, message):
#     print(message)

# host = "ws://54.169.157.249:8888/context/webhook"
# wsapp = websocket.WebSocketApp(host,
# subprotocols=["eyJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogMTYwMTA0MzkzMDI4NzQxMTIwMlxuSXNzdWVkIEF0OiBGcmksIDkgRGVjIDIwMjIgMDI6Mzk6NTMgR01UXG5FeHBpcmF0aW9uIFRpbWU6IE1vbiwgNiBEZWMgMjAzMiAwMjozOTo1MyBHTVQiLCJzaWduYXR1cmUiOiIweGU1OWE1Nzk4OGNhZWU4NmFmYzA3NzlhOTE4MDA5MDRmNjc3NmUxZGMxYTc5NGE2MjllY2Y5YmI0ZjAyZDllYjcwZDBiMGZiNDAxNjQ4NTc5ZTFiZDkzMmU2NmU0NjdjMzFkMDlmOGNjM2EwOGVjN2U1NGY2ZTJhNTM5ZWVjNTA5MWMifQ=="], on_message=on_message)
# wsapp.run_forever()  






# from ecdsa import SigningKey, SECP256k1

# sk = SigningKey.generate(curve=SECP256k1)
# vk = sk.verifying_key

# msg = b"Some arbitrary message"
# signature = sk.sign(msg)

# print("Signing (Private) key: ", sk.to_string().hex())
# print("Verifying (Public) key: ", vk.to_string().hex())
# print("Signature: ", signature.hex())
# print(vk.verify(signature, msg))



from eth_keys import keys

pk = keys.PrivateKey(b'\x0c' * 32)
vk = pk.public_key
add = vk.to_checksum_address()
signature = pk.sign_msg(b'a message')

print('pk:',pk)
print('vk:',vk)
print('add:',add)
print('signature:',signature)

vk2 = signature.recover_public_key_from_msg(b'a message')
print('vk2:',vk2)