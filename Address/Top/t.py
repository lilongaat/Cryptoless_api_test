import requests
import json
from decimal import Decimal

url = "https://clover.webapi.subscan.io/api/v2/scan/transfers"

payload = json.dumps({
  "row": 10,
  "page": 0,
  "address": "5HmnWdz7xXfpgHhzrUG6KG89pZE7c66LeLgTvHj7MVCtWdus"
})
headers = {
  'authority': 'clover.webapi.subscan.io',
  'accept': 'application/json, text/plain, */*',
  'accept-language': 'zh-CN',
  'baggage': '',
  'content-type': 'application/json',
  'origin': 'https://clover.subscan.io',
  'referer': 'https://clover.subscan.io/',
  'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
  'sec-ch-ua-mobile': '?0',
  'sec-ch-ua-platform': '"macOS"',
  'sec-fetch-dest': 'empty',
  'sec-fetch-mode': 'cors',
  'sec-fetch-site': 'same-site',
  'sentry-trace': '17871ba09a054b59bbc42ca32fa88a81-b4b2380120084876-0',
  'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
}

response = requests.request("POST", url, headers=headers, data=payload)

list = []
for i in range(len(response.json()["data"]["transfers"])):
    list.append(Decimal(response.json()["data"]["transfers"][i]["amount"]))
print(list)
print(sum(list))
