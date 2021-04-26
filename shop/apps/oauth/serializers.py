from django_redis import get_redis_connection
from rest_framework import serializers
from .models import OauthQQUser
from user.models import  UserInfo
from .utils import check_user_token_openid
class QQauthUserSerializer(serializers.ModelSerializer):
    # 需要反序列化 字段 username password mobile sms_code access_token
    sms_code = serializers.CharField(label='验证码')
    mobile = serializers.RegexField(label='手机号',regex=r'^1[3-9]\d{9}$')
    password = serializers.CharField(label='密码',min_length=8,max_length=20)
    access_token = serializers.CharField(label='openid',max_length=128)

    def validate(self, attrs):
        # 对openid进行及解密 获取到openid
        access_token = attrs['access_token']
        openid = check_user_token_openid(access_token)
        if not openid:
            raise serializers.ValidationError('无效的openid')

        # 获取到短信验证码 从redis数据库中取得并进行校验
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_code = redis_conn.get('sms_%s' %mobile)
        if attrs['sms_code'] != real_code.decode():
            raise serializers.ValidationError('验证码错误！')
        if real_code == None:
            raise serializers.ValidationError('无效的验证码！')
        try:
            user = UserInfo.objects.get(mobile = mobile)
        except UserInfo.DoesNotExist:
            pass
        else:
            password = attrs['password']
            if not user.check_password(password):
                raise serializers.ValidationError('密码错误')
            attrs['user'] = user

        return attrs

        # 通过手机号寻找用户 如果有 则将openid 与用户进行绑定
        # 如果没有 则需要新建用户 再将openid与用户进行绑定
    def create(self, validated_data):
        user = validated_data.get('user')

        if not user:
            # 用户不存在 则新建用户
            user = UserInfo.objects.Create_user(
                username = validated_data['mobile'],
                password = validated_data['password'],
                mobile = validated_data['mobile'],
            )
        OauthQQUser.objects.create(
            openid=validated_data['open_id'],
            user = user
        )
        return user




