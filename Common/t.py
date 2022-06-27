from secp256k1 import PrivateKey

key = '9365d91088ca52629cd2f22bb14fda4efecf8905d53734e115cb9e1c8bb5b580'
msg = '08b9b4d2f055554acb611d8b353897d3a76638aa950e209a0fef2705e2f3b955'

privkey = PrivateKey(bytes(bytearray.fromhex(key)), raw=True)
s = privkey.ecdsa_sign_recoverable(bytes(bytearray.fromhex(msg)), raw=True)
ss = privkey.ecdsa_recoverable_serialize(s)
print(bytes.hex(ss[0]))