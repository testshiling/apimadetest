# coding =utf-8

import csv

def csvReader():
    file_path = '/Users/luoshiling/apimadetest/apitest/test/apiData.csv'
    with open(file_path,'r') as f:
        count = 1
        dataList = []
        data = csv.reader(f)
        for row in data:
            if count == 1:
                count += 1
                continue
            else:
                dataList.append(row)
    if not dataList:
        print("csv无数据")
        return False
    #print(dataList)
    return dataList
if __name__ == '__main__':
    csvReader()