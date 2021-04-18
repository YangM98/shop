from django.conf.urls import url
from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from . import views
urlpatterns = [
    # 新增数据
    path('user/',views.UserView.as_view()),
    # 检查username是否重复
    url(r'^usernames/(?P<username>\w{5,20})/count/$',views.usernameAPIView.as_view()),
    # 检查mobile是否重复
    url(r'^mobiles/(?P<mobile>1[3-9]\d{9})/count/$',views.mobileAPIView.as_view()),
    # 用户登录认证
    path('authorizations/', obtain_jwt_token),
]


