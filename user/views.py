from django.shortcuts import render, redirect
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse
from io import BytesIO
from user.models import *
from django.core.mail import send_mail
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
from django.views.generic.base import View  # 视图类模块
from dayfresh.settings import SECRET_KEY, EMAIL_FROM, DOMAIN
from django.contrib.auth import authenticate, login,logout  # 用户认证
from django.contrib.auth.decorators import login_required
import random
from django.core.paginator import Paginator
from order.models import *


#登录
class Login (View):
    def get(self, request):
        # 登录界面
        # 记住用户名的cookie是否存在
        if request.COOKIES.get ('cookie_user_name') != None:
            uname = request.COOKIES.get ('cookie_user_name')
            checked = 'checked'
        else:
            uname = ''
            checked = ''
        return render (request, 'user/login.html', {'uname': uname, 'checked': checked})

    def post(self, request):

        # 登录处理
        request_parmes = request.POST
        uname = request_parmes.get ('username')
        upasswd = request_parmes.get ('pwd')
        remember = request_parmes.get ('remember')

        # 用户认证
        user = authenticate (username=uname, password=upasswd)
        if user != None:
            next_url=request.GET.get('next','/')
            if user.is_active == '0':
                return HttpResponse ({'is_activity': '0'})
            login (request, user)
            response=redirect(next_url)
            # cookie
            if remember:
                response.set_cookie ('cookie_user_name', uname, max_age=60 * 60 * 24)
            else:
                response.delete_cookie ('cookie_user_name')
        else:
            response = redirect ('/user/login')

        return response

#注册
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

        # 写入数据库
        user = User.objects.create_user (username=uname, email=umail, password=upasswd)
        user.is_activity = True
        user.save ()
        request.session.clear ()
        request.session.flush ()
        return redirect ('/user/login')


# 检查用户名是否存在
def check_user_name(request):
    uname = request.GET.get ('uname')

    if User.objects.filter (username=uname).exists ():
        return HttpResponse (1)
    else:
        return HttpResponse (0)


# 检查密码是否正确
def check_user_pwd(request):
    uname = request.GET.get ('uname')
    upwd = request.GET.get ('pwd')

    user = authenticate (username=uname, password=upwd)
    if user != None:
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
    upasswd = request.GET.get ('upasswd')
    umail = request.GET.get ('umail')
    # 生成随机字符串
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len (chars) - 1
    for i in range (4):
        str += chars[random.randint (0, length)]

    # 发送邮件
    serializer = Serializer (SECRET_KEY, 3600)
    info = {'uname': username, 'upasswd': upasswd, 'umail': umail}
    token = serializer.dumps (info).decode ()
    subject = '天天生鲜注册'
    message = ''  # 文本内容
    sender = EMAIL_FROM
    receiver = [umail]
    html_message = '%s欢迎加入天天生鲜<br/>你的注册码为<span style="color:red">%s</span><br/>或访问该链接完成用户验证:<a href="%s?token=%s">点击完成注册</a>' % (
        username, str, DOMAIN, token)
    try:
        send_mail (subject, message, sender, receiver, html_message=html_message)
        response = 1
    except SignatureExpired as e:
        response = 0
        #验证码写入session
    request.session['eyzm'] = str
    request.session.set_expiry (0)

    return HttpResponse (response)

#激活
class Activate (View):
    def get(self, request):
        token = None
        # 用户输入邮箱验证码验证
        if request.GET.get ('token') == None:
            ueyzm = request.GET.get ('ueyzm')
            eyzm = request.session['eyzm']
            ueyzm = ueyzm.upper ()
            eyzm = eyzm.upper ()
            if ueyzm == eyzm:
                return HttpResponse (1)
            else:
                return HttpResponse (0)
        else:
            # 用户点击链接验证
            serializer = Serializer (SECRET_KEY, 3600)
            try:
                token = request.GET.get ('token')
                info = serializer.loads (token)
                uname = info['uname']
                upasswd = info['upasswd']
                umail = info['umail']
                user = User.objects.create_user (username=uname, email=umail, password=upasswd)
                user.is_activity = 1
                user.save ()
                response = redirect ('/user/login')
            except SignatureExpired as e:
                response = HttpResponse ('激活链接已过期')
            return response



#个人信息
@login_required
def user_center_info(request):
    page='info'

    user = request.user
    from dayfresh.settings import redis_conn
    from goods.models import GoodsSKU
    history_key = 'history_%s' % user.id

    sku_ids = redis_conn.lrange(history_key, 0, 4)
    # 获取对应的商品信息
    skus = []
    for sku_id in sku_ids:
        sku = GoodsSKU.objects.get(id=sku_id)
        skus.append(sku)

    return render(request,'user/user_center_info.html',{'page':page,'skus':skus})

#全部订单
@login_required
def user_center_order(request,page):
    user = request.user
    orders = OrderInfo.objects.filter(user=user).order_by('-create_time')
    for order in orders:
        order_skus = OrderGoods.objects.filter(order=order)
        for order_sku in order_skus:
            amount = order_sku.count * order_sku.price
            order_sku.amount = amount

        total_pay = order.total_price + order.transit_price
        order.total_pay = total_pay

        status_name = OrderInfo.ORDER_STATUS[order.order_status]
        order.status_name = status_name

        order.order_skus = order_skus

    paginator = Paginator(orders, 1)
    page = int(page)
    if page > paginator.num_pages:
        page = 1
    order_page = paginator.page(page)
    pages=paginator.page_range

    context = {
        'order_page': order_page,
        'pages': pages,
        'page': 'order',
        'pageid':page
    }

    return render(request,'user/user_center_order.html',context)

#登出
def logout_view(request):
    logout(request)
    return redirect('/')
