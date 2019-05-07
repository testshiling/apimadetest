from django.shortcuts import render,HttpResponse
from apitest.models import *
import json
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password, make_password
import sys
import datetime
import threading
from apitest.others import others_pay_order_true
import requests


# api_demo
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def api_demo(request):
    parameter = request.data
    id = parameter['data']
    if id == 1:
        data = 'There are three dogs'
    elif id == 2:
        data = 'There are two dogs'
    else:
        data = 'Thers is nothing'

    return Response({'data': data})


# 登录接口-post
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def login_post(request):
    data = json.loads(request.body)
    try:
        user = User.objects.get(username=data['username'])
    except User.DoesNotExist:
        return Response({
            "status_code": 400,
            'msg': "用户不存在"
        })
    password = data['password']
    passwdcheck = check_password(password, user.password)
    if passwdcheck:
        return Response({
            "status_code":200,
            'msg': "登录成功"
        })
    else:
        return Response({
            "status_code": 400,
            'msg': "密码错误"
        })


# 登录接口-get
@csrf_exempt
@api_view(http_method_names=['GET'])
@permission_classes((permissions.AllowAny,))
def login_get(request):
    username = request.GET.get('username')
    password = request.GET.get('password')
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({
            "status_code": 400,
            'msg': "用户不存在"
        })
    passwdcheck = check_password(password, user.password)
    if passwdcheck:
        return Response({
            "status_code":200,
            'msg': "登录成功"
        })
    else:
        return Response({
            "status_code": 400,
            'msg': "密码错误"
        })
# 注册接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def register(request):
    """
    参数示例：
    data = {
        'username': "luoshiling18",
        'password': admin12345,
        'email': "15901304866@163.com",
    }
    :param request:
    :return:
    """
    data = json.loads(request.body)
    if (data['username'] == ""
            or data['password'] == ""
            or data['email'] == ""
            ):
        return Response({
            "status_code": 400,
            'msg': "信息错误"
        })
    else:
        user = User(email=data['email'],
                    password=make_password(data['password']),
                    username=data['username'])
        user.save()
        return Response({
            "status_code": 200,
            'msg': "注册成功"
        })


# 数据库检查字段  目前没用
def is_fields_error(_model, fields, ex_fields):
    from django.db import models
    """
    @note 检查相应的_model里是否含有params所有key，若为否，则返回第一个遇到的不在_model里的key和False
    否则，返回为空True与空
    :param _model: fields:待检查字段  ex_fields:不在检查范围内的字段，比如外键
    :param params:
    :return: True,'' / False, key
    """
    if ex_fields:
        for i in ex_fields:
            if i in fields:
                fields.remove(i)

    if not (issubclass(_model, models.Model) and isinstance(fields, (list, tuple))):
        return False, u'参数有误'

    all_fields = list(_model._meta.get_fields())
    print(all_fields)
    for key in fields:
        if key not in all_fields:
            return False, key
    return True, ''


# 添加房源接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def add_lodgeinfo(request):
    """
    参数示例：
    info_dict = {"dayprice":3,
    #              "estate":"valid",
    #              "minday":1,
    #              "maxday":2,
    #              "tel":"15901304864",
    #              "remarks":"",
    #              "address_id":"124253424342",
    #              "image_md5":"sfdgwet4husf98fwiuhfsjkdhwh"
    #             }
    :param request:
    :return:
    """
    info_dict = json.loads(request.body)
    # _flag, func_r = is_fields_error(lodgeunitinfo, list(info_dict.keys()), ex_fields=['id','create_time','update_time'])
    # if not _flag:
    #     print("触发", func_r)
    # else:
    #     print("没触发", func_r)
    try:
        lodgeunitinfo.objects.create(**info_dict)
        return Response({"status_code": 200, "msg": "房源添加成功"})
    except Exception:
        exception_info = sys.exc_info()
        return Response({"status_code": 400, "msg":exception_info[0] + ":" + exception_info[1]})


