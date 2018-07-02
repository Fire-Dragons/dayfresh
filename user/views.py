from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from dayfresh import myutil
from io import BytesIO
from user.models import *
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from django.views.generic.base import View  # 视图类模块
from dayfresh.settings import SECRET_KEY, EMAIL_FROM, DOMAIN
import random


# from email.mime.text import MIMEText
# import smtplib


def index(request):
    return render (request, './index.html')


class Login (View):
    def get(self, request):
        # 登录界面
        context = {}
        # 记住用户名的cookie是否存在
        if request.COOKIES.get ('cookie_user_name') != None:
            context['uname'] = request.COOKIES.get ('cookie_user_name')

        return render (request, 'user/login.html', context)

    def post(self, request):
        # 登录处理
        request_parmes = request.POST

        uname = request_parmes.get ('username')
        upasswd = request_parmes.get ('pwd')
        remember = request_parmes.get ('remember')
        upasswd = myutil.mymd5 (upasswd)

        if User.objects.filter (uname=uname, upasswd=upasswd).exists ():
            user = User.objects.filter (uname=uname, upasswd=upasswd)
            if user[0].is_activity == '0':
                return HttpResponse ({'is_activity': '0'})
            response = redirect ('/')
            # cookie
            if remember:
                response.set_cookie ('cookie_user_name', uname, 60 * 60 * 24)
        else:
            response = redirect ('/user/login')
        return response


class Register (View):
    def get(self, request):
        # 注册界面
        return render (request, 'user/register.html')

    def post(self, request):
        # 注册处理
        request_parmes = request.POST
        # 获取页面信息
        uname = request_parmes.get ('user_name')
        upasswd = request_parmes.get ('pwd')
        umail = request_parmes.get ('email')
        # 密码加密
        upasswd = myutil.mymd5 (upasswd)
        # 写入数据库
        user = User ()
        user.uname = uname
        user.upasswd = upasswd
        user.umail = umail
        user.is_activity = 1
        user.save ()
        request.session.flush ()
        return redirect ('/user/login')


# 检查用户名是否存在
def check_user_name(request):
    uname = request.GET.get ('uname')
    if User.objects.filter (uname=uname).exists ():
        return HttpResponse (1)
    else:
        return HttpResponse (0)


# 检查密码是否正确
def check_user_pwd(request):
    uname = request.GET.get ('uname')
    upwd = request.GET.get ('pwd')

    upwd = myutil.mymd5 (upwd)

    if User.objects.filter (uname=uname, upasswd=upwd).exists ():
        return HttpResponse (1)
    else:
        return HttpResponse (0)


