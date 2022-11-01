import json
import requests
from decimal import Decimal


address = "0x0716a17fbaee714f1e6ab0f9d59edbc5f09815c0"

url = "https://api.etherscan.io/api?module=account&action=txlist&address="+address+"&startblock=14570439&endblock=latest&page=1&offset=1000&sort=desc&apikey=UDIG7EZI6J2VBUZIT6AAKXAKTVRQ64J2CF"

response = requests.request("GET", url, headers={}, data={})
assert response.status_code == 200

txlist = response.json()["result"]


url_graphql = "http://13.212.89.244:4005/graphql"

payload_graphql = json.dumps({
  "query": "query getLedgersByAddress\n{\n  getLedgersByAddress(address:\""+address+"\",filter:{},pagination:{limit:10000})\n  {total limit offset data{address amount coinId blockHash blockNumber time txHash sign _id memo}}\n}"
})
headers_graphql = {
  'Content-Type': 'application/json'
}

response_graphql = requests.request("POST", url_graphql, headers=headers_graphql, data=payload_graphql)
assert response_graphql.status_code == 200

txlist_graphql = response_graphql.json()["data"]["getLedgersByAddress"]["data"]

# print(txlist_graphql)

for i in range(len(txlist)):
  txdetail = txlist[i]
  txhash = txlist[i]["hash"]
  txdetail_graphql = [t for t in txlist_graphql if t.get("txHash") == txhash]
  if len(txdetail_graphql) == 0:
    print(i+1,"ERROR 未找到同步txhash")
  elif len(txdetail_graphql) == 1:
    print(i+1,"找到一条同步txhash: ",txhash)
    assert txdetail["blockNumber"] == str(txdetail_graphql[0]["blockNumber"]),txhash
    assert txdetail["blockHash"] == txdetail_graphql[0]["blockHash"],txhash
    if txdetail["from"] == address: #如果是转出地址
      if txdetail["to"] == address: #如果自己转自己
        assert Decimal(txdetail["gas"])*Decimal(txdetail["gasPrice"]) == Decimal(txdetail_graphql[0]["amount"]),txhash
      else: #如果自己转别人
        assert txdetail_graphql[0]["sign"] == -1,txhash
        if "gas" in txdetail: #如果是非内部交易
          assert Decimal(txdetail["value"]) + Decimal(txdetail["gas"])*Decimal(txdetail["gasPrice"]) == Decimal(txdetail_graphql[0]["amount"]),txhash
        if "gas" not in txdetail: #如果是内部交易
          assert txdetail["value"] == txdetail_graphql[0]["amount"],txhash        
    elif txdetail["to"] == address: #如果是转入地址
      assert txdetail_graphql[0]["sign"] == 1,txhash
      assert txdetail["value"] == txdetail_graphql[0]["amount"],txhash
  else:
    print(i+1,"ERROR 找到多条同步txhash")