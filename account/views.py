# _*_ coding:utf-8 _*_

from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
import urllib.request
import urllib
import platform
from django.conf import settings
import json

from django.views.decorators.csrf import csrf_exempt

from order.models import *
from order2.models import *
from order3.models import *

import logging

from django.core.serializers.json import DjangoJSONEncoder

logger = logging.getLogger(__name__)
"""
缺少功能，用户评分更新
"""


class serializeUser(DjangoJSONEncoder):
    def default(self, o, *fields):
        ret_value = {}
        if isinstance(o, user):
            for key in fields:
                value = getattr(o, key)
                if isinstance(value, str):
                    ret_value[key] = value
                elif type(value) == type(None):
                    ret_value[key] = ''
                elif type(value) == float:
                    ret_value[key] = value
                elif type(value) == int:
                    ret_value[key] = value
                else:
                    serializeValue = super().default(value)
                    ret_value[key] = serializeValue
            return str(ret_value)

        elif type(o) == str:
            return o
        elif type(o) == None:
            return ''
        return super().default(o)


# 没有问题，单元测试搞不来
def order_user_Serializer(o, orderFields, userFields):
    # print(type(o))
    ret_value = {}
    for key in orderFields:
        serializer = serializeUser()
        obj = getattr(o, key)
        if isinstance(obj, user):
            value = serializer.default(obj, *userFields)
            ret_value[key] = value
        else:
            ret_value[key] = obj
    return ret_value


# class sculogin(object):
#     url = "http://zhjw.scu.edu.cn/j_spring_security_check"
#     img_url = "http://zhjw.scu.edu.cn/img/captcha.jpg"
#     is_updated = False
#
#     #验证码地址
#     #ip + 'static/' + 'account/img/login.jpg'
#
#
#
#     def getCapatcha(self):
#         """
#         :return 图片的url:
#         """
#         self.session = requests.Session()
#         print(sculogin.url)
#         ir = self.session.get(sculogin.img_url)
#         # print(ir.text)
#         if ir.status_code == 200:
#             if platform.system()=="Linux":
#                 open(settings.STATIC_ROOT+'/account/img/login.jpg', 'wb').write(ir.content)
#             else:
#                 open('static/account/img/login.jpg', 'wb').write(ir.content)
#         # test
#         # img = Image.open("static/account/img/login.jpg")
#         # img.show()
#
#
#     def login(self,username,password,captcha:str,cookies)->bool:
#         """
#         :param captcha:
#         :param username:
#         :param password:
#         :return bool:
#         """
#         self.session = requests.session()
#         data = {
#             'j_username':username,
#             'j_password':password,
#             'j_captcha':captcha,
#         }
#         # print(cookies)
#         res = self.session.post(sculogin.url,data=data,cookies=cookies)
#         # print(res.status_code)
#         # print(res.text)
#         if (res.status_code==200):
#             return True
#
#         return False


