import csv

data = []
with open('/Users/lilong/Documents/Test_Api/Address/Top/BTC.csv') as csvfile:
    # reader = csv.DictReader(csvfile)
    reader = csv.reader(csvfile)
    for i,row in enumerate(reader):
        print(row[0])
        data.append({row[0]})
        if(i >= 9):
            break
print(data)
