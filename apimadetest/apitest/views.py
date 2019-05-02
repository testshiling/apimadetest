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
    data = json.loads(request.body)
    if (data['username'] == ""
            or data['password'] == ""
            or data['email'] == ""
            or data['passwdconfirm'] == ""):
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


# 数据库检查字段
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
    data = json.loads(request.body)
    #  房源存在校验
    luid = data['luid']
    daynum = datetime.datetime.strptime(data['checkoutday'],'%Y-%m-%d') - datetime.datetime.strptime(data['checkinday'],'%Y-%m-%d')
    id_list = []
    for i in lodgeunitinfo.objects.values('id'):
        id_list.append(i['id'])
    if luid not in id_list:
        return Response({"status_code": 400, "msg": luid + "不存在"})
    elif daynum.days < 1:
        return Response({"status_code": 400, "msg": "入住时间不能晚于离开时间"})
    else:
        lodgeinfo = lodgeunitinfo.objects.filter(id=str(luid))
        # for i in lodgeunitinfo:
        #     if i["id"] == luid:
        #         dayprice = i['dayprice']
        dayprice = 0
        for i in lodgeinfo:
            dayprice = i.dayprice
        totalprice = int(daynum.days) * dayprice
        data["totalprice"] = totalprice
        order.objects.create(**data)
        return Response({"status_code": 200, "msg": "创建订单成功"})

