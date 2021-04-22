from django.urls import path
from . import views
urlpatterns = [
    path('qq/authorization/',views.QQAuthURLView.as_view()),
    path('qq/user/',views.QQAuthUserView.as_view()),
]
