from django.shortcuts import render
from QQLoginTool.QQtool import OAuthQQ
# Create your views here.
from rest_framework.views import APIView
from django.conf import settings


class QQAuthURLView(APIView):

    def get(self,request):

        next = request.query_params.get('next')
        pass







