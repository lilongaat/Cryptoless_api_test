from pycoin.ecdsa import generator_secp256k1, sign, verify
from pycoin.ecdsa import possible_public_pairs_for_signature
import hashlib

def sha3_256Hash(msg):
    hashBytes = hashlib.sha3_256(msg.encode("utf8")).digest()
    return int.from_bytes(hashBytes, byteorder="big")

# 签名
def signECDSAsecp256k1(msg, privKey):
    msgHash = sha3_256Hash(msg)
    signature = sign(generator_secp256k1, privKey, msgHash)
    return signature

# 验签
def verifyECDSAsecp256k1(msg, signature, pubKey):
    msgHash = sha3_256Hash(msg)
    valid = verify(generator_secp256k1, pubKey, msgHash, signature)
    return valid

# 恢复公钥
def recoverPubKeyFromSignature(msg, signature):
    msgHash = sha3_256Hash(msg)
    recoveredPubKeys = possible_public_pairs_for_signature(
        generator_secp256k1, msgHash, signature)
    return recoveredPubKeys

privatekey = '0xb62cb712741b7e6f60b54728b6fb071c32feb1cd14e8e2c1b08c92230d650e95'
msg = b'hello'
signECDSAsecp256k1(msg=msg,privKey=privatekey)