# 订单接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def create_order(request):
    """
    参数示例：
    order_info = {
    #     "luid":1,
    #     "guestnum":2,
    #     "checkinday":"2019-01-03",
    #     "checkoutday":"2019-01-04"
    # }
    :param request:
    :return:
    """
    data = json.loads(request.body)
    #  房源存在校验
    luid = data['luid']
    daynum = datetime.datetime.strptime(data['checkoutday'], '%Y-%m-%d') - datetime.datetime.strptime(data['checkinday'],'%Y-%m-%d')
    id_list = []
    for i in lodgeunitinfo.objects.values('id'):
        id_list.append(i['id'])
    if luid not in id_list:
        return Response({"status_code": 400, "msg": luid + "不存在"})
    elif daynum.days < 1:
        return Response({"status_code": 400, "msg": "入住时间不能晚于离开时间"})
    else:
        lodgeinfo = lodgeunitinfo.objects.filter(id=str(luid))
        dayprice = 0
        for i in lodgeinfo:
            dayprice = i.dayprice
        totalprice = int(daynum.days) * dayprice
        #print("日价", dayprice, "天数", daynum.days)
        data["totalprice"] = totalprice
        order.objects.create(**data)
        return Response({"status_code": 200, "msg": "创建订单成功"})


# 支付回调接口--示例
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def payback_order(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='done')
    except Exception:
        return Response({"status_code": 400, "msg": "订单回调更新失败"})
    return Response({"status_code": 200, "msg": "支付成功"})


# 支付第三方接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def others_pay_order(request):
    data = json.loads(request.body)
    order_id = data['order_id']
    totalprice = data['totalprice']
    other_order_info = others_order.objects.filter(order_id=str(order_id))
    if other_order_info:
        pass
    else:
        others_order.objects.create(order_id=order_id)
    # 下面这步在实际中其实是不对，应该是从第三方库中查
    try:
        orderinfo = order.objects.filter(id=str(order_id))
    except Exception:
        return Response({"status_code": 400, "msg": "订单不存在"})
    for i in orderinfo:
        if totalprice == i.totalprice:
            if i.estate == 'valid':
                coo_others = threading.Thread(target=update_others_order, kwargs=({"order_id": order_id, "totalprice": totalprice, "estate": "yes"}))
                coo_others.start()
                coo_back = threading.Thread(target=payback_order_true, kwargs=({"order_id": order_id}))
                coo_back.start()
                return Response({"status_code": 200, "msg": "支付成功"})
            else:
                return Response({"status_code": 400, "msg": "订单状态不正确"})
        else:
            return Response({"status_code": 400, "msg": "订单总价不正确"})


# 支付回调接口--第三方用
def payback_order_true(**data):
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='done')
    except Exception:
        return Response({"status_code": 400, "msg": "支付订单回调更新失败"})


# 起一个进程去后台更新数据库
def update_others_order(**data):
    check_dict = isinstance(data, dict)
    if check_dict:
        others_order.objects.filter(order_id=data['order_id']).\
            update(**data)
        pass
    else:
        return Response({"status_code": 400, "msg": "订单更新失败"})

    print("更新内容：" + str(data))


# 起一个进程去取消订单
def order_cancel(**data):
    order_id = data['order_id']
    try:
        order.objects.filter(id=order_id).update(estate='cancel')
    except Exception:
        return Response({"status_code": 400, "msg": "取消订单回调更新失败"})




# 支付接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def pay_order(request):
    """
    参数示例：
    pay_order_info = {
        "order_id": 1,
        "luid": 1
    }
    :param request:
    :return:
    """
    data = json.loads(request.body)
    #  订单参数检查
    order_id = data['order_id']
    luid = data['luid']
    try:
        orderinfo = order.objects.filter(id=str(order_id))
    except Exception:
        return Response({"status_code": 400, "msg": "订单不存在"})
    try:
        luinfo = lodgeunitinfo.objects.filter(id=str(luid))
    except Exception:
        return Response({"status_code": 400, "msg": "房源不存在"})
    for i in orderinfo:
        if luid == i.luid:
            if i.estate == 'valid':
                for j in luinfo:
                    if j.estate == 'valid':
                        coo_other_pay = threading.Thread(target=others_pay_order_true, kwargs=({"order_id": order_id, "totalprice": i.totalprice, "estate": "yes"}))
                        coo_other_pay.start()
                        return Response({"status_code": 200, "msg": "第三方支付接口调用成功，支付成功"})
                    else:
                        return Response({"status_code": 400, "msg": "房源已下线或已被预订"})
            else:
                return Response({"status_code": 400, "msg": "订单已失效"})
        else:
            return Response({"status_code": 400, "msg": "订单与房源不匹配"})


