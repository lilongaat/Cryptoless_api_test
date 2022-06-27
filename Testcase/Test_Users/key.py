import requests
import json

# 批量生成key

host_test = 'http://13.215.207.236:8082'
header = {"Authorization":"eyJzaWduYXR1cmUiOiIweDkwMDczNWEzMDgwZDA3NDdmZjEyZjNjMTRmODZjNzJjOGRmM2NjNzU5MDA0ODI2ODFkNTNmOGYzMWMyMjhiOWUwOWM4OTgyMjI3MDFhYjJmMTFmZmYwZDhmNWE5MWQ4ZThlYmYzNjU0MmY5MmViMDg2YWMwZjFkMDIzMDljZTZiMWIiLCJib2R5IjoiV2ViMyBUb2tlbiBWZXJzaW9uOiAyXG5Ob25jZTogNjM1NzA0OVxuSXNzdWVkIEF0OiBGcmksIDE3IEp1biAyMDIyIDE2OjU1OjMxIEdNVFxuRXhwaXJhdGlvbiBUaW1lOiBUdWUsIDE3IEp1biAyMDQyIDE2OjU1OjMxIEdNVCJ9"}

def creatkey():
    for i in range(100):
        url = host_test + '/escrow/keys'

        body = {
            "count": 10
        }

        res = requests.post(url,json=body,headers=header)
        print(res.text)
        assert res.status_code == 200

def querykey():
    url = host_test + '/escrow/keys'

    res = requests.get(url,headers=header)
    print(json.dumps(res.json()))


# creatkey()
querykey()



