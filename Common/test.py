from web3 import Web3

w3 = Web3(Web3.HTTPProvider("https://goerli.infura.io/v3/5d6fbdc545934723b28072344efcf9e5"))

amount = 0.01
from_address = "0xe525E7cd17f6Dc950492755A089E452fd5d9d44f"
private_key = "dca5feaaf2296dca296a015b0ce26d82f89ab8d0f77ec98901a77e96f6e2e2da"
address_to = "0xe525E7cd17f6Dc950492755A089E452fd5d9d44f"
nonce = w3.eth.getTransactionCount(from_address)
value = w3.toWei(amount, 'ether')
balance = w3.eth.getBalance(from_address)

g = w3.eth.gas_price

print("nonce:" + str(nonce) + "\n" + "value:" + str(value))
print(balance)

# tx = {
#   'from': from_address,
#   'to': address_to,
#   'value': value,
#   'gas': 21000,
#   'gasPrice': w3.eth.generate_gas_price(),
#   'nonce': nonce,
#   'chainId': 1
# }
# # signed_txn = w3.eth.account.sign_transaction(tx, private_key=private_key)
# # send = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
# # txid = send.hex()

# raw = w3.eth.account.sign_transaction(tx, private_key=private_key).rawTransaction
# print(raw)