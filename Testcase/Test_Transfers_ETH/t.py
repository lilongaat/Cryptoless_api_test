import json

t = {'estimatedFee': '2263864419453000', 'hash': '', 'id': '1535367664837844993', 'networkCode': 'ETH', 'requiredSignings': [{'hash': '52c3ca78d2f0fb96e8b1c29abc824bbb90a4a420c6723a444577d229b309e531', 'publicKeys': ['02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8'], 'threshold': 1}], 'serialized': 'e40b8519199044c9825208948591589a1d9e21073084329dde89ab745c0f5a2e2880808080', 'signatures': [{'hash': '52c3ca78d2f0fb96e8b1c29abc824bbb90a4a420c6723a444577d229b309e531', 'publickeys': ['02488e3f6edb86a6a5e5fe457c71b9d5e40d75558231bfb1489e62694044490fc8'], 'signature': 'e4cfafc377c8285e0a1bce357dac5894125f7bcdd2ced91a6efb154ec37a28f127d179fa40ae1cb0d945669bafc5e41a5766f26a0e223972a6bd94d8be05b0180'}], 'status': 'BUILDING'}


print(type(t))
print(json.dumps(t))
