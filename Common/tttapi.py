from bitcoin import *
from bitcoinlib.keys import HDKey


k1 = random_key()
k2 = random_key()
p1 = privkey_to_pubkey(k1)
p2 = privkey_to_pubkey(k2)
# print(p1,p2)

pubs = [
    "02e8852463021b47fe5214c599e87e431f2eb1219044946bbff397afd0518b85a6",
    "0231e263a7e95bf5107b88b85b49918841b937305cce5dae7dd7ba9b86fc460f70"
    ]

s = mk_multisig_script(pubs,2)
print(s)


# script =  mk_multisig_script(pubs, 2, 2)
# address = scriptaddr(script)
# print(address)