from django.db import models
from user.models import UserInfo
from shop.utils.models import BaseModel


class OauthQQUser(BaseModel):
    user = models.ForeignKey(UserInfo, on_delete=models.CASCADE, verbose_name='用户')
    openid = models.CharField(max_length=64, verbose_name='openid', db_index=True)  # db_index 数据库优化

    class Meta:
        db_table = 'tb_oauth_qq'
        verbose_name = 'QQ用户信息'
        verbose_name_plural = verbose_name
