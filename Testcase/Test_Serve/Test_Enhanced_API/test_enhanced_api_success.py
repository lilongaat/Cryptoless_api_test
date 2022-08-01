import json
import requests
import web3
import pytest_check
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common import Http_Enhancedapi,Httprpc
from Common.Loguru import logger


url_aichemy = "https://eth-mainnet.g.alchemy.com/v2/ecaUhEy8uO_z30FhA3OxmNKDptoqpBdZ"

# tokenInfo
@allure.feature("Enhanced_API_Success!")
class Test_Enhanced_API_tokenInfo:

    test_data = [
        ("查询TokenInfo ERC20(USDT)","0xdAC17F958D2ee523a2206206994597C13D831ec7"),
        ("查询TokenInfo ERC20(USDC)","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"),
        ("查询TokenInfo ERC20(BNB)","0xB8c77482e45F1F44dE1745F52C74426C631bDD52"),
        ("查询TokenInfo ERC20(BUSD)","0x4Fabb145d64652a948d72533023f6E7A623C7C53"),
        ("查询TokenInfo ERC20(HEX)","0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39"),
        ("查询TokenInfo ERC20(DAI)","0x6B175474E89094C44Da98b954EedeAC495271d0F"),
        ("查询TokenInfo ERC20(SHIB)","0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE"),
        ("查询TokenInfo ERC20(MATIC)","0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0"),
        ("查询TokenInfo ERC20(THETA)","0x3883f5e181fccaF8410FA61e12b59BAd963fb645"),
        ("查询TokenInfo ERC20(OKB)","0x75231F58b43240C9718Dd58B4967c5114342a86c"),

        ("查询TokenInfo ERC721(BS)","0xe381B9b1A7f778b27543Dcf3Da7F4305F38e0233"),
        ("查询TokenInfo ERC721(ASOH)","0x82Cb9D20862641301C987f0b096086d32bC11B65"),
        ("查询TokenInfo ERC721(MOON)","0x12b180b635dD9f07a78736fB4E43438fcdb41555"),
        ("查询TokenInfo ERC721(LMP)","0x33c6Eec1723B12c46732f7AB41398DE45641Fa42"),
        ("查询TokenInfo ERC721(LNRBST)","0xF3a57eaf64d2f0bE4Eb9904adf4955B08841584E"),
        ("查询TokenInfo ERC721(SUPAPE)","0x57928f060910f9f7714fD545969e152Dd3655C28"),
        ("查询TokenInfo ERC721(HHOS1)","0x929832b1f1515cf02c9548A0fF454f1B0E216B18"),
        ("查询TokenInfo ERC721(OfficeHrs)","0xA6C1C8ef0179071c16E066171d660dA4ad314687"),
        ("查询TokenInfo ERC721(FREEMINTBOT)","0xfDadC8e89a75D9d0E97B2aead25Feb10660f648F"),
        ("查询TokenInfo ERC721(HERTZ)","0x28B119e69748b17E9A33936EDf0180f2eaB9b6Cc"),

        ("查询TokenInfo ERC1155(OPENSTORE)","0x495f947276749Ce646f68AC8c248420045cb7b5e"),
        ("查询TokenInfo ERC1155(TIGER)","0x1e52F7A450b08b1B249A4f4f54518fC5278C2285"),
        ("查询TokenInfo ERC1155(LL)","0x76BE3b62873462d2142405439777e971754E8E77"),
        ("查询TokenInfo ERC1155(PUZLPARTS)","0x44e6E5FAA5bf7b401fB3E98C9599AE1B2c3dC7Cc"),
        ("查询TokenInfo ERC1155(F1DTI)","0x2aF75676692817d85121353f0D6e8E9aE6AD5576"),
        ("查询TokenInfo ERC1155(ASSET)","0xa342f5D851E866E18ff98F351f2c6637f4478dB5"),
        ("查询TokenInfo ERC1155(WtoB)","0xDe95471123ce8BD81AD8e7BA553e019dA110b654"),
        ("查询TokenInfo ERC1155(RARI)","0xB66a603f4cFe17e3D27B87a8BfCaD319856518B8"),
        ("查询TokenInfo ERC1155(ZPR NFT)","0xF1F3ca6268f330fDa08418db12171c3173eE39C9"),
        ("查询TokenInfo ERC1155(BAPUTIL)","0x2923c3e5A0F10bc02d8c90287b2Af45Cd579dEc4"),
    ]

    @allure.story("Enhanced_API_tokenInfo!")
    @allure.title('{test_title}-token_address:{token_address}')
    @pytest.mark.parametrize('test_title,token_address', test_data)
    def test_tokenInfo(self, test_title,token_address):

        with allure.step("Query TokenInfo!"):
            res = Http_Enhancedapi.HttpUtils.get_tokenInfo(token_address)
            assert res.status_code == 200
            res_ethplorer = Http_Enhancedapi.HttpUtils.get_tokenInfo_ethplorer(token_address)
            assert res_ethplorer.status_code == 200
        
        with allure.step("TokenInfo Check!"):
            pytest_check.equal(res.json()["address"],res_ethplorer.json()["address"],"address Check error!")
            pytest_check.equal(res.json()["name"],res_ethplorer.json()["name"],"name Check error!")
            pytest_check.equal(res.json()["symbol"],res_ethplorer.json()["symbol"],"symbol Check error!")
            pytest_check.equal(res.json()["decimals"],int(res_ethplorer.json()["decimals"]),"decimals Check error!")
            pytest_check.equal(res.json()["total_supply"],res_ethplorer.json()["totalSupply"],"totalSupply Check error!")
            # pytest_check.equal(res.json()["logo"],res_ethplorer.json()[""]," Check error!")
            # pytest_check.equal(res.json()["type"],res_ethplorer.json()[""]," Check error!")
            # pytest_check.equal(res.json()["creator"],res_ethplorer.json()[""]," Check error!")
            # pytest_check.equal(res.json()["created_at"],res_ethplorer.json()[""]," Check error!")


