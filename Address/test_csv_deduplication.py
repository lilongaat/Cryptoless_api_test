import csv
from email.policy import default
from unittest.mock import DEFAULT
import pandas as pd

# csv 文件去重 
path = '/Users/lilong/Documents/Test_Api/Address/Top/BTC.csv'
frame=pd.read_csv(path, names = ['address'])
data = frame.drop_duplicates(subset=['address'], keep='first', inplace=False)
data.to_csv(path, header=None , index= 0,encoding='utf8')