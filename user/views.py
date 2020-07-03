from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password
from django.core.mail import send_mail
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
import re
# Create your views here.
from django.urls import reverse
from django.views.generic.base import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired

from freshmall.settings import SECRET_KEY, EMAIL_FROM
from user.models import User
from utils.mixin import LoginRequiredMixin


class RegisterView(View):
    def get(self,request:HttpRequest):
        '''注册页面处理'''
        return render(request,'register.html')

    def post(self,request):
        # 1.接收数据
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        # 2.数据校验
        if not all([username, password, email]):
            # 提交数据不完整
            return render(request, 'register.html', {'errmsg': '数据不完整'})
        # 校验邮箱
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errmsg': '邮箱格式不合法'})
        # 校验密码是否一致
        if allow != 'on':
            return render(request, 'register.html', {'errmsg': '请同意协议'})
        # 校验用户名是否重复
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            # 用户名不存在
            user = None
        if user:
            # 用户存在的处理
            return render(request, 'register.html', {'errmsg': '用户名已存在'})
        # 3.进行业务处理：用户注册(Django中的用户表可以直接使用)
        user = User.objects.create_user(username, email, password)
        user.is_active = 0
        user.save()
        # 附加功能：发送激活邮件，包含激活链接(激活链接中需要包含用户的身份信息)
        # 采用自定义标识：http://127.0.0.1:8000/user/active/uid   注意：对用户身份信息进行加密，使用itsdangerous
        # 1.加密用户的身份信息，生成激活token
        serializer = Serializer(SECRET_KEY,3600)
        info = {'confirm':user.id}# 根据情况去自定义数据类型
        token = serializer.dumps(info).decode()
        #2.发送邮件
        # 组织邮件信息
        subject = 'freshmall用户激活'
        message = '<a href="http://127.0.0.1:8000/user/active/%s">点击激活</a>' % (token)
        sender = EMAIL_FROM
        receiver = [email]
        html_msg = message  # 如果含有html标签，则使用html_message
        # 会可能出现阻塞，耗时严重·采用异步实现「
        send_mail(subject, message, sender, receiver, html_message=message)
        # 4.返回应答(注册成功之后，跳转至首页)
        return redirect(reverse('goods:index'))


class ActiveView(View):
    '''用户激活'''
    def get(self,request,token):
        '''进行用户激活解密操作'''
        serializer = Serializer(SECRET_KEY, 3600)
        try:
            info = serializer.loads(token)
            # 获取用户ID
            user_id = info['confirm']
            user = User.objects.get(id=user_id)
            user.is_active = 1# 修改激活状态
            user.save()
            # 返回应答,跳转至登录页面
            return redirect(reverse('user:login'))

        except SignatureExpired as e:
            # 激活链接过期
            return HttpResponse('激活链接已过期')


class LoginView(View):
    '''登录'''
    def get(self,request):
        # 判断是否记住了用户名
        if 'username' in request.COOKIES:
            username = request.COOKIES.get('username')
            checked = 'checked'
        else:
            username = ''
            checked = ''
        return render(request,'login.html',{'username':username, 'checked':checked})

    def post(self,request):
        '''登录校验'''
        #1.接收数据
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        #2. 校验
        if not all([username,password]):
            return render(request,'login.html',{'errmsg':'数据不完整'})
        #3.业务处理
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_active:
                try:
                    login(request,user)
                except Exception as e:
                    print('**：',e)
                # 获取登录后需要跳转的地址:http://127.0.0.1:8000/user/login/?next=/user/
                # 如果没有,默认跳转至首页
                next_url = request.GET.get('next',reverse('goods:index'))
                print(next_url)
                response =  redirect(next_url)
                # 判断是否需要记住用户名
                remember = request.POST.get('remember')
                if remember == 'on':
                    response.set_cookie('username', username, max_age=7*24*3600)
                else:
                    response.delete_cookie('username')
                return response

            else:
                return render(request, 'login.html', {'errmsg': '账户未激活'})
        else:
            return render(request, 'login.html', {'errmsg': '密码错误'})

# /user
class UserInfoView(LoginRequiredMixin,View):
    '''用户中心'''
    def get(self,request):
        '''显示'''
        print('================fttr===============')
        return render(request,'user_center_info.html',{'page':'user'})

# /user/address
class AddressView(LoginRequiredMixin,View):
    '''用户地址中心'''
    def get(self,request):
        '''显示'''
        return render(request,'user_center_site.html',{'page':'address'})


# /user/order
class UserOrderView(LoginRequiredMixin,View):
    '''用户订购中心'''
    def get(self,request):
        '''显示'''
        return render(request,'user_center_order.html',{'page':'order'})