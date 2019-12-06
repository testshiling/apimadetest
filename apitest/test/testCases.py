# coding = utf-8

import ddt
import unittest
import requests
import json
from apitest.test.csvReader import csvReader



def apiRequest(data):
    host = 'http://127.0.0.1:8000/'
    api_name = data[0]
    runOrNot = data[1]
    requestType = data[3]
    url = host + data[2]
    dataType = data[4]
    api_data = data[5]
    assertion = data[6]
    if runOrNot == 0:
        print(api_name,"不需要测试")
        return True
    if requestType == 'get':
        url = url + api_data
        res = requests.get(url).json()
    elif requestType == 'post':
        if dataType == 'json':
            api_data = eval(api_data) #str 转成字典
            #post_data = json.dumps(api_data) data-json
            res = requests.post(url,json=api_data).json()
        else:
            print("暂不支持这种数据格式的post请求")
            return False
    else:
        print('暂不支持这种请求方式')
        return False
    assertCotent,expectResult = assertion.split(":")
    try:
        test_result = res[assertCotent]
    except Exception as e:
        print("取值失败，返回中没有", assertCotent)
        return False
    try:
        assert test_result == int(expectResult)
        print("测试通过!!!")
    except AssertionError:
        print("断言失败!!!")
        print("预期结果：", assertCotent,expectResult)
        print("实际结果：", assertCotent,test_result)
        return False

@ddt.ddt
class apiTest(unittest.TestCase):
    dataList = csvReader()

    def setUp(self):
        print("测试开始")

    def tearDown(self):
        print("测试结束")

    @ddt.data(*dataList)
    def test_apiTest(self, row):
        apiRequest(row)


if __name__ == '__main__':
    unittest.main()

