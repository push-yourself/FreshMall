from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
from db.base_model import BaseModel

# 继承抽象模型类(共有)
class User(AbstractUser,BaseModel):
    '''用户模型类'''
    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'# 单数
        verbose_name_plural = verbose_name# 复数


class Address(BaseModel):
    '''地址模型类'''
    receiver = models.CharField(max_length=20,verbose_name='收件人')
    addr = models.CharField(max_length=256,verbose_name='收件地址')
    zip_code = models.CharField(max_length=6,null=True,verbose_name='邮政编码')
    phone = models.CharField(max_length=11,verbose_name='联系方式')
    is_default = models.BooleanField(default=False,verbose_name='是否默认')
    # 外键字段
    user = models.ForeignKey('User',verbose_name='所属账户',on_delete=models.CASCADE)
