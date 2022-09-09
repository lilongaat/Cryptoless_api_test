import csv
from email.policy import default
from unittest.mock import DEFAULT
import pandas as pd

# csv 文件去重 
path = '/Users/lilong/Documents/Test_Api/Testcase/Test_Account/Test_Create_Account/eth_address_d.csv'
frame=pd.read_csv(path, names = ['key','value'])
data = frame.drop_duplicates(subset=['value'], keep='first', inplace=False)
data.to_csv(path, header=None , index= 0,encoding='utf8')