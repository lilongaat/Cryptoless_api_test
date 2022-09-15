import requests

url = "https://api.opensea.io/api/v1/asset/0xb47e3cd837ddf8e4c57f05d70ab865de6e193bbb/1/owners?limit=20&order_by=created_date&order_direction=desc"

response = requests.get(url)

print(response.text)