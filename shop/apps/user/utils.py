import re

from django.contrib.auth.backends import ModelBackend
from .models import UserInfo


def jwt_response_payload_handler(token,user = None,request = None):

    return {
        'token':token,
        'username':user.username,
        'user_id':user.id
    }



def get_user_by_account(account):
    """
    根据帐号获取user对象
    :param account: 账号，可以是用户名，也可以是手机号
    :return: User对象 或者 None
    """
    try:
        if re.match('^1[3-9]\d{9}$', account):
            # 帐号为手机号
            user = UserInfo.objects.get(mobile=account)
        else:
            # 帐号为用户名
            user = UserInfo.objects.get(username=account)

    except UserInfo.DoesNotExist:
        return None
    else:
        return user

class UsernameMobileAuthBackend(ModelBackend):
    """
    自定义用户名或手机号认证 修改Django认证  实现多账号登陆
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        # 获取到user
        user = get_user_by_account(username)

        # django自带的用户认证模型  判断前端传入的密码是否正确
        if user is not None and user.check_password(password):
            return user


