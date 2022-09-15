import json
import pytest_check
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
from Common import Httpnft
from Common.Loguru import logger
            

collection_address ="0xbc4ca0eda7647a8ab7c2061c2e118a18a936f13d"

collection_details = Httpnft.HttpUtils.get_collection_details(collection_address)

collection_details_genie = Httpnft.HttpUtils.get_collection_details_genie(collection_address)  
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
                # logger.error(value[i])
                value_genie = [t for t in collection_details_genie.json()["data"][0]["traits"] if t.get("trait_type") == value[i]["trait_type"] and (t.get("trait_value")).lower() == value[i]["trait_value"]][0]
                # logger.error(value_genie)
                # 遍历每个特征参数
                trait_gaps = {}
                for k,v in value[i].items():
                    if (k == "percentListed" or k == "floorPrice"):
                        # percent = v/value_genie[k]
                        # if (percent<0.8 or percent>1.2):
                        #     trait_gaps.update(value[i])
                        #     trait_gaps.update({k+"_genie":value_genie[k]})
                        pass
                    else:
                        if (v != (value_genie[k])):
                            trait_gaps.update(value[i])
                            trait_gaps.update({k+"_genie":value_genie[k]})
                if len(trait_gaps) > 0:
                    traits_gaps.append(trait_gaps)
            logger.error(json.dumps(traits_gaps))