# balance
@allure.feature("Enhanced_API_Success!")
class Test_Enhanced_API_balance:
    test_data = [
        ("查询地址ETH","0x56eddb7aa87536c09ccc2793473599fd21a8b17f","",""),
        ("查询地址ETH","0xb32Ffd383759Ab23C56e907DB8D33E498467847e","",""),
        ("查询地址ETH","0xB0253D0308125d7eD0AaE9f2Ff138C85CcFFcc07","",""),
        ("查询地址ETH","0x2D4b1580A0db58781a6D3A9d2CCbed16128FA0c9","",""),
        ("查询地址ETH","0x97B67E5D4eDA1a4A2A1687Fe59336eB4F7cFCec0","",""),
        ("查询地址ETH","0x3257eff4bdcb74b6ebf8f0f4c67f5d15288cf97c","",""),
        ("查询地址ETH","0x1e7067c402f89b3623d774dcda4a11e0d62bdabe","",""),
        ("查询地址ETH","0x00cdC153Aa8894D08207719Fe921FfF964f28Ba3","",""),
        ("查询地址ETH","0x6887246668a3b87F54DeB3b94Ba47a6f63F32985","",""),
        ("查询地址ETH","0x533e3c0e6b48010873B947bddC4721b1bDFF9648","",""),
        ("查询地址ETH","0x477b8D5eF7C2C42DB84deB555419cd817c336b6F","",""),
        ("查询地址ETH","0xd88C972516714C6cb182c08cC4116dd3d5056f86","",""),
        ("查询地址ETH","0xa4f86E2f93376cF8DFB5de2f60CEA840df9E6eF0","",""),
        ("查询地址ETH","0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45","",""),
        ("查询地址ETH","0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549","",""),
        ("查询地址ETH","0x1eAb3B222A5B57474E0c237E7E1C4312C1066855","",""),
        ("查询地址ETH","0xd24400ae8BfEBb18cA49Be86258a3C749cf46853","",""),
        ("查询地址ETH","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","",""),
        ("查询地址ETH","0xC6bd89f570AE2FAC958eCbEEEED7d79FfC9260db","",""),
        ("查询地址ETH","0x6553aa7a55ECd9A2d05310EDCe271160656e909D","",""),

        ("查询地址ERC20-USDP","0xC88F7666330b4b511358b7742dC2a3234710e7B1","0x8E870D67F660D95d5be530380D0eC0bd388289E1",""),
        ("查询地址ERC20-USDC","0x30Cc64aD0Ce2B05934DA2FB63D458BcAB90aA62A","0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",""),
        ("查询地址ERC20-USDT","0xCeD10edfFa41d4ABEF45Cd1B032776c235b5eabE","0xdAC17F958D2ee523a2206206994597C13D831ec7",""),
        ("查询地址ERC20-MVDG","0xA83B11093c858c86321FBc4c20FE82cdbd58E09E","0x2eE543b8866F46cC3dC93224C6742a8911a59750",""),
        ("查询地址ERC20-APE","0x75e89d5979E4f6Fba9F97c104c2F0AFB3F1dcB88","0x4d224452801ACEd8B2F0aebE155379bb5D594381",""),
        ("查询地址ERC20-ENJ","0x4E5fca7aBe239626529115E5255B4d29cd4095A7","0xF629cBd94d3791C9250152BD8dfBDF380E2a3B9c",""),
        ("查询地址ERC20-MATIC","0x77480481A5C0CF3441B6988C9f55DF919b622088","0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0",""),
        ("查询地址ERC20-USDT","0x004f74a8388cE91950F29ea3E37EF604693a6395","0xdAC17F958D2ee523a2206206994597C13D831ec7",""),
        ("查询地址ERC20-SUSHI","0x93C1b2cc803199e6820cE8aDA97e86c3a964b984","0x6B3595068778DD592e39A122f4f5a5cF09C90fE2",""),
        ("查询地址ERC20-SHIB","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","0x95aD61b0a150d79219dCF64E1E6Cc01f0B64C4cE",""),

        ("查询地址ERC721-SFB","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","0xc9c77B0c2EE79CEc54B3aF7039f8a7bC684e48bD",""),
        ("查询地址ERC721-SNFT","0x473037de59cf9484632f4A27B509CFE8d4a31404","0x2A036569DBbe7730D69ed664B74412E49f43C2C0",""),
        ("查询地址ERC721-LIST","0x514910771AF9Ca656af840dff83E8264EcF986CA","0x81a91270629632886e56Ab01BBa3d8BCB5Da4b9b",""),
        ("查询地址ERC721-BKC","0x6B175474E89094C44Da98b954EedeAC495271d0F","0x2f2d5aA0EfDB9Ca3C9bB789693d06BEBEa88792F",""),
        ("查询地址ERC721-UD","0xdAC17F958D2ee523a2206206994597C13D831ec7","0xD1E5b0FF1287aA9f9A268759062E4Ab08b9Dacbe",""),
        ("查询地址ERC721-TSC","0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0","0x282A7D13152b3f51a3E31D46A2Ca563F8554d85D",""),
        ("查询地址ERC721-GENESIS","0x5B4093207C2660a7EB4ca3732B94EA25bDB6580B","0xd8a5d498ab43Ed060cb6629b97a19e3e4276dD9f",""),
        ("查询地址ERC721-ES","0x1692bf3AA4a65DB1C264D0244f9dDA1B4A387Ef7","0x3fD36d72f05fb1AF76EE7Ce9257ca850fAbA91ed",""),
        ("查询地址ERC721-Homes","0x89a91fc631D0E4d51740E3D9E20016C14e8F4cA2","0x4137D0606F4292aa57060321c856894EeB354B1b",""),
        ("查询地址ERC721-TSC","0xe7DFa5fffAF6E4F1EC79B5BDFDe57BCDe60E3C8b","0x282A7D13152b3f51a3E31D46A2Ca563F8554d85D",""),
        
        ("查询地址ERC1155-RARI","0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511","0xd07dc4262BCDbf85190C01c996b4C06a461d2430",""),
        ("查询地址ERC1155-","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","0xfaaFDc07907ff5120a76b34b731b278c38d6043C",""),
        ("查询地址ERC1155-RARI","0x0548F59fEE79f8832C299e01dCA5c76F034F558e","0xd07dc4262BCDbf85190C01c996b4C06a461d2430",""),
        ("查询地址ERC1155-OPENSTORE","0xcaD621da75a66c7A8f4FF86D30A2bF981Bfc8FdD","0x495f947276749Ce646f68AC8c248420045cb7b5e",""),
        ("查询地址ERC1155-BadKids","0x8a677474dEC43FCAeB80a2Dd2B1bc5D945aB61d1","0xf24587ecA741F60fEc923CC217be075f12E15473",""),
        ("查询地址ERC1155-WeAreLand","0x5B4093207C2660a7EB4ca3732B94EA25bDB6580B","0x59a79E83A2Bc84Abe2839F8Cd779181b551E6b89",""),
        ("查询地址ERC1155-ZPR NFT","0x6637b4b8fc4102135340509e294beeeBf4793FA7","0xF1F3ca6268f330fDa08418db12171c3173eE39C9",""),
        ("查询地址ERC1155-GAMAS","0x7A50C8658c40F50F90DCaD085E654b3748d8bCB4","0xa698CF4e59a6e21a97675603E541F1Aa5C7D44A3",""),
        ("查询地址ERC1155-OPENSTORE","0x1Cd602bdD66ffb80611A1F8f0ba628e9fFb233C0","0x495f947276749Ce646f68AC8c248420045cb7b5e",""),
        ("查询地址ERC1155-BadKids","0x3dF772D9C8849b7d52909d6B4f1a9bcBb8240222","0xf24587ecA741F60fEc923CC217be075f12E15473",""),
        ]

    @allure.story("Enhanced_API_balance!")
    @allure.title('{test_title}-address:{address}')
    @pytest.mark.parametrize('test_title,address,token_address,token_id', test_data)
    def test_balance(self, test_title,address,token_address,token_id):

        with allure.step("Query balance!"):
            with allure.step("Query balance!"):
                res = Http_Enhancedapi.HttpUtils.get_balance(address,token_address,token_id)
                assert res.status_code == 200
                blances = int(res.json()["amount"])

            with allure.step("Query balance by Aichemy!"):
                if (token_address == ""):
                    res_aichemy = Httprpc.HttpRpcEth_Utils.eth_getbalance(url_aichemy,address,"latest")
                    assert res_aichemy.status_code == 200
                    blances_aichemy = int(res_aichemy.json()["result"],16)
                else:
                    # pyload = {
                    #     "to":token_address,
                    #     "data":web3.Web3.keccak(text = "balanceOf()").hex()[:10] + "".zfill(20) + address[2:]
                    # }
                    # res_aichemy = Httprpc.HttpRpcEth_Utils.eth_call(url_aichemy,pyload,"latest")
                    # assert res_aichemy.status_code == 200
                    # blances_aichemy = int(res_aichemy.json()["result"],16)

                    body = {
                            "jsonrpc": "2.0",
                            "id": 0,
                            "method": "alchemy_getTokenBalances",
                            "params": [
                                address,
                                [token_address]
                            ]
                            }
                    logger.info('\n'+"<-----eth_getbalance----->"+"\n"+"Url:"+url_aichemy+'\n\n'+'Body:'+json.dumps(body))
                    res_aichemy = requests.post(url=url_aichemy,json=body,timeout=60)
                    logger.info('\n'+"<-----eth_getbalance Response----->"+"\n"+(res_aichemy.text))
                    assert res_aichemy.status_code == 200
                    blances_aichemy_hex = res_aichemy.json()["result"]["tokenBalances"][0]["tokenBalance"]
                    if (blances_aichemy_hex == None):
                        blances_aichemy = blances_aichemy_hex
                    else:
                        blances_aichemy = int(blances_aichemy_hex,16)
            
            with allure.step("balance check!"):
                logger.info("\n\n" + "<-----balances----->" + str(blances))
                logger.info("\n\n" + "<-----blances_aichemy----->" + str(blances_aichemy))
                assert blances == blances_aichemy


