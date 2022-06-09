import requests


url = "http://54.254.26.12:8545"
headers = {
        "Content-Type":"application/json",
        }
data = {
	"jsonrpc":"2.0",
	"method":"eth_getBalance",
	"params":[
		"0x407d73d8a49eeb85d32cf465507dd71d507100c1", 
		"latest"
	],
	"id":1
}
 
res = requests.post(url=url,json=data,headers=headers)
print(res.text)