def login(request):
    wx_name = request.GET.get("wx_name", "")
    wx_name = str(wx_name)
    # print(wx_name)
    appid = settings.APPID
    secret = settings.SECRET
    code = request.GET.get("code", "")
    head_img = request.GET.get("head_img", "")

    errmsg = ""
    if not appid:
        errmsg += "appid不能为空"
    elif not secret:
        errmsg += "秘钥secret不能为空"
    elif not code:
        errmsg += "登录code为空"
    elif not head_img:
        errmsg += "头像url没空"
    elif not wx_name:
        errmsg += "微信名为空"
    if errmsg:
        return JsonResponse({"errmsg": errmsg}, status=404)

    # 发送请求获得openid session_key unionid errcode errmsg

    tencent_url = "https://api.weixin.qq.com/sns/jscode2session?appid={}&secret={}&js_code={}&grant_type=authorization_code".format(
        appid, secret, code)

    headers = {'content-type': 'application/json'}

    R = urllib.request.Request(url=tencent_url, headers=headers)  # 接口成功只返回openid session_key

    response = urllib.request.urlopen(R).read()

    response_json = json.loads(response)
    openid = response_json.get("openid")
    session_key = response_json.get("session_key")

    errmsg = response_json.get("errmsg", "")
    errcode = response_json.get("errcode")

    if not errcode:
        request.session['openid'] = openid
        # print("wx_name",wx_name)
        # print("🐷")
        try:
            cur_user = user.objects.get(openid=openid)

            cur_user.wx_name = wx_name
            cur_user.save()
        except:
            # 创建user
            cur_user = user()
            cur_user.openid = openid
            cur_user.wx_name = wx_name
            cur_user.head_img = settings.STATIC_URL + "account/img/" + openid + ".jpg"
            cur_user.save()
            # 头像文件保存
        if platform.system() == 'Linux':
            local = settings.STATIC_ROOT + "/account/img/" + cur_user.openid + ".jpg"
        else:
            local = "static/account/img/" + cur_user.openid + ".jpg"
            # with open(local,'w') as f:
            #     pass
        urllib.request.urlretrieve(head_img, local)
        request.session['session_key'] = session_key
        request.session['openid'] = openid
        request.session['is_login'] = True
        request.session.set_expiry(100000000)

        return JsonResponse({"msg": "You are logged in"})
    else:  # errcode由微信api决定(auth code2session), https://developers.weixin.qq.com/miniprogram/dev/api-backend/auth.code2Session.html
        return JsonResponse({"errmsg": errmsg, "errcode": errcode}, status=404)


# def logout(request):
#     print(dict(request.session))
#     if request.session.exists('openid'):
#         del request.session['openid']
#     if request.session.exists('session_key'):
#         del request.session['session_key']
#     return JsonResponse({"msg":"You are logged out"})
#
# @csrf_exempt
# def verifStuId(request):
#     scuLoginer = sculogin()
#     print(dict(request.session))
#     stuId = request.POST.get("stuId","")
#     passwd = request.POST.get("passwd")
#     captcha = request.POST.get("captcha")
#     openid = request.session.get("openid","")
#     is_updated = request.session.get("is_updated","")
#     cur_user = get_object_or_404(user,openid=openid)
#     cookies = request.session.get("cookies")
#     # print(stuId,passwd,captcha)
#     # print(cookies)
#     if not is_updated:
#         return JsonResponse({"msg":"验证码未更新"},status=404,)
#
#     result = scuLoginer.login(username=stuId,password=passwd,captcha=captcha,cookies=cookies)
#     request.session["is_updated"] = False
#     if result:
#         #保存学号和密码
#         cur_user.studentId = stuId
#         cur_user.stuIdPwd = passwd
#         cur_user.save()
#         return JsonResponse({"msg":"绑定成功"})
#
#     else:
#         return JsonResponse({"msg":"绑定失败"},status=404)



@csrf_exempt
def myAddress(request):
    if request.method == 'POST':
        openid = request.session.get("openid")
        cur_user = get_object_or_404(user, openid=openid)
        name = request.POST.get("name", "")
        receiveAddress = request.POST.get("receive_pos", "")
        phone = request.POST.get("phone", "")
        print(name)
        cur_user.receiveAddress = receiveAddress
        cur_user.name = name
        cur_user.phone = phone
        cur_user.save()
        return JsonResponse({"msg": "保存成功"})
    else:
        return JsonResponse({"msg": "please use post"}, status=406)  # not acceptable


@csrf_exempt
def getAddress(request):
    openid = request.session.get("openid")
    cur_user = get_object_or_404(user, openid=openid)
    userSerializer = serializeUser()
    value = userSerializer.default(cur_user, *["phone", "receiveAddress", "name"])
    print(value)
    return JsonResponse(value, safe=False)


