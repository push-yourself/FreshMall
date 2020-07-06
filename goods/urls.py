from django.urls import path, include

from .views import IndexView

urlpatterns = [
    path('index', IndexView.as_view(), name='index'),  # 首页
]