import json
import requests


# address = "0xda9dfa130df4de4673b89022ee50ff26f6ea73cf"
address = "0xa7efae728d2936e78bda97dc267687568dd593f3"

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


for i in range(100):
    txdetail = txlist[i]
    txtxdetail_graphql = [t for t in txlist_graphql if t.get("txHash") == txlist[i]["hash"]]
    if len(txtxdetail_graphql) == 0:
        print("graphql没有找到该交易\n",txlist[i])
    elif len(txtxdetail_graphql) == 1:
        if txdetail["blockNumber"] != str(txtxdetail_graphql[0]["blockNumber"]):
            print("blockNumber ERROR\n",txlist[i])
        if txdetail["blockHash"] != txtxdetail_graphql[0]["blockHash"]:
            print("blockHash ERROR\n",txlist[i])
        if txdetail["from"] == address:
            if txtxdetail_graphql[0]["sign"] != -1:
                print("sign ERROR\n",txlist[i])
            # 非内部交易
            if "gas" in txdetail:
                if str(int(txdetail["value"]) + txdetail["gas"]*int(txdetail["gasPrice"])) != txtxdetail_graphql[0]["amount"]:
                    print("amount+fee ERROR\n",txlist[i])
                    print(str(int(txdetail["value"]) + txdetail["gas_used"]*int(txdetail["gas_price"])))
                    print(txtxdetail_graphql[0]["amount"])
            # 内部交易
            else:
                if (txdetail["value"]) != txtxdetail_graphql[0]["amount"]:
                    print("amount ERROR\n",txlist[i])
                    print(txdetail["value"])
                    print(txtxdetail_graphql[0]["amount"])
        elif txdetail["to"] == address:
            if txtxdetail_graphql[0]["sign"] != 1:
                print("sign ERROR\n",txlist[i])
            if (txdetail["value"]) != txtxdetail_graphql[0]["amount"]:
                print("amount ERROR\n",txlist[i])
                print(txdetail["value"])
                print(txtxdetail_graphql[0]["amount"])
    else:
        print("查询交易数量多条",txlist[i])