from django.urls import path, re_path
from django.contrib.auth.decorators import login_required
from .views import RegisterView, ActiveView, LoginView, UserInfoView, AddressView, UserOrderView

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),# 注册操作
    path('login/',LoginView.as_view(),name='login'),# 登录操作
    re_path(r'^active/(?P<token>.*)$',ActiveView.as_view(),name='active'),# 激活操作
    #login_required装饰器会在url下面添加next变量;http://127.0.0.1:8000/user/login/?next=/user/
    path('',UserInfoView.as_view(),name='user'),# 用户中心/user/
    path('address/',AddressView.as_view(),name='address'),# 用户地址信息/user/addrerss
    path('order/',UserOrderView.as_view(),name='order')# 用户订购信息/user/order

]
