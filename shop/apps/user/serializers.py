import re
from django_redis import get_redis_connection
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from .models import UserInfo


class CreateUserSerializer(serializers.ModelSerializer):
    '''注册序列化器'''
    # 序列化器的所有字段 ：['id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 需要校验的字段：[ 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # 模型中已经存在的字段 ['id', 'username', 'password',  'mobile'] 所以需要序列化器创建以下三个字段

    # 需要序列化的字段['id', 'username', 'mobile','token']
    # 需要反序列化的字段[ 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow']
    # write_only  只需要反序列化   read_only  只需要序列化
    password2 = serializers.CharField(label='确认密码', write_only=True)
    sms_code = serializers.CharField(label='短信验证码', write_only=True)
    allow = serializers.CharField(label='同意协议', write_only=True)
    token  = serializers.CharField(label='token',read_only=True)

    class Meta:
        model = UserInfo
        fields = ('id', 'username', 'password', 'password2', 'mobile', 'sms_code', 'allow','token')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许5-20个字符的⽤户名',
                    'max_length': '仅允许5-20个字符的⽤户名',
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '仅允许8-20个字符的密码',
                    'max_length': '仅允许8-20个字符的密码',
                }
            }
        }

    # 单个字段验证 validate_ 字段名 输入什么 返回什么
    def validate_mobile(self, value):
        if not re.match(r'^1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机格式错误！')
        return value

    def validate_allow(self, value):
        if value != 'true':
            raise serializers.ValidationError('请同意用户协议！')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次密码不一致！')
        # 取得短信验证码
        redis_conn = get_redis_connection('verify_codes')
        mobile = attrs['mobile']
        real_sms_code = redis_conn.get('sms_%s' % mobile)
        if attrs['sms_code'] !=real_sms_code.decode():  # 从redis数据库中提取的数据类型是byte型
            raise serializers.ValidationError('验证码错误！！')
        if real_sms_code ==None:
            raise serializers.ValidationError('无效的验证码！')
        return attrs

    #
    def create(self, validated_data):
        # validated_data 前端传过来的反序列化字典数据

        del validated_data['password2']
        del validated_data['sms_code']
        del validated_data['allow']

        password = validated_data.pop('password')
        user = UserInfo.objects.create(**validated_data)
        user.set_password(password)
        user.save()

        # 使用jwt生成token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)

        token = jwt_encode_handler(payload)

        user.token = token
        return user


