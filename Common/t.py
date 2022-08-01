print((int("0x000000000000000000000000000000000000000000002dfb683ebdaddc5e1956",16)))

import web3

# totalSupply   balanceOf  decimals
method_id = web3.Web3.keccak(text = "balanceOf()").hex()[:10]
print(method_id)
address = "0xC88F7666330b4b511358b7742dC2a3234710e7B1"
data = method_id + "".zfill(20) + address[2:]
print(data)


# from web3 import Web3
# import ssl
# import certifi
# ssl_context = ssl.create_default_context()
# ssl_context.load_verify_locations(certifi.where())

# print(Web3(Web3.WebsocketProvider("wss://mainnet.infura.io/ws/v3/f8167b1c15ae4716976dd317d03b3e7f",websocket_kwargs={"ssl":ssl_context})).eth.block_number)
# # print(Web3(Web3.WebsocketProvider("wss://eth-mainnet.cryptoless.io")).eth.block_number)

# print(Web3(Web3.HTTPProvider("https://mainnet.infura.io/v3/f8167b1c15ae4716976dd317d03b3e7f",request_kwargs={'timeout': 100})).eth.block_number)


# a = [{"a":1,"b":2},{"a":2,"b":9},{"a":3,"b":87},{"a":3,"b":92},{"a":0,"b":2}]
# u = [x.get("b") for x in a if x.get("a") == 1]
# print(u)

# t = []
# t.append({"tpo":u})
# print(t)