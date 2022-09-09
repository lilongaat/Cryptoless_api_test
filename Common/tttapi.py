list = [1,2,3]
list_api = [1]

for i in range(len(list)):
    if (list[i] not in list_api):
        print(list[i])