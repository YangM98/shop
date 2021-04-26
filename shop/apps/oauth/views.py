from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
from rest_framework import status
from rest_framework.response import Response
from .models import OauthQQUser
from rest_framework.views import APIView
from django.conf import settings
from rest_framework_jwt.settings import api_settings
from . import utils
from . import serializers
# Create your views here.
#logger = settings.LOGGING()

class QQAuthURLView(APIView):
    '''获取qq认证路径'''
    def get(self,request):
        # next 表示从哪个界面进入到登录界面  登陆之后再返回到之前的页面
        next = request.query_params.get('next')
        if not next:
            next = '/'
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID,client_secret=settings.QQ_CLIENT_SECRET
                        ,redirect_uri=settings.QQ_REDIRECT_URI,state=next)
        # 构建qq认证的url
        login_url = oauth.get_qq_url()

        return Response({'login_url':login_url})


class QQAuthUserView(APIView):
    ''' 创建Oauth对象 调用函数 获取token值  再通过token 获取到openID

    '''
    def get(self,request):
        code = request.query_params.get('code')
        if not code:
            return Response({'message':'code值为空'},status=status.HTTP_400_BAD_REQUEST)
        # 得到code值 使用加密方式
        oauth = OAuthQQ(client_id=settings.QQ_CLIENT_ID, client_secret=settings.QQ_CLIENT_SECRET
                        , redirect_uri=settings.QQ_REDIRECT_URI)
        try:
            access_t = oauth.get_access_token(code=code)
            # 每个QQ的openid是固定的
            openid = oauth.get_open_id(access_token=access_t)
        except Exception as e:
            #logger.info(e)
            return  Response({'message':'QQ服务器异常'},status=status.HTTP_503_SERVICE_UNAVAILABLE)
        # 使用openID查询该qq是否在商城绑定过用户
        # 如果没有绑定 则将openID加密后返回前端暂时存储一下 以便后面绑定用户时使用
        # 如果绑定了 则手动生成JWT_token 返回到前端

        try:
            oauthUser_model = OauthQQUser.objects.get(openid=openid)
        except OauthQQUser.DoesNotExist:
            access_token = utils.generate_user_openid_token(openid)
            return  Response({'access_token':access_token})
        else:
            # 使用jwt生成token
            jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
            jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
            # 从QQ模型中获取关联的user
            user = oauthUser_model.user

            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            return Response({
                'user_id':user.id,
                'username' :user.username,
                'token':token
            })

    def post(self,request):
        ''' 使用 openid 绑定用户'''
        serializer = serializers.QQauthUserSerializer(data=request.data)
        # 校验数据
        serializer.is_valid()
        # 保存校验结果 并接收数据
        user = serializer.save()
        # 使用jwt生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        return Response({
            'user_id': user.id,
            'username': user.username,
            'token': token
        })















