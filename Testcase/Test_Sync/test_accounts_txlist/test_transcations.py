import json
import requests

address = "0x0716a17fbaee714f1e6ab0f9d59edbc5f09815c0"

# url = "https://eth-mainnet.cryptoless.io/v1/account/"+address+"/transactions?to_block=latest&limit=1000"
# payload={}
# headers = {}
# response = requests.request("GET", url, headers=headers, data=payload)

url_graphql = "http://13.212.89.244:4005/graphql"
payload_graphql = json.dumps({
  "query": "query getLedgersByAddress\n{\n  getLedgersByAddress(address:\""+address+"\",filter:{},pagination:{limit:10000})\n  {total limit offset data{address amount coinId blockHash blockNumber time txHash sign _id memo}}\n}"
})
headers_graphql = {
  'Content-Type': 'application/json'
}
response_graphql = requests.request("POST", url_graphql, headers=headers_graphql, data=payload_graphql)
assert response_graphql.status_code == 200


# url_ = "http://13.215.207.236:8888/escrow/api/transactions?categoryId=&network=&limit=1000"
# payload_={}
# headers_ = {
#    'Authorization': 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIxNTczOTM3MDIxNzEzNzc2NjQyIiwiZXhwIjoxNjY0Njk1NjE2LCJpYXQiOjE2NjQwOTA4MTYsInVzZXJJZCI6MTU3MzkzNzAyMTcxMzc3NjY0Mn0.TfkTJsH4rp4FCmciMn1BUVlnev1JPI7glaTUjyVUz8M',
#    'User-Agent': 'apifox/1.0.0 (https://www.apifox.cn)'
# }

# response_ = requests.request("GET", url_, headers=headers_, data=payload_)
# assert response_.status_code == 200

# tx = [r for r in response_.json() if address in r.get("balanceChanges")]
# print(tx)

txlist = []
for i in range(len(response_graphql.json()["data"]["getLedgersByAddress"]["data"])):
    txHash = response_graphql.json()["data"]["getLedgersByAddress"]["data"][i]["txHash"]
    txlist.append(txHash)
print(txlist)