def myorder(request):
    # status 0,1,2,3,4,5
    # 需要登录
    openid = request.session.get("openid", "")
    cur_user = get_object_or_404(user, openid=openid)
    status = request.GET.get("status", "")

    try:
        status = int(status)
    except ValueError as e:
        logger.critical(e)
        status = 0

    # 第一种,我发的订单
    sendOrder = order.objects.filter(order_owner=cur_user)
    receivedOrder = order.objects.filter(free_lancer=cur_user)

    orderFields = ["orderid", "createTime", "expireDateTime", "order_owner", "free_lancer", "money", "pos", "kuaidi",
                   "received_pos", "hidden_info"]
    userFields = ["openid", "wx_name", "phone", "studentId", "head_img"]
    if status != "":
        sendOrder = sendOrder.filter(order_status=status)
        receivedOrder = receivedOrder.filter(order_status=status)
    # 默认按照订单创建时间排序,最新的订单
    sendOrder.order_by("createTime").reverse()
    receivedOrder.order_by("createTime").reverse()

    sendOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in sendOrder]
    receivedOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in receivedOrder]
    # sendOrder = sendOrder.values(*orderFields)
    # receivedOrder = receivedOrder.values(*orderFields)
    print(receivedOrders)
    return JsonResponse({"sendOrder": sendOrders, "receivedOrder": receivedOrders}, safe=False)


def myorder2(request):
    # status 1,2,3,4
    # 需要登录
    openid = request.session.get("openid", "")
    cur_user = get_object_or_404(user, openid=openid)
    status = request.GET.get("status", "")
    kind = request.GET.get("kind", "")
    try:
        status = int(status)
    except ValueError as e:
        logger.critical(e)
        status = 0

    # 第一种,我发的订单
    sendOrder = order2.objects.filter(order_owner=cur_user, kind=kind)
    receivedOrder = order2.objects.filter(free_lancer=cur_user, kind=kind)

    orderFields = ["orderid", "createTime", "expireDateTime", "order_owner", "free_lancer", "money", "pos",
                   "received_pos", "hidden_info"]
    userFields = ["openid", "wx_name", "phone", "studentId", "head_img"]
    if status != "":
        sendOrder = sendOrder.filter(order_status=status)
        receivedOrder = receivedOrder.filter(order_status=status)
    # 默认按照订单创建时间排序,最新的订单
    sendOrder.order_by("createTime").reverse()
    receivedOrder.order_by("createTime").reverse()

    sendOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in sendOrder]
    receivedOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in receivedOrder]
    # sendOrder = sendOrder.values(*orderFields)
    # receivedOrder = receivedOrder.values(*orderFields)

    return JsonResponse({"sendOrder": sendOrders, "receivedOrder": receivedOrders}, safe=False)

@csrf_exempt
def myInfo(request):
    openid = request.session.get("openid")
    cur_user = get_object_or_404(user, openid=openid)
    userSerializer = serializeUser()
    # print(isinstance(cur_user,user))
    value = userSerializer.default(cur_user, *["name", "phone", "studentId", "head_img", "rate", "created_date",
                                               "received_order_count", "sended_order_count"])
    # print(value)
    return JsonResponse(value, safe=False)

def myorder3(request):
    # status 1,2,3,4
    # 需要登录
    openid = request.session.get("openid", "")
    cur_user = get_object_or_404(user, openid=openid)
    status = request.GET.get("status", "")

    try:
        status = int(status)
    except ValueError as e:
        logger.critical(e)
        status = 0

    # 第一种,我发的订单
    sendOrder = order3.objects.filter(order_owner=cur_user)
    receivedOrder = order3.objects.filter(free_lancer=cur_user)

    orderFields = ["orderid", "createTime", "expireDateTime", "order_owner", "free_lancer", "money", "pos",
                   "received_pos", "hidden_info"]
    userFields = ["openid", "wx_name", "phone", "studentId", "head_img"]
    if status != "":
        sendOrder = sendOrder.filter(order_status=status)
        receivedOrder = receivedOrder.filter(order_status=status)
    # 默认按照订单创建时间排序,最新的订单
    sendOrder.order_by("createTime").reverse()
    receivedOrder.order_by("createTime").reverse()

    sendOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in sendOrder]
    receivedOrders = [order_user_Serializer(order_obj, orderFields, userFields) for order_obj in receivedOrder]
    # sendOrder = sendOrder.values(*orderFields)
    # receivedOrder = receivedOrder.values(*orderFields)

    return JsonResponse({"sendOrder": sendOrders, "receivedOrder": receivedOrders}, safe=False)

# def get_cookies(request):
#     return JsonResponse(dict(request.session['cookies']))
