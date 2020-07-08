from django.urls import path, include, re_path

from .views import IndexView, DetailView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),  # 首页
    re_path(r'^(?P<goods_id>\d+)$', DetailView.as_view(), name='detail'),  # 商品详情页
]