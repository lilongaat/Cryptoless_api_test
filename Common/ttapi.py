import requests
from bs4 import BeautifulSoup

list = []
list_api = []
for i in range(2):
    url = "https://cn.etherscan.com/txsInternal?block=15495641&ps=100&p=" + str(i+1)
    payload={}
    headers = {
    'authority': 'cn.etherscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'max-age=0',
    'cookie': 'ASP.NET_SessionId=0wylskbqpa1faq5sp0p22ti0; _pk_id.10.1f5c=2d110707d6251c3f.1654502290.; _ga=GA1.2.1821908089.1657258798; cf_clearance=9z_WauLTZuEmHonR12UefQJ01syiDAfg9dewfwQR0pw-1661754410-0-150; _pk_ses.10.1f5c=1; __stripe_mid=59bfd5ad-809b-451a-a3be-fff3d78bd515c99b09; etherscan_pwd=4792:Qdxb:AGmcDvIzL9ZE1XMbcpG+n0Bxpj4TFNZ2orhauJQ3izQ=; etherscan_userid=lilongaat; etherscan_autologin=True; __cf_bm=9QH4UxBwK2FWpykTJNd5DsVokMu4WNd54Z1aDMJDT.U-1662449092-0-AaOi6EbTHkYVWo6UiuhDkexvaVEUoCTyEvNm85bA7eG9sYBnXgqjZPAmfFRAnOlTFb1HA+fh4NwZTtQ0hjpwwbo1IpnE7phXCXO6Rg4xYxuMoelGIfOvHcQ9kHcqelOm1A==',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    soup = BeautifulSoup(response.text, 'lxml').body

    for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
            for a in td.find_all("a"):
                if "/tx/" in a.get('href'):
                    hash = a.get('href').split("/tx/")[1]
                    list.append(hash)
                    # print(hash)

# url = "https://eth-mainnet.cryptoless.io/sit/v1/internal/block/transactions?from_block=15495641&to_block=15447129&limit=200"
url = "https://eth-mainnet.cryptoless.io/sit/v1/internal/block/transactions?block_hash=0x4d6e32b8443beb2a54d460e8ca24c999e1ae3891a12832a3140f6eb80ac615be&limit=1000"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)
for i in range(len(response.json()["data"])):
    list_api.append(response.json()['data'][i]["hash"])
    # print(response.json()['data'][i]["hash"])

# print(list)
# print(list_api)

for ii in range(len(list_api)):
    if (list_api[ii] not in list):
        print(list_api[ii])