# tokenAssets
@allure.feature("Enhanced_API_Success!")
class Test_Enhanced_API_tokenAssets:

    test_data = [
        ("查询地址全部资产","0x56eddb7aa87536c09ccc2793473599fd21a8b17f","",""),
        ("查询地址全部资产","0xb32Ffd383759Ab23C56e907DB8D33E498467847e","",""),
        ("查询地址全部资产","0xB0253D0308125d7eD0AaE9f2Ff138C85CcFFcc07","",""),
        ("查询地址全部资产","0x2D4b1580A0db58781a6D3A9d2CCbed16128FA0c9","",""),
        ("查询地址全部资产","0x97B67E5D4eDA1a4A2A1687Fe59336eB4F7cFCec0","",""),
        ("查询地址全部资产","0x3257eff4bdcb74b6ebf8f0f4c67f5d15288cf97c","",""),
        ("查询地址全部资产","0x1e7067c402f89b3623d774dcda4a11e0d62bdabe","",""),
        ("查询地址全部资产","0x00cdC153Aa8894D08207719Fe921FfF964f28Ba3","",""),
        ("查询地址全部资产","0x6887246668a3b87F54DeB3b94Ba47a6f63F32985","",""),
        ("查询地址全部资产","0x533e3c0e6b48010873B947bddC4721b1bDFF9648","",""),
        ("查询地址全部资产","0x477b8D5eF7C2C42DB84deB555419cd817c336b6F","",""),
        ("查询地址全部资产","0xd88C972516714C6cb182c08cC4116dd3d5056f86","",""),
        ("查询地址全部资产","0x8a677474dEC43FCAeB80a2Dd2B1bc5D945aB61d1","",""),
        ("查询地址全部资产","0xa4f86E2f93376cF8DFB5de2f60CEA840df9E6eF0","",""),
        ("查询地址全部资产","0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45","",""),
        ("查询地址全部资产","0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549","",""),
        ("查询地址全部资产","0xcaD621da75a66c7A8f4FF86D30A2bF981Bfc8FdD","",""),
        ("查询地址全部资产","0x1eAb3B222A5B57474E0c237E7E1C4312C1066855","",""),
        ("查询地址全部资产","0xd24400ae8BfEBb18cA49Be86258a3C749cf46853","",""),
        ("查询地址全部资产","0x0548F59fEE79f8832C299e01dCA5c76F034F558e","",""),
        ("查询地址全部资产","0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511","",""),
        ("查询地址全部资产","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","",""),
        ("查询地址全部资产","0xC6bd89f570AE2FAC958eCbEEEED7d79FfC9260db","",""),
        ("查询地址全部资产","0x6B175474E89094C44Da98b954EedeAC495271d0F","",""),
        ("查询地址全部资产","0xdAC17F958D2ee523a2206206994597C13D831ec7","",""),
        ("查询地址全部资产","0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0","",""),
        ("查询地址全部资产","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","",""),
        ("查询地址全部资产","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","",""),
        ("查询地址全部资产","0x473037de59cf9484632f4A27B509CFE8d4a31404","",""),
        ("查询地址全部资产","0x514910771AF9Ca656af840dff83E8264EcF986CA","",""),
        ("查询地址全部资产","0xC88F7666330b4b511358b7742dC2a3234710e7B1","",""),
        ("查询地址全部资产","0x30Cc64aD0Ce2B05934DA2FB63D458BcAB90aA62A","",""),
        ("查询地址全部资产","0xCeD10edfFa41d4ABEF45Cd1B032776c235b5eabE","",""),
        ("查询地址全部资产","0xA83B11093c858c86321FBc4c20FE82cdbd58E09E","",""),
        ("查询地址全部资产","0x75e89d5979E4f6Fba9F97c104c2F0AFB3F1dcB88","",""),
        ("查询地址全部资产","0x4E5fca7aBe239626529115E5255B4d29cd4095A7","",""),
        ("查询地址全部资产","0x77480481A5C0CF3441B6988C9f55DF919b622088","",""),
        ("查询地址全部资产","0x004f74a8388cE91950F29ea3E37EF604693a6395","",""),
        ("查询地址全部资产","0x93C1b2cc803199e6820cE8aDA97e86c3a964b984","",""),
        ("查询地址全部资产","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","",""),

        ("查询地址erc721&erc1155资产","0x56eddb7aa87536c09ccc2793473599fd21a8b17f","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0xb32Ffd383759Ab23C56e907DB8D33E498467847e","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0xB0253D0308125d7eD0AaE9f2Ff138C85CcFFcc07","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x2D4b1580A0db58781a6D3A9d2CCbed16128FA0c9","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x97B67E5D4eDA1a4A2A1687Fe59336eB4F7cFCec0","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x3257eff4bdcb74b6ebf8f0f4c67f5d15288cf97c","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x1e7067c402f89b3623d774dcda4a11e0d62bdabe","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x00cdC153Aa8894D08207719Fe921FfF964f28Ba3","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x6887246668a3b87F54DeB3b94Ba47a6f63F32985","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x533e3c0e6b48010873B947bddC4721b1bDFF9648","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x477b8D5eF7C2C42DB84deB555419cd817c336b6F","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0xd88C972516714C6cb182c08cC4116dd3d5056f86","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x8a677474dEC43FCAeB80a2Dd2B1bc5D945aB61d1","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0xa4f86E2f93376cF8DFB5de2f60CEA840df9E6eF0","erc721,erc1155",""),
        ("查询地址erc721&erc1155资产","0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45","erc721,erc1155",""),
    ]

    @allure.story("Enhanced_API_tokenAssets!")
    @allure.title('{test_title}-address:{address}')
    @pytest.mark.parametrize('test_title,address,types,limit', test_data)
    def test_tokenassets(self, test_title,address,types,limit):

        if (types == ""): #查询地址全部tokens assets
            with allure.step("Query All tokenAssets!"):
                res = Http_Enhancedapi.HttpUtils.get_tokenAssets(address,types,limit)
                assert res.status_code == 200
                res_ethplorer = Http_Enhancedapi.HttpUtils.get_tokenAssets_ethplorer(address)
                assert res_ethplorer.status_code == 200

            with allure.step("tokens 与 ethplorer-tokens 条数对比!"):
                if (res.json()["size"] == 0):
                    pytest_check.equal(len(res.json()["data"]),0)
                    assert 'tokens' not in res_ethplorer.json(),'Tokens Number Gaps!'
                    logger.info("\n\n" + "<-----Tokens Null----->")         
                else:
                    pytest_check.greater(len(res.json()["data"]),0)
                    pytest_check.greater_equal(len(res.json()["data"]),len(res_ethplorer.json()["tokens"]),'Tokens Number Gaps!')

                    with allure.step("ethplorer-tokens  资产对比!"):  #拿ethplorer-tokens的数据与 tokens的数据对比
                        token_gaps = []
                        for i in range(len(res_ethplorer.json()["tokens"])):
                            token_address_ethplorer = res_ethplorer.json()["tokens"][i]["tokenInfo"]["address"]
                            token_balance_ethplorer = (res_ethplorer.json()["tokens"][i]["rawBalance"])
                            # token_amount
                            token_amount = [b.get("amount") for b in (res.json()["data"]) if b.get("token_address") == token_address_ethplorer]

                            if len(token_amount) == 0:
                                # 未查到相关token写入数组
                                token_gaps.append({"token_address":token_address_ethplorer,"token_balance_ethplorer":token_balance_ethplorer,"token_amount":'',"tips":"No token information found"})
                            elif len(token_amount) == 1:
                                # token资产不一致写入数组
                                if (token_balance_ethplorer != token_amount[0]):
                                    token_gaps.append({"token_address":token_address_ethplorer,"token_balance_ethplorer":token_balance_ethplorer,"token_amount":token_amount[0]})
                            elif len(token_amount) > 1:
                                # 查到重复token写入数组
                                token_gaps.append({"token_address":token_address_ethplorer,"token_balance_ethplorer":token_balance_ethplorer,"token_amount":token_amount,"token_amount":"token information repeat"})
                        logger.info("\n" + "<-----Tokens Assets Gaps----->" + "\n" + str(token_gaps))
                        assert len(token_gaps) == 0,'TokenAssets Gaps!'

        elif (types == "erc721,erc1155"):  #查询地址erc721,erc1155 tokens assets

            with allure.step("Query erc721,erc1155 tokenAssets!"):
                res = Http_Enhancedapi.HttpUtils.get_tokenAssets(address,types,limit)
                assert res.status_code == 200
                res_erc721erc1155 = Http_Enhancedapi.HttpUtils.get_tokenAssets_erc721erc1155(address)
                assert res_erc721erc1155.json()["code"] == 200
            
            with allure.step("ERC721&ERC1155 tokens 与 genie-tokens 条数对比!"):
                if (res.json()["size"] == 0):
                    pytest_check.equal(len(res.json()["data"]),0)
                    assert "assets" not in res_erc721erc1155.json()["data"],'Tokens Number Gaps!'
                    logger.info("\n\n" + "<-----Tokens Null----->")
                else:
                    pytest_check.greater(len(res.json()["data"]),0)
                    pytest_check.greater_equal(len(res.json()["data"]),len(res_erc721erc1155.json()["data"]["assets"]),'Tokens Number Gaps!')

                    with allure.step("genie-tokens  资产对比!"):  #拿genie-tokens的数据与 tokens的数据对比
                        token_gaps = []
                        for i in range(len(res_erc721erc1155.json()["data"]["assets"])):
                            token_address_genie = res_erc721erc1155.json()["data"]["assets"][i]["asset_contract"]["address"]
                            if (token_address_genie not in res.json()):
                                token_gaps.append({"token_address":token_address_genie})
                        logger.info("\n" + "<-----Tokens Gaps----->" + "\n" + str(token_gaps))
                        assert len(token_gaps) == 0,'Tokens Gaps!'


