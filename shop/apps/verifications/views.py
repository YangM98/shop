from random import randint

from django.shortcuts import render

# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from . import const
from shop.lib.yuntongxun.sms import CCP


class SMSValidView(APIView):
    def get(self,request ,mobile):

        # 1 创建Redis连接对象
        redis_conn = get_redis_connection('verify_codes')
        # 设置60s之内只能发一次短信   每次发短信先查找是否存储的标记  如果标记存在则返回  不存在则将标记存在到redis数据库中
        flag = redis_conn.get('send_flag_%s' % mobile)
        if flag:
            return Response({'message':'60秒内请勿重复发短信'},status=status.HTTP_400_BAD_REQUEST)
        # 2 生成验证码
        sms_code = '%06d' %randint(0,999999)
        print(sms_code)

        # 创建管道  利用管道让多条redis命令一次执行 ，避免多条命令多次访问redis数据库
        pl = redis_conn.pipeline()
        pl.setex('send_flag_%s' % mobile,const.SEND_SMS_CODE_INTERVAL, 1)
        pl.setex('sms_%s' % mobile, const.SMS_CODE_REDIS_EXPIRES, sms_code)
        pl.execute()  # 执行

        # 3 保存flag标记 到Redis数据库中
        #redis_conn.setex('send_flag_%s' % mobile,const.SEND_SMS_CODE_INTERVAL, 1)
        # 4 保存验证码到Redis数据库中
        #redis_conn.setex('sms_ %s' % mobile, const.SMS_CODE_REDIS_EXPIRES, sms_code)
        # 5 利用云通讯 发送手机验证码
        # CCP.send_template_sms(self, 手机号，[验证码，5分钟]，1 第一样式)
        # CCP.send_template_sms(mobile,[sms_code,const.SMS_CODE_REDIS_EXPIRES//60],1)
        # 6 返回响应
        return Response({'message':'ok'})
