from django.shortcuts import render
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import UserInfo
from .serializers import CreateUserSerializer, UserDetailSerializer, EmailSerializer


# Create your views here.



class UserView(CreateAPIView):
    # 创建新用户
    serializer_class = CreateUserSerializer

class usernameAPIView(APIView):
    '''校验username是否重复'''
    def get(self,request,username):
        # 1 获取username
        count = UserInfo.objects.filter(username = username).count()

        # 2 构建响应数据
        data = {
            'username':username,
            'count':count
        }
        # 3 返回响应数据
        return Response(data)


class mobileAPIView(APIView):
    '''校验手机号是否重复'''
    def get(self, request, mobile):
        # 1 获取username
        count = UserInfo.objects.filter(mobile=mobile).count()

        # 2 构建响应数据
        data = {
            'mobile': mobile,
            'count': count
        }
        # 3 返回响应数据
        return Response(data)

class UserDetialView(RetrieveAPIView):
    ''' 提供用户详情细信息 '''
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]

    # 重写get_object（self）方法，返回用户详情模型对象
    def get_object(self):
        return self.request.user

class EmailView(UpdateAPIView):
    ''' 更新邮箱信息'''
    serializer_class = EmailSerializer
    permission_classes = [IsAuthenticated]

    # 重写get_object（self）方法，返回用户详情模型对象
    def get_object(self):
        return self.request.user





















