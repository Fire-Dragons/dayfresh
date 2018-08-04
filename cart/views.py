from django.shortcuts import render
from django.http.response import JsonResponse,HttpResponse
from goods.models import *
from dayfresh.settings import redis_conn
from django.views.generic import View
from utils.minix_util import LoginRequiredMinix


def get_cart_count(user):
    '''获取用户的购物车购买商品的总数'''

    cart_key = 'cart_%s' % user.id
    #获取信息
    cart_dict=redis_conn.hgetall(cart_key)
    #保存用户购物车中商品的总数目
    total_count=0
    #遍历获取商品的信息
    for sku_id,count in cart_dict.items():
        total_count+=int(count)
    return total_count

class Get_cart_count(View):
    def get(self,request):
        user=request.user
        cart_count=get_cart_count(user)
        return HttpResponse(cart_count)


def cart_add(request):
    user=request.user
    sku_id=request.POST['sku_id']
    count=request.POST['count']

    #验证用户是否登录
    if user.is_authenticated():

        #校验数据是否完整
        if not all([sku_id,count]):
            return JsonResponse({'res':0,'errmsg':'数据不完整'})

        #校验商品数量
        try:
            count=int(count)
        except Exception as e:
            #数目出错
            return JsonResponse({'res':2,'errmsg':'商品数目出错'})

        #校验商品是否存在
        try:
            sku=GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            #商品不存在
            return JsonResponse({'res':3,'errmsg':'商品不存在'})

        # redis连接,添加购物车记录
        # 拼接key
        cart_key = 'cart_%s' % user.id
        #先尝试获取sku_id的值 ->hget cart_key 属性
        #如果sku_id在hash中不存在，hget返回None
        cart_count=redis_conn.hget(cart_key,sku_id)
        if cart_count:
            #累加购物车中商品的数目
            count+=int(cart_count)

        #校验商品的库存
        if count>sku.stock:
            return JsonResponse({'res':4,'errmsg':'商品库存不足'})

        #设置hash中sku_id对应的值
        #hset -> 如果sku_id已经存在，更新数据，如果sku_id不存在，添加数据
        redis_conn.hset(cart_key,sku_id,count)

        #计算用户购物车商品的条目数
        total_count=get_cart_count(user)

        response=JsonResponse({'res':5,'cart_count':total_count})

    else:
        response=JsonResponse({'errmsg':'请先登录'})
    return response


class Cart_List(LoginRequiredMinix,View):
    def get(self,request):
        context={}
        user=request.user
        if user.is_authenticated:
            cart_key='cart_%s'%user.id
            cart_dict=redis_conn.hgetall(cart_key)

            skus=[]
            total_count=0
            total_amount=0

            for sku_id,count in cart_dict.items():
                sku=GoodsSKU.objects.get(id=sku_id)
                sku.count=count
                sku.amount=sku.price*int(count)
                skus.append(sku)
                total_count+=int(count)
                total_amount+=sku.amount

            context={
                'skus':skus,
                'total_count':total_count,
                'total_amount':total_amount
            }
            return render(request, 'goods/cart.html', context)

#购物车更新
class Cart_Update(View):
    def post(self,request):
        user=request.user
        if not user.is_authenticated:
            return JsonResponse({'res':0,'errmsg':'用户未登录'})

        sku_id=request.POST.get('sku_id')
        count=request.POST.get('count')
        #校验参数
        if not all([sku_id,count]):
            return JsonResponse({'res':1,'errmsg':'参数不完整'})

        #校验商品id
        try:
            sku=GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res':2,'errmsg':'商品不存在'})

        #校验商品的数量
        try:
            count=int(count)
        except Exception as e:
            return JsonResponse({'res':3,'errmsg':'商品数目不正确'})
        if count<=0:
            return JsonResponse({'res': 3, 'errmsg': '商品数目不正确'})
        if count>sku.stock:
            return JsonResponse({'res': 4, 'errmsg': '商品库存不足'})

        #连接redis，修改数据
        cart_key='cart_%s'%user.id
        redis_conn.hset(cart_key,sku_id,count)

        return JsonResponse({'res':5,'message':'更新成功'})

class Cart_Delete(View):
    def post(self,request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        sku_id = request.POST.get('sku_id')
        # 校验参数
        if not all([sku_id]):
            return JsonResponse({'res': 1, 'errmsg': '参数不完整'})

        # 校验商品id
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except GoodsSKU.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '商品不存在'})


        # 连接redis，修改数据
        cart_key = 'cart_%s' % user.id
        redis_conn.hdel(cart_key, sku_id)
        total_count=get_cart_count(user)
        return JsonResponse({'res': 3, 'message': '更新成功','cart_count':total_count})