from django.shortcuts import render, redirect
from django.views.generic import View
from utils.minix_util import LoginRequiredMinix
from address.models import Address
from goods.models import *
from dayfresh.settings import redis_conn
from django.http import JsonResponse
from .models import *
from datetime import datetime
from django.db import transaction
from alipay import AliPay
from dayfresh.settings import *


class Order(LoginRequiredMinix, View):
    def post(self, request):
        user = request.user

        # 购物车
        cart_key = 'cart_%s' % user.id

        sku_ids = request.POST.getlist('sku_ids')
        if not all([sku_ids]):
            return redirect('/cart')
        # 购物车总量
        total_count = 0
        # 总价
        total_amount = 0
        # 地址
        addrs = Address.objects.filter(user=user.id)
        skus = []
        for sku_id in sku_ids:
            sku = GoodsSKU.objects.get(id=sku_id)
            count = redis_conn.hget(cart_key, sku_id)
            amount = sku.price * int(count)
            sku.amount = amount
            sku.count = count
            skus.append(sku)
            total_count += int(count)
            total_amount += amount

        # 运费
        transit_price = 10

        # 实付款
        total_pay = total_amount + transit_price

        sku_ids = '-'.join(sku_ids)

        context = {
            'skus': skus,
            'addrs': addrs,
            'total_amount': total_amount,
            'total_count': total_count,
            'total_pay': total_pay,
            'transit_price': transit_price,
            'sku_ids': sku_ids,
            'meth': '购物车'
        }
        return render(request, 'goods/place_order.html', context)


# 立即购买
class order(View):
    def post(self, request):
        user = request.user
        sku_id = request.POST.get('sku_id')
        sku_count = request.POST.get('sku_count')
        # 购物车总量
        total_count = 0
        # 总价
        total_amount = 0
        # 地址
        addrs = Address.objects.filter(user=user.id)
        skus = []
        sku = GoodsSKU.objects.get(id=sku_id)
        amount = sku.price * int(sku_count)
        sku.amount = amount
        sku.count = sku_count
        skus.append(sku)
        total_count += int(sku_count)
        total_amount += amount

        # 运费
        transit_price = 10

        # 实付款
        total_pay = total_amount + transit_price
        sku_ids = '-'.join(sku_id)
        context = {
            'skus': skus,
            'addrs': addrs,
            'total_amount': total_amount,
            'total_count': total_count,
            'total_pay': total_pay,
            'transit_price': transit_price,
            'sku_ids': sku_ids,
            'meth': '立即购买'
        }
        # response= render(request, 'goods/place_order.html', context)
        return render(request, 'goods/place_order.html', context)


@transaction.atomic
def commit(request):
    # 判断用户
    user = request.user
    if not user.is_authenticated():
        return JsonResponse({'res': 0, 'errmsg': '用户未登录'})
    # 获取参数
    sku_ids = request.POST.get('sku_ids')
    addr_id = request.POST.get('addr_id')
    pay_method = request.POST.get('pay_method')
    # 校验参数
    if not all([sku_ids, addr_id, pay_method]):
        return JsonResponse({'res': 1, 'errmsg': '数据不完整'})
    try:
        addr = Address.objects.get(id=addr_id)
    except Address.DoesNotExist:
        return JsonResponse({'res': 2, 'errmsg': '地址信息错误'})

    try:
        pay_method = int(pay_method)
    except ValueError:
        return JsonResponse({'res': 3, 'errmsg': '支付方式非法1'})
    if pay_method not in OrderInfo.PAY_METHODS.keys():
        return JsonResponse({'res': 3, 'errmsg': '支付方式非法'})
    # 构建order id
    order_id = datetime.now().strftime('%Y%m%d%H%M%S') + str(user.id)

    # 订单运费
    transit_price = 10

    # 商品的总数目和总价格
    total_count = 0
    total_price = 0
    sid = transaction.savepoint()
    print(1)
    try:
        # todo: 向df_order_info表中添加一条记录
        order = OrderInfo.objects.create(
            order_id=order_id,
            user=user,
            addr=addr,
            pay_method=pay_method,
            total_count=total_count,
            total_price=total_price,
            transit_price=transit_price
        )
        print(2)
        # todo:用户的订单中有几个商品，需要向df_order_goods表中加入几条记录
        cart_key = 'cart_%s' % user.id
        sku_ids = sku_ids.split('-')


        for sku_id in sku_ids:
            # 获取商品的信息

            try:
                # sku=GoodsSKU.objects.get(id=sku_id)
                sku = GoodsSKU.objects.select_for_update().get(id=sku_id)
            except:
                # 商品不存在，回滚到sid事务保存点
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 4, 'errmsg': '商品不存在'})

            if request.POST.get('meth') == '购物车':
                # 从redis中获取用户所要购买的商品数量
                count = redis_conn.hget(cart_key, sku_id)
            else:
                count = request.POST.get('sku_count')

            # todo:判断商品的库存

            if int(count) > sku.stock:
                transaction.savepoint_rollback(sid)
                return JsonResponse({'res': 6, 'errmsg': '商品库存不足'})

            # todo:更新商品的库存和销量
            sku.stock -= int(count)
            sku.sales += int(count)
            sku.save()

            # todo:向df_order_goods表中添加一条记录
            OrderGoods.objects.create(
                order=order,
                sku=sku,
                count=int(count),
                price=sku.price
            )

            # todo:累加计算订单商品的总数量和总价格
            amount = sku.price * int(count)
            total_count += int(count)
            total_price += amount

        order.total_count = total_count
        order.total_price = total_price
        order.save()

    except Exception as e:

        transaction.savepoint_rollback(sid)
        return JsonResponse({'res': 7, 'errmsg': '下单失败'})
    if request.POST.get('meth') == '购物车':
        # todo:清除用户购物车中对应的记录
        redis_conn.hdel(cart_key, *sku_ids)

    transaction.savepoint_commit(sid)
    # 返回应答
    return JsonResponse({'res': 5, 'errmsg': '创建成功'})


