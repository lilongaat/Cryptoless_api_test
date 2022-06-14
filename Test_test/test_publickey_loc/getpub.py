# from pycoin.ecdsa import generator_secp256k1, sign, verify
# from pycoin.ecdsa import possible_public_pairs_for_signature
# import hashlib

# def sha3_256Hash(msg):
#     hashBytes = hashlib.sha3_256(msg.encode("utf8")).digest()
#     return int.from_bytes(hashBytes, byteorder="big")

# # 签名
# def signECDSAsecp256k1(msg, privKey):
#     msgHash = sha3_256Hash(msg)
#     signature = sign(generator_secp256k1, privKey, msgHash)
#     return signature

# # 验签
# def verifyECDSAsecp256k1(msg, signature, pubKey):
#     msgHash = sha3_256Hash(msg)
#     valid = verify(generator_secp256k1, pubKey, msgHash, signature)
#     return valid

# # 恢复公钥
# def recoverPubKeyFromSignature(msg, signature):
#     msgHash = sha3_256Hash(msg)
#     recoveredPubKeys = possible_public_pairs_for_signature(
#         generator_secp256k1, msgHash, signature)
#     return recoveredPubKeys

# privkey = '44298f449dab3993e9965a32c1c4e1d99c1fcece7e228b348516924cecc88f18'
# hash = '0d38b11668876d4a4d0556af796fd3a21d7528dcdd9d8ff6d03c9517a8ca2bef'
# signECDSAsecp256k1(msg=hash,privKey=privkey)
