from django.shortcuts import render,redirect
from PIL import Image,ImageDraw,ImageFont
from django.http import HttpResponse
from dayfresh import myutil
from io import BytesIO
from user.models import *
import random



def index(request):
    return render(request,'./index.html')


#登录界面
def login(request):

    context = {}
    if request.COOKIES.get('cookie_user_name') != None:
        context['uname'] = request.COOKIES.get('cookie_user_name')

    return render(request,'user/login.html',context)

#登录处理
def login_handle(request):
    request_parmes = request.POST

    uname = request_parmes.get('username')
    upasswd = request_parmes.get ('pwd')
    remember = request_parmes.get('remember')
    upasswd = myutil.mymd5(upasswd)

    if User.objects.filter(uname=uname,upasswd=upasswd).exists():
        user= User.objects.filter(uname=uname,upasswd=upasswd)
        if user[0].is_activity == '0':
            return HttpResponse({'is_activity':'0'})
        response = redirect ('/')
        #cookie
        if remember:
            response.set_cookie('cookie_user_name',uname,60*60*24)
    else:
        response = redirect('/user/login')
    return response

#注册界面
def register(request):
    return render(request,'user/register.html')

#注册处理
def register_handle(request):
    request_parmes = request.POST
    #获取页面信息
    uname = request_parmes.get('user_name')
    upasswd = request_parmes.get('pwd')
    umail = request_parmes.get('email')
    #密码加密
    upasswd = myutil.mymd5(upasswd)
    #写入数据库
    user = User()
    user.uname = uname
    user.upasswd = upasswd
    user.umail = umail
    user.save()

    return redirect('/user/login')

#检查用户名是否存在
def check_user_name(request):
    uname = request.GET.get('uname')
    if User.objects.filter(uname=uname).exists():
        return HttpResponse(1)
    else:
        return HttpResponse(0)

#检查密码是否正确
def check_user_pwd(request):
    uname = request.GET.get('uname')
    upwd = request.GET.get('pwd')

    upwd = myutil.mymd5(upwd)

    if User.objects.filter(uname=uname,upasswd=upwd).exists():
        return HttpResponse(1)
    else:
        return HttpResponse(0)

#验证码
def verificationcode(request):
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    # im = Image.new('RGB', (width, height), bgcolor)
    im = Image.new('RGB', (width, height), (255,255,255))
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象
    font = ImageFont.truetype('arial.ttf', 23)
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    #创建内存读写的对象
    buf = BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')

    #放入session中
    request.session['verificationcode'] = rand_str
    request.session.set_expiry(0)

    return HttpResponse(buf.getvalue(), 'image/png')

def check_yzm(request):
    request_parmes = request.GET

    verificationcode = request_parmes.get ('yzm')
    if request.session['verificationcode'].upper () != verificationcode.upper ():
        return HttpResponse(1)
    else:
        return HttpResponse(0)