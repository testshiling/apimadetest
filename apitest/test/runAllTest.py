# coding = utf-8

import unittest
from apitest.test.HTMLTestRunner import HTMLTestRunner
import time


suite = unittest.TestSuite()
try:
    test_case = unittest.defaultTestLoader.discover('./', pattern='testCases.py')
    suite.addTest(test_case)
except Exception:
    print("加载失败")
result_path = './report/'
now = time.strftime("%Y-%m-%d %H_%M_%S", time.localtime())
file_path = result_path + now +"AttendanceReport.html"
with open(file_path, 'wb') as file:
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=file, verbosity=1, title='接口测试报告', description='接口测试报告', tester='罗式伶'
    )
    runner.run(suite)