# 验证码
def verificationcode(request):
    bgcolor = (random.randrange (20, 100), random.randrange (20, 100), 255)
    width = 100
    height = 40
    # 创建画面对象
    # im = Image.new('RGB', (width, height), bgcolor)
    im = Image.new ('RGB', (width, height), (255, 255, 255))
    # 创建画笔对象
    draw = ImageDraw.Draw (im)
    # 调用画笔的point()函数绘制噪点
    for i in range (0, 100):
        xy = (random.randrange (0, width), random.randrange (0, height))
        fill = (random.randrange (0, 255), 255, random.randrange (0, 255))
        draw.point (xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range (0, 4):
        rand_str += str1[random.randrange (0, len (str1))]
    # 构造字体对象
    font = ImageFont.truetype ('./static/ziti/Apple.ttf', 28)
    # 构造字体颜色
    fontcolor = (255, random.randrange (0, 255), random.randrange (0, 255))
    # 绘制4个字
    draw.text ((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text ((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text ((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text ((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 创建内存读写的对象
    buf = BytesIO ()
    # 将图片保存在内存中，文件类型为png
    im.save (buf, 'png')

    # 放入session中
    request.session['verificationcode'] = rand_str
    request.session.set_expiry (0)

    return HttpResponse (buf.getvalue (), 'image/png')


# 检查验证码
def check_yzm(request):
    request_parmes = request.GET

    verificationcode = request_parmes.get ('yzm')
    if request.session['verificationcode'].upper () != verificationcode.upper ():
        return HttpResponse (1)
    else:
        return HttpResponse (0)


# 发送用户激活验证邮件
def send_email(request):
    username = request.GET.get ('uname')
    umail = request.GET.get ('umail')
    # 生成随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len (chars) - 1
    for i in range (4):
        str += chars[random.randint (0, length)]
    # message = ("\n").join(
    #     [u'{0},欢迎加入'.format(username), u"验证码为:{0}\n".format(str), u'请访问该链接，完成用户验证:', DOMAIN + "?uname=" + username])
    #
    # msg = MIMEText(message, 'html')  # 设置正文为符合邮件格式的HTML内容
    # msg['subject'] = '账号激活认证'  # 设置邮件标题
    # msg['from'] = EMAIL_FROM  # 设置发送人
    # msg['to'] = umail  # 设置接收人
    # try:
    #     s = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)  # 注意！如果是使用SSL端口，这里就要改为SMTP_SSL
    #     s.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)  # 登陆邮箱
    #     s.sendmail(EMAIL_HOST_USER, umail, msg.as_string())  # 发送邮件！
    #     response = 1
    # except smtplib.SMTPException:
    #     response = 0

    upasswd = request.GET.get ('upasswd')
    # 密码加密
    upasswd = myutil.mymd5 (upasswd)
    # 发送邮件
    serializer = Serializer (SECRET_KEY, 3600)
    info = {'uname': username, 'upasswd': upasswd, 'umail': umail}
    token = serializer.dumps (info).decode ()
    subject = '天天生鲜注册'
    message = ''  # 文本内容
    sender = EMAIL_FROM
    receiver = [umail]
    html_message = '%s欢迎加入天天生鲜<br/>你的注册码为<span style="color:red">%s</span><br/>或访问该链接完成用户验证:<a href="%s?token=%s">点击完成注册</a>' % (username,str, DOMAIN, token)
    try:
        send_mail (subject, message, sender, receiver, html_message=html_message)
        response = 1
    except SignatureExpired as e:
        response = 0
    # 把用户信息写入session用于链接验证
    request.session['eyzm'] = str
    # request.session['uname'] = upasswd
    # request.session['upasswd'] = umail
    request.session.set_expiry(0)

    return HttpResponse (response)

class Activate(View):
    def get(self,request):
        token = None
        # 用户输入邮箱验证码验证
        if request.GET.get('token')==None:
            ueyzm = request.GET.get('ueyzm')
            eyzm = request.session['eyzm']
            ueyzm = ueyzm.upper()
            eyzm = eyzm.upper()
            if ueyzm == eyzm:
                return HttpResponse(1)
            else:
                return HttpResponse(0)
        else:
            # 用户点击链接验证
            serializer = Serializer(SECRET_KEY, 3600)
            try:
                token = request.GET.get('token')
                info = serializer.loads(token)
                uname = info['uname']
                upasswd = info['upasswd']
                umail = info['umail']
                user = User()
                user.uname = uname
                user.upasswd = upasswd
                user.umail = umail
                user.is_activity = 1
                user.save()
                response = redirect('/user/login')
            except SignatureExpired as e:
                response = HttpResponse('激活链接已过期')
            return response
# 用户输入邮箱验证码验证
# def activate(request):
#     # if request.GET.get('uyzm') == None:
#     #     print(request.session.keys())
#     #     uname = request.GET.get('uname')
#     #     upasswd = request.session['uname']
#     #     umail = request.session['upasswd']
#     #     user = User()
#     #     user.uname = uname
#     #     print(uname)
#     #     user.upasswd = upasswd
#     #     print(upasswd)
#     #     user.umail = umail
#     #     print(umail)
#     #     user.is_activity = 1
#     #     user.save()
#     #     return redirect('/user/login')
#     # else:
#     ueyzm = request.GET.get ('ueyzm')
#     eyzm = request.session['eyzm']
#     ueyzm = ueyzm.upper ()
#     print (eyzm)
#     print (ueyzm)
#     eyzm = eyzm.upper ()
#     if ueyzm == eyzm:
#         return HttpResponse (1)
#     else:
#         return HttpResponse (0)