# nfts
@allure.feature("Enhanced_API_Success!")
class Test_Enhanced_API_nft:

    test_data = [
        ("查询地址全部资产","0x56eddb7aa87536c09ccc2793473599fd21a8b17f",""),
        ("查询地址全部资产","0xb32Ffd383759Ab23C56e907DB8D33E498467847e",""),
        ("查询地址全部资产","0xB0253D0308125d7eD0AaE9f2Ff138C85CcFFcc07",""),
        ("查询地址全部资产","0x2D4b1580A0db58781a6D3A9d2CCbed16128FA0c9",""),
        ("查询地址全部资产","0x97B67E5D4eDA1a4A2A1687Fe59336eB4F7cFCec0",""),
        ("查询地址全部资产","0x3257eff4bdcb74b6ebf8f0f4c67f5d15288cf97c",""),
        ("查询地址全部资产","0x1e7067c402f89b3623d774dcda4a11e0d62bdabe",""),
        ("查询地址全部资产","0x00cdC153Aa8894D08207719Fe921FfF964f28Ba3",""),
        ("查询地址全部资产","0x6887246668a3b87F54DeB3b94Ba47a6f63F32985",""),
        ("查询地址全部资产","0x533e3c0e6b48010873B947bddC4721b1bDFF9648",""),
        ("查询地址全部资产","0x477b8D5eF7C2C42DB84deB555419cd817c336b6F",""),
        ("查询地址全部资产","0xd88C972516714C6cb182c08cC4116dd3d5056f86",""),
        ("查询地址全部资产","0x8a677474dEC43FCAeB80a2Dd2B1bc5D945aB61d1",""),
        ("查询地址全部资产","0xa4f86E2f93376cF8DFB5de2f60CEA840df9E6eF0",""),
        ("查询地址全部资产","0x68b3465833fb72A70ecDF485E0e4C7bD8665Fc45",""),
        ("查询地址全部资产","0x21a31Ee1afC51d94C2eFcCAa2092aD1028285549",""),
        ("查询地址全部资产","0xcaD621da75a66c7A8f4FF86D30A2bF981Bfc8FdD",""),
        ("查询地址全部资产","0x1eAb3B222A5B57474E0c237E7E1C4312C1066855",""),
        ("查询地址全部资产","0xd24400ae8BfEBb18cA49Be86258a3C749cf46853",""),
        ("查询地址全部资产","0x0548F59fEE79f8832C299e01dCA5c76F034F558e",""),
        ("查询地址全部资产","0xb5d85CBf7cB3EE0D56b3bB207D5Fc4B82f43F511","erc1155"),
        ("查询地址全部资产","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","erc1155"),
        ("查询地址全部资产","0xC6bd89f570AE2FAC958eCbEEEED7d79FfC9260db","erc1155"),
        ("查询地址全部资产","0x6B175474E89094C44Da98b954EedeAC495271d0F","erc1155"),
        ("查询地址全部资产","0xdAC17F958D2ee523a2206206994597C13D831ec7","erc1155"),
        ("查询地址全部资产","0x7D1AfA7B718fb893dB30A3aBc0Cfc608AaCfeBB0","erc1155"),
        ("查询地址全部资产","0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2","erc1155"),
        ("查询地址全部资产","0x2260FAC5E5542a773Aa44fBCfeDf7C193bc2C599","erc1155"),
        ("查询地址全部资产","0x473037de59cf9484632f4A27B509CFE8d4a31404","erc1155"),
        ("查询地址全部资产","0x514910771AF9Ca656af840dff83E8264EcF986CA","erc1155"),
        ("查询地址全部资产","0xC88F7666330b4b511358b7742dC2a3234710e7B1","erc721"),
        ("查询地址全部资产","0x30Cc64aD0Ce2B05934DA2FB63D458BcAB90aA62A","erc721"),
        ("查询地址全部资产","0xCeD10edfFa41d4ABEF45Cd1B032776c235b5eabE","erc721"),
        ("查询地址全部资产","0xA83B11093c858c86321FBc4c20FE82cdbd58E09E","erc721"),
        ("查询地址全部资产","0x75e89d5979E4f6Fba9F97c104c2F0AFB3F1dcB88","erc721"),
        ("查询地址全部资产","0x4E5fca7aBe239626529115E5255B4d29cd4095A7","erc721"),
        ("查询地址全部资产","0x77480481A5C0CF3441B6988C9f55DF919b622088","erc721"),
        ("查询地址全部资产","0x004f74a8388cE91950F29ea3E37EF604693a6395","erc721"),
        ("查询地址全部资产","0x93C1b2cc803199e6820cE8aDA97e86c3a964b984","erc721"),
        ("查询地址全部资产","0x95A9bd206aE52C4BA8EecFc93d18EACDd41C88CC","erc721"),
    ]

    @allure.story("Enhanced_API_nfts!")
    @allure.title('{test_title}-address:{address}')
    @pytest.mark.parametrize('test_title,address,types', test_data)
    def test_nfts(self, test_title,address,types):
        
        with allure.step("Query nfts!"):
            res = Http_Enhancedapi.HttpUtils.get_nfts(address,types)
            assert res.status_code == 200

if __name__ == '__main__':
    pytest.main(["-vs", "/Users/lilong/Documents/Test_Api/Testcase/Test_Serve/Test_Enhanced_API/test_enhanced_api_success.py::Test_Enhanced_API_tokenInfo",'--alluredir=Report/a'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/a')
