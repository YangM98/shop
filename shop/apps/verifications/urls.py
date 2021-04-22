from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    # 发送短信
    url('^sms_code/(?P<mobile>1[3-9]\d{9})/$', views.SMSValidView.as_view()),
]
