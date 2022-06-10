from curses import keyname
from secp256k1 import PrivateKey

key = 'b62cb712741b7e6f60b54728b6fb071c32feb1cd14e8e2c1b08c92230d650e95'

privkey = PrivateKey(bytes(bytearray.fromhex(key)))
pubkey_ser = privkey.pubkey.serialize()
pubkey_ser_uncompressed = privkey.pubkey.serialize(compressed=False)

print(key)
print(pubkey_ser.hex())

sig = privkey.ecdsa_sign(b'hello')
print(sig)