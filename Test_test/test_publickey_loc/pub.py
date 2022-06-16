import secp256k1

privkey_str = '1dfb5db671e7d68dda061d8a7e79a57ed9e27449d6e934c3286978ee2873a435'
hash_str = '6b797f3b17ef9d4dd434c51aabf687eb9f3a18b811c4735e6389cd2ec5a4c386'


privkey = secp256k1.PrivateKey(bytes(bytearray.fromhex(privkey_str)))
msg = bytes(bytearray.fromhex(hash_str))

unrelated = secp256k1.ECDSA()

# Create a signature that allows recovering the public key.
recsig = privkey.ecdsa_sign_recoverable(msg)
# Recover the public key.
pubkey = unrelated.ecdsa_recover(msg, recsig)
# Check that the recovered public key matches the one used
# in privkey.pubkey.
pubser = secp256k1.PublicKey(pubkey).serialize()
assert privkey.pubkey.serialize() == pubser

# Check that after serializing and deserializing recsig
# we still recover the same public key.
recsig_ser = unrelated.ecdsa_recoverable_serialize(recsig)
recsig2 = unrelated.ecdsa_recoverable_deserialize(*recsig_ser)
pubkey2 = unrelated.ecdsa_recover(msg, recsig2)
pubser2 = secp256k1.PublicKey(pubkey2).serialize()
assert pubser == pubser2

raw_sig = unrelated.ecdsa_recoverable_convert(recsig2)
unrelated.ecdsa_deserialize(unrelated.ecdsa_serialize(raw_sig))