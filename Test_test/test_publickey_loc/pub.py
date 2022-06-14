import secp256k1

privkey_str = '1dfb5db671e7d68dda061d8a7e79a57ed9e27449d6e934c3286978ee2873a435'
hash_str = '6b797f3b17ef9d4dd434c51aabf687eb9f3a18b811c4735e6389cd2ec5a4c386'


privkey = secp256k1.PrivateKey(bytes(bytearray.fromhex(privkey_str)))
msg = bytes(bytearray.fromhex(hash_str))

sig = privkey.ecdsa_sign_recoverable(msg)
sig_tuple = privkey.ecdsa_recoverable_serialize(sig)
print(sig_tuple)

recsig = privkey.ecdsa_sign_recoverable(msg)
recsig_ser = secp256k1.ECDSA().ecdsa_recoverable_serialize(recsig)
print(recsig_ser)
assert sig_tuple == recsig_ser
sigture = bytes.hex(recsig_ser[0]) + "0" + str(recsig_ser[1])
print(len(sigture))