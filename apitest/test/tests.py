from django.test import TestCase
import requests
import json
#from apitest.models import *
# Create your tests here.

def login(username, password):
    url = 'http://127.0.0.1:8000/api_login_post/'
    data = {
        'username': username,
        'password': password
    }
    json.dumps(data)
    re = requests.post(url, json=data)
    print("登录信息", re.text)

def login1():
    url = 'http://127.0.0.1:8000/api_login_get?username=luoshiling&password=admin12345'
    re = requests.get(url)
    print(re.text)



def register(username, password, email):
    url = 'http://127.0.0.1:8000/api_register/'

    data = {
        'username': username,
        'password': password,
        'email': email,
        'passwdconfirm': password
    }
    json.dumps(data)
    re = requests.post(url, json=data)
    print("注册信息",re.text)


def add_lodgeInfo(info_dict):
    url = 'http://127.0.0.1:8000/api_add_lodgeinfo/'
    json.dumps(info_dict)
    re = requests.post(url,json=info_dict)
    print("添加房源", re.text)



def add_order(order_info):
    url = 'http://127.0.0.1:8000/api_add_order/'
    json.dumps(order_info)
    re = requests.post(url, json=order_info)
    print(re.text)






if __name__ == '__main__':
    # username = "luoshiling18",
    # password = "admin12345",
    # email = "15901304866@163.com"
    # register(username, password, email)
    # login(username, password)
    # info_dict = {"dayprice":3,
    #              "estate":"valid",
    #              "minday":1,
    #              "maxday":2,
    #              "tel":"15901304864",
    #              "remarks":"",
    #              "address_id":"124253424342",
    #              "image_md5":"sfdgwet4husf98fwiuhfsjkdhwh"
    #             }
    # add_lodgeInfo(info_dict)
    order_info = {
        "luid":1,
        "guestnum":2,
        "checkinday":"2019-01-03",
        "checkoutday":"2019-01-04"
    }
    add_order(order_info)