class OrderPay(View):
    def post(self, request):
        """订单支付"""
        # 用户登录判断
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 参数校验
        if not all([order_id]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

        # 校验订单信息
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          order_status=1,
                                          pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        # 业务处理: 使用python SDK调用支付宝的下单支付接口
        # 初始化

        alipay = AliPay(
            appid="2016091900545245",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=APP_PRIVATE_KEY_PATH,  # 网站私钥文件路径
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )

        total_pay = order.total_price + order.transit_price  # Decimal
        # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
        order_string = alipay.api_alipay_trade_page_pay(
            out_trade_no=order_id,  # 订单id
            total_amount=str(total_pay),  # 订单的实付款
            subject='天天生鲜%s' % order_id,  # 订单标题
            return_url=None,
            notify_url=None  # 可选, 不填则使用默认notify url
        )

        pay_url = 'https://openapi.alipaydev.com/gateway.do?' + order_string
        # 返回应答
        return JsonResponse({'res': 3, 'pay_url': pay_url})


class OrderCheck(View):
    def post(self, request):
        """订单支付查询"""
        # 用户登录判断
        user = request.user
        if not user.is_authenticated():
            return JsonResponse({'res': 0, 'errmsg': '用户未登录'})

        # 接收参数
        order_id = request.POST.get('order_id')

        # 参数校验
        if not all([order_id]):
            return JsonResponse({'res': 1, 'errmsg': '订单id为空'})

        # 校验订单信息
        try:
            order = OrderInfo.objects.get(order_id=order_id,
                                          user=user,
                                          order_status=1,
                                          pay_method=3)
        except OrderInfo.DoesNotExist:
            return JsonResponse({'res': 2, 'errmsg': '无效订单id'})

        # 业务处理: 使用python SDK调用支付宝的下单支付接口
        # 初始化

        alipay = AliPay(
            appid="2016091900545245",  # 应用id
            app_notify_url=None,  # 默认回调url
            app_private_key_path=APP_PRIVATE_KEY_PATH,  # 网站私钥文件路径
            alipay_public_key_path=ALIPAY_PUBLIC_KEY_PATH,  # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
            sign_type="RSA2",  # RSA 或者 RSA2
            debug=True  # 默认False, True代表沙箱环境
        )

        while True:
            response = alipay.api_alipay_trade_query(order_id)
            code = response.get('code')

            if code == '10000' and response.get('trade_status') == 'TRADE_SUCCESS':
                # 支付成功
                # 获取支付宝交易号
                trade_no = response.get('trade_no')
                # 更新订单状态，设置支付宝交易号
                order.order_status = 2  # 待发货
                order.trade_no = trade_no
                order.save()

                # 返回应答
                return JsonResponse({'res': 3, 'message': '支付成功'})
            elif code == '40004' or (code == '10000' and response.get('trade_status') == 'WAIT_BUYER_PAY'):
                # code == '40004': 支付交易订单还未创建，用户登录支付宝后就会创建
                # 等待买家付款
                import time
                time.sleep(5)
                continue
            else:
                # 支付失败
                return JsonResponse({'res': 4, 'errmsg': '支付失败'})
