import http
import json
import pytest_check
import allure
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common import Httpnft
from Common.Loguru import logger
            
# NFT
@allure.feature("NFT!")
class Test_NFT_Collection:

    test_data_collection_address = [
        ("0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"),
        ("0x495f947276749ce646f68ac8c248420045cb7b5e"),#erc1155
        ("0x34d85c9cdeb23fa97cb08333b511ac86e1c4e258"),
        ("0x60e4d786628fea6478f785a6d7e704777c86a7c6"),
        ("0x23581767a106ae21c074b2276d25e5c3e136a68b"),
        ("0xd1258db6ac08eb0e625b75b371c023da478e94a9"),
        ("0xff7ee5e55b2847ace66b8e0c59ce089311325da5"),
        ("0x249c3a9839c27a6a79820a24e7a6fec6b5992423"),
        ("0x059edd72cd353df5106d2b9cc5ab83a52287ac3a"),
        ("0x93589ca4d8581950fbdbf8a4fe262e4a37a64331"),
        ("0x0406243ca557c259712be750773177bc714e49f6"),
        ("0x31d45de84fde2fb36575085e05754a4932dd5170"),
        ("0x0914d4f60f1ea6baaccb95584c9e69208b9acce9"),
        ("0x8847d9c052200164961e82da1624e5820cd5d2fa"),
        ("0xab180e1e045118701bba99b1c59b5c9b26588414"),
        ("0x8ca191dd59260ee226523179220421e40e763cd7"),
        ("0xdcb1cdfe2b5f592e7bdc2696b7a68c6e866c4cc2"),
    ]

    test_data_owner_address = [
        ("0x92f4937c03a5dd90f5382ea593c9f7f3ae1d23a5")
    ]

    @allure.story("Collection detail!")
    @allure.title('Collection_address-{collection_address}')
    @pytest.mark.parametrize('collection_address', test_data_collection_address)
    def test_collection_details(self, collection_address):

        with allure.step("查询合集明细"):
            collection_details = Httpnft.HttpUtils.get_collection_details(collection_address)
            assert collection_details.status_code == 200

        with allure.step("Genie查询合集明细"):
            collection_details_genie = Httpnft.HttpUtils.get_collection_details_genie(collection_address)  
            assert collection_details_genie.status_code == 200
            assert collection_details_genie.json()['code'] == 200
            assert collection_details_genie.json()['status'] == "success"

            data_genie = {
                "address":collection_details_genie.json()["data"][0]["address"],
                "slug":collection_details_genie.json()["data"][0]["slug"],
                "name":(collection_details_genie.json()["data"][0]["name"]).replace(" ",""), #去除空格
                "symbol":collection_details_genie.json()["data"][0]["symbol"],
                "standard":collection_details_genie.json()["data"][0]["standard"].lower(), #转小写
                "description":collection_details_genie.json()["data"][0]["description"],
                "external_url":collection_details_genie.json()["data"][0]["externalUrl"],
                "image_url":collection_details_genie.json()["data"][0]["imageUrl"],
                "banner_image_url":collection_details_genie.json()["data"][0]["bannerImageUrl"],
                "verified":collection_details_genie.json()["data"][0]["isVerified"],
                "traits":collection_details_genie.json()["data"][0]["traits"],
                "stats":collection_details_genie.json()["data"][0]["stats"]
                }
            # logger.error(json.dumps(data_genie))


        with allure.step("遍历合集明细所有字段与Genie对比"):
            Collection_detail_gaps = {}
            traits_gaps = []
            stats_gaps = {}
            for key,value in collection_details.json().items():
                if key == "traits":
                    if len(value) == 0:
                        pytest_check.equal(len(collection_details_genie.json()["data"][0][key]),0,"traits is Null")
                    else:
                        # 遍历特征数组
                        for i in range(len(value)):
                            # 查询genie trait_value,trait_value相同的数据
                            value_genie = [t for t in collection_details_genie.json()["data"][0]["traits"] if t.get("trait_type") == value[i]["trait_type"] and (t.get("trait_value")).lower() == value[i]["trait_value"]][0]
                            # 遍历每个特征参数
                            trait_gaps = {}
                            for k,v in value[i].items():
                                if (k == "percentListed" or k == "floorPrice"):
                                    # percent = v/value_genie[k]
                                    # if (percent<0.8 or percent>1.2):
                                    #     trait_gaps.update(value[i])
                                    #     trait_gaps.update({k+"_genie":value_genie[k]})
                                    pass
                                elif (k == "trait_value"):
                                    if (v != (value_genie[k]).lower()):
                                        trait_gaps.update(value[i])
                                        trait_gaps.update({k+"_genie":value_genie[k]})
                                else: 
                                    if (v != value_genie[k]):
                                        trait_gaps.update(value[i])
                                        trait_gaps.update({k+"_genie":value_genie[k]})
                            if len(trait_gaps) > 0:
                                traits_gaps.append(trait_gaps)
                        # logger.error(json.dumps(traits_gaps))
                elif key == "stats":
                    if len(value) == 0:
                        pytest_check.equal(len(collection_details_genie.json()["data"][0][key]),0,"traits is Null")
                    else:
                        for k_,v_ in value.items():
                            if k_ == "total_supply":
                                if v_ != data_genie[key][k_]:
                                    stats_gaps.update({k_:v_,k_+"_genie":data_genie[key][k_]})
                            elif k_ == "market_cap" or k_ == "updated_at":
                                pass
                            else:
                                percent = v_/data_genie[key][k_]
                                if (percent < 0.8 or percent > 1.2):
                                    stats_gaps.update({k_:v_,k_+"_genie":data_genie[key][k_]})
                            if len(stats_gaps) > 0:
                                Collection_detail_gaps.update({key:stats_gaps})
                elif key == "created_at":
                    pass
                else:
                    if (value != data_genie[key]):
                        Collection_detail_gaps.update({key:value,key+"_genie":data_genie[key]})
            Collection_detail_gaps.update({"traits":traits_gaps,"stats":stats_gaps})     
            logger.info("\n\n\n" + "<-----Collection Detail Gaps----->" +"\n"+ json.dumps(Collection_detail_gaps))
            assert len(Collection_detail_gaps) == 0,"Collection Detail Gaps!"


    @allure.story("Collection NFT list!")
    @allure.title('Collection_address-{collection_address}')
    @pytest.mark.parametrize('collection_address', test_data_collection_address)
    def test_collection_nft_list(self, collection_address):

        with allure.step("查询合集NFT列表"):
            collection_nft_list = Httpnft.HttpUtils.get_collection_nft_list(collection_address)
            assert collection_nft_list.status_code == 200

        with allure.step("GEM查询合集NFT列表"):
            collection_nft_list_gem = Httpnft.HttpUtils.get_collection_nft_list_gem(collection_address)
            assert collection_nft_list_gem.status_code == 200

        with allure.step("每个NFT都在GEM合集的NFTS中"):
            data_id_gaps = [] #id存在差异
            data_id = [] #id都存在
            for i in range(len(collection_nft_list.json()["data"])):
                gap = [d.get("id") for d in collection_nft_list_gem.json()["data"] if d.get("tokenId") == collection_nft_list.json()["data"][i]["id"]]
                if len(gap) == 0:
                    data_id_gaps.append(collection_nft_list.json()["data"][i])
                else:
                    data_id.append(collection_nft_list.json()["data"][i])
            pytest_check.equal(len(data_id_gaps),0,"id存在差异")
            logger.info(json.dumps(data_id_gaps))
            logger.info(json.dumps(data_id))


        with allure.step("Genie查询合集NFT列表的每个NFT明细"):
            data_gaps = []
            for i in range(len(data_id)):
                data_detail_gaps = {}
                nft_detail = Httpnft.HttpUtils.get_nft_details_genie(collection_address,data_id[i]["id"])
                assert nft_detail.status_code == 200
                assert nft_detail.json()["code"] == 200
                assert nft_detail.json()["status"] == "success"

                with allure.step("NFT字段数据验证"):
                    name = data_id[i]["name"]
                    description = data_id[i]["description"]
                    id = data_id[i]["id"]
                    quantity = data_id[i]["quantity"]
                    last_sale_price = data_id[i]["last_sale_price"]
                    last_sale_asset = data_id[i]["last_sale_asset"]
                    last_sale_decimals = data_id[i]["last_sale_decimals"]
                    image_url = data_id[i]["image_url"]
                    image_thumbnail_url = data_id[i]["image_thumbnail_url"]

                    name_genie = nft_detail.json()["asset"][0]["collectionName"].replace(" ","") + " #" + nft_detail.json()["asset"][0]["tokenId"]
                    # description_genie
                    id_genie = nft_detail.json()["asset"][0]["tokenId"]
                    quantity_genie = str(nft_detail.json()["asset"][0]["quantity"])
                    image_url_genie = nft_detail.json()["asset"][0]["imageUrl"]
                    image_thumbnail_url_genie = nft_detail.json()["asset"][0]["smallImageUrl"]
                    if name != name_genie:
                        data_detail_gaps.update({"name":name,"name_genie":name_genie})
                    if id != id_genie:
                        data_detail_gaps.update({"id":id,"id_genie":id_genie})
                    if quantity != quantity_genie:
                        data_detail_gaps.update({"quantity":quantity,"quantity_genie":quantity_genie})
            data_gaps.append(data_id_gaps)
            data_gaps.append(data_detail_gaps)
            pytest_check.equal(len(data_gaps),0,"")
            logger.error(json.dumps(data_gaps))
        

    @allure.story("NFT Detail!")
    @allure.title('Collection_address-{collection_address}')
    @pytest.mark.parametrize('collection_address', test_data_collection_address)
    def test_nft_detail(self, collection_address):

        with allure.step("查询合集NFT列表"):
            collection_nft_list = Httpnft.HttpUtils.get_collection_nft_list(collection_address)
            assert collection_nft_list.status_code == 200

        for i in range(len(collection_nft_list.json()["data"])):
            id = collection_nft_list.json()["data"][i]["id"]
            with allure.step("查询NF明细"):
                nft_detail = Httpnft.HttpUtils.get_nft_details(collection_address,id)
                assert nft_detail.status_code == 200

            with allure.step("Genie查询NF明细"):
                nft_detail_genie = Httpnft.HttpUtils.get_nft_details_genie(collection_address,id)
                assert nft_detail_genie.status_code == 200
                assert nft_detail_genie.json()['code'] == 200
                assert nft_detail_genie.json()['status'] == "success"

    @allure.story("Collection Owners list!")
    @allure.title('Collection_address-{collection_address}')
    @pytest.mark.parametrize('collection_address', test_data_collection_address)
    def test_collection_owners_list(self, collection_address):

        with allure.step("查询合集Owners列表"):
            collection_owners_list = Httpnft.HttpUtils.get_collection_owners_list(collection_address)
            assert collection_owners_list.status_code == 200

    @allure.story("Owner Nfts list!")
    @allure.title('Owenr_address-{owenr_address}')
    @pytest.mark.parametrize('owenr_address', test_data_owner_address)
    def test_owner_nfts_list(self, owenr_address):

        with allure.step("查询Owner Nfts列表"):
            owner_nfts_list = Httpnft.HttpUtils.get_owner_nft_list(owenr_address)
            assert owner_nfts_list.status_code == 200


if __name__ == '__main__':
    path = os.path.abspath(__file__) + "::Test_NFT_Collection::test_collection_details"
    pytest.main(["-vs", path,'--alluredir=Report/Allure'])
    os.system(f'allure serve /Users/lilong/Documents/Test_Api/Report/Allure')