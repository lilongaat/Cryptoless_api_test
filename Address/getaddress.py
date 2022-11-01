import csv
import pandas as pd
import requests
from bs4 import BeautifulSoup
import json


# BTC DOGE LTC BCH
# 网站: https://bitinfocharts.com/zh/top-100-richest-bitcoin-addresses.html
def rich_address(coin:str ,netWork:str ,page_num:int): # 100Xpage_num
  payload={}
  headers = {
    'authority': 'bitinfocharts.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': '_ga=GA1.2.1964905881.1661753193; _gid=GA1.2.459454226.1661753193; _xicah=63aa175b-78ea36d6; __gads=ID=f322c056aa38719e:T=1661753195:S=ALNI_MbB5pZBCzegSAUpiRzpT33ZrgoKbQ; __gpi=UID=00000931c9b34ccd:T=1661753195:RT=1661753195:S=ALNI_Ma_GoPqRU1Qa1n5Mti8vQHBjTvuew',
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

  path = '/Users/lilong/Documents/Test_Api/Address/Top/' + netWork + '.csv'
  with open(path,'w+') as f: # 清空文件
      f.truncate()
      f.close()

  for i in range(page_num): # 文件追加rich address
    url = "https://bitinfocharts.com/zh/top-100-richest-" + coin + "-addresses-" + str(i+1) + ".html"
    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml').body
    # print(soup)

    with open(path,'a+') as f:
      for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
          # print(td.text)
          for a in td.find_all("a"):
            if "/address/" in a.get('href'):
              address = a.get('href').split("/address/")[1]
              csv_write = csv.writer(f)
              csv_write.writerow([address])
      f.close()
  
  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')

# BSC
# 网站:https://bscscan.com/accounts
def rich_address_bsc(page_num:int): # 100Xpage_num
  payload={}
  headers = {
    'authority': 'bscscan.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'ASP.NET_SessionId=psed04jvmiqxjzvkmd254cyo; __cuid=25190bd04d1c4fa99b69c2ade7508645; amp_fef1e8=b4e75291-cb2b-48e3-a622-664208184107R...1gb6sbpmn.1gb6sc4ch.2.1.3; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVrtWyD3G8GoGap; _gid=GA1.2.339125649.1661850943; _gat_gtag_UA_46998878_23=1; __cf_bm=2lAGg4l3VY2KAiS8i.wOU85Pp4C2MG6Qok9Aiae9x4s-1661852025-0-ATw1oc1fpSVLOwgJGLuoqqpOEmNLGTdPreLO3+apuM9ShV6cQsYJQDDBJxEF8o/LYn/WsnuV7tJCTeZkDIX6bE5G8ToIs5bkZl9C9H8JOPaYw3PoVntGxg/dmdQ7yDBTdw==; _ga_PQY6J2Q8EP=GS1.1.1661850943.31.1.1661852054.0.0.0; _ga=GA1.1.1421372093.1656302099; ASP.NET_SessionId=h510wafovgeqkuosl0bfwpqx; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVryhi4UHWZeZcp',
    'referer': 'https://bscscan.com/accounts/100?ps=100',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
  }

  path = "/Users/lilong/Documents/Test_Api/Address/Top/BSC.csv"
  with open(path,'w+') as f: # 清空文件
      f.truncate()
      f.close()
       
  for i in range(page_num):

    url = "https://bscscan.com/accounts/" + str(i+1) + "?ps=100"
    response = requests.request("GET", url, headers=headers, data=payload)
    
    soup = BeautifulSoup(response.text, 'lxml').body
    
    with open(path,'a+') as f:
      for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
          for a in td.find_all("a"):
            if "/address/" in a.get('href'):
              address = a.get('href').split("/address/")[1]
              csv_write = csv.writer(f)
              csv_write.writerow([address])
      f.close()

  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')

# ATOM
# 网站:https://atomscan.com/accounts
def rich_address_atom(page_num:int): # 10Xpage_num
  path="/Users/lilong/Documents/Test_Api/Address/Top/ATOM.csv"
  with open(path,'w+') as f: # 清空文件
    f.truncate()
    f.close()

  for i in range(page_num):
    url = "https://index.atomscan.com/accounts?orderBy=desc&order=total&page=" + str(i+0)+ "&perPage=10&withCounts=true"
    payload={}
    headers = {
      'authority': 'index.atomscan.com',
      'accept': '*/*',
      'accept-language': 'zh-CN,zh;q=0.9',
      'if-none-match': 'W/"b3c-FNq1W0Ei59KOo7kFbvTjiut0xEA"',
      'origin': 'https://atomscan.com',
      'referer': 'https://atomscan.com/',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    with open(path,'a+') as f:
      csv_write = csv.writer(f)
      for j in range(len(response.json()["accounts"])):
        csv_write.writerow([response.json()["accounts"][j]["address"]])
      f.close()

  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')

# MATIC
# https://polygonscan.com/accounts
def rich_address_matic(page_num:int): # 100Xpage_num
  path = "/Users/lilong/Documents/Test_Api/Address/Top/MATIC.csv"
  with open(path,'w+') as f: # 清空文件
    f.truncate()
    f.close()

  for i in range(page_num):
    url = "https://polygonscan.com/accounts/"+str(i+1)+"?ps=100"
    payload={}
    headers={}
    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml').body
    with open(path,'a+') as f:
      for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
          for a in td.find_all("a"):
            if "/address/" in a.get('href'):
              address = a.get('href').split("/address/")[1]
              csv_write = csv.writer(f)
              csv_write.writerow([address])
      f.close()

# ETH
# 网站:https://cn.etherscan.com/accounts
def rich_address_eth(page_num:int): # 100Xpage_num
  path = "/Users/lilong/Documents/Test_Api/Address/Top/ETH.csv"
  with open(path,'w+') as f: # 清空文件
    f.truncate()
    f.close()

  for i in range(page_num):
    url = "https://cn.etherscan.com/accounts/"+str(i+1)+"?ps=100"
    payload={}
    headers = {
      'authority': 'cn.etherscan.com',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'accept-language': 'zh-CN,zh;q=0.9',
      'cookie': 'ASP.NET_SessionId=0wylskbqpa1faq5sp0p22ti0; _pk_id.10.1f5c=2d110707d6251c3f.1654502290.; _ga=GA1.2.1821908089.1657258798; cf_clearance=9z_WauLTZuEmHonR12UefQJ01syiDAfg9dewfwQR0pw-1661754410-0-150; _pk_ses.10.1f5c=1; __cf_bm=wypmwDpJjDPEQEy2JSgStVnr3hDrRz0a_FtMO7txk9I-1661941002-0-AUkx7PrihK10TaeUakKZ5jj0ubCA/4yw06uuhSG3dyv+lmyKEFdBc+2fw5yfBUlQLXKDhMJsCba5MEyakTiNddowGAyKhdjdMWR1nZspZR2bIs6cDnmAm3OsWBabatCTTg==',
      'referer': 'https://cn.etherscan.com/accounts',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'document',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-user': '?1',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
    }
    response = requests.request("GET", url, headers=headers, data=payload)

    soup = BeautifulSoup(response.text, 'lxml').body

    with open(path,'a+') as f:
      for tr in soup.find_all("tr"):
        for td in tr.find_all("td"):
          for a in td.find_all("a"):
            if "/address/" in a.get('href'):
              address = a.get('href').split("/address/")[1]
              csv_write = csv.writer(f)
              csv_write.writerow([address])
      f.close()

  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')

# DOT
# 网站:https://polkadot.subscan.io/
def rich_address_dot(page_num:int): # 25Xpage_num
  path="/Users/lilong/Documents/Test_Api/Address/Top/DOT.csv"
  with open(path,'w+') as f: # 清空文件
    f.truncate()
    f.close()

  for i in range(page_num):
    url = "https://polkadot.webapi.subscan.io/api/v2/scan/accounts"
    payload = json.dumps({
      "filter": "",
      "row": 25,
      "page": i+1,
      "order": "desc",
      "order_field": "balance"
    })
    headers = {
      'authority': 'polkadot.webapi.subscan.io',
      'accept': 'application/json, text/plain, */*',
      'accept-language': 'zh-CN',
      'baggage': '',
      'content-type': 'application/json',
      'origin': 'https://polkadot.subscan.io',
      'referer': 'https://polkadot.subscan.io/',
      'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"macOS"',
      'sec-fetch-dest': 'empty',
      'sec-fetch-mode': 'cors',
      'sec-fetch-site': 'same-site',
      'sentry-trace': 'b7160dcfec744c469952466caa2bae9f-984bb14e2fb6b58c-0',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    
    with open(path,'a+') as f:
      csv_write = csv.writer(f)
      for j in range(len(response.json()["data"]["list"])):
        csv_write.writerow([response.json()["data"]["list"][j]["address"]])
      f.close()

  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')

# CLV
# 网站:https://clover.subscan.io/account
def rich_address_clv(page_num:int): # 25Xpage_num
  path="/Users/lilong/Documents/Test_Api/Address/Top/CLV.csv"
  with open(path,'w+') as f: # 清空文件
    f.truncate()
    f.close()

  for i in range(page_num):
    url = "https://clover.webapi.subscan.io/api/v2/scan/accounts"
    payload = json.dumps({
      "filter": "",
      "row": 25,
      "page": i+1,
      "order": "desc",
      "order_field": "balance"
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
      'sentry-trace': '5772e92145804fadbceb234efcfb1778-91b4be44633156e8-0',
      'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.5112.101 Safari/537.36'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    with open(path,'a+') as f:
      csv_write = csv.writer(f)
      for j in range(len(response.json()["data"]["list"])):
        csv_write.writerow([response.json()["data"]["list"][j]["address"]])
      f.close()

  # 文件地址去重
  frame=pd.read_csv(path, names = ['address'])
  data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
  data.to_csv(path, header=None , index= 0,encoding='utf8')


# rich_address("bitcoin","BTC",100)
# rich_address("dogecoin","DOGE",100)
# rich_address("litecoin","LTC",100)
# rich_address("bitcoin%20cash","BCH",100)
# rich_address_bsc(100)
# rich_address_atom(1000)
rich_address_matic(100)
# rich_address_eth(100)
# rich_address_dot(100)
# rich_address_clv(100)