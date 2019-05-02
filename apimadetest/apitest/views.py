from django.shortcuts import render,HttpResponse
from apitest.models import *
import json
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password, make_password


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


# 添加房源接口
@csrf_exempt
@api_view(http_method_names=['POST'])
@permission_classes((permissions.AllowAny,))
def add_lodgeInfo(request):
    info_dict = json.loads(request.body)

    try:
        lodgeunitinfo.objects.create(**info_dict)
        return HttpResponse({"status_code":200,"msg":"房源添加成功"})
    except Exception:
        print({"status_code":400,"msg":"房源添加失败"})




# 订单接口
# @csrf_exempt
# @api_view(http_method_names=['POST'])
# @permission_classes((permissions.AllowAny,))
# def order(request):
#     data = json.loads(request.body)
#
#     #  房源存在校验
#     try: