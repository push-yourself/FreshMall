from django.urls import path, re_path

from .views import RegisterView, ActiveView, LoginView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),# 注册操作
    path('login/',LoginView.as_view(),name='login'),# 注册操作
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),# 注册操作
]
