from django.shortcuts import render, redirect
from django.views.generic.base import View
from .models import *
from django.core.cache import cache
from dayfresh.settings import redis_conn
from django.core.paginator import Paginator
from cart.views import get_cart_count


class index(View):
    def get(self, request):

        context = cache.get('cache_index_page_data')
        if context == None:
            # 商品种类
            types = GoodsType.objects.all()

            # 首页轮播
            index_banner = IndexGoodsBanner.objects.all().order_by('index')

            # 首页促销
            promotion_banner = IndexPromotionBanner.objects.all().order_by('index')

            # 首页分类展示详情
            for type in types:
                type.title_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=0).order_by('index')
                type.image_banner = IndexTypeGoodsBanner.objects.filter(type=type, display_type=1).order_by('index')

            context = {
                'types': types,
                'index_banner': index_banner,
                'promotion_banner': promotion_banner,
            }

            cache.set('cache_index_page_data', context, 3600)

        # 购物车数量
        user = request.user
        if user.is_authenticated:
            cart_count = get_cart_count(user)
        else:
            cart_count = 0
        context.update(cart_count=cart_count)

        return render(request, 'goods/index.html', context)


class detail(View):
    def get(self, request, sku_id):
        context = {}
        try:
            sku = GoodsSKU.objects.get(id=sku_id)
        except:
            return redirect('/')
        context['sku'] = sku

        # 新品推荐
        new_skus = GoodsSKU.objects.exclude(id=sku_id).filter(type=sku.type).order_by('-create_time')[:2]
        context['new_skus'] = new_skus

        # 其他规格
        same_spu_skus = GoodsSKU.objects.exclude(id=sku_id).filter(type=sku.type)
        context['same_spu_skus'] = same_spu_skus

        sku_images = sku.goodsimage_set.all()
        context['sku_images'] = sku_images

        # 用户浏览记录
        user = request.user
        if user.is_authenticated():
            # redis连接

            # 拼接key
            history_key = 'history_%s' % user.id
            # 如果已浏览过则从redis中移除
            redis_conn.lrem(history_key, 0, sku_id)
            # 添加
            redis_conn.lpush(history_key, sku_id)
            # 购物车数量
            cart_count=get_cart_count(user)
        else:
            cart_count = 0
        context['cart_count'] = cart_count
        types = GoodsType.objects.all()
        context['types']=types

        return render(request, 'goods/detail.html', context)


class goods_list(View):
    def get(self, request, typeid, pageid, sort):
        """
            url中的参数依次代表
            typeid:商品类型;
            pageid:页数
            sort:查询条件，1默认，2根据价格查询，3根据点击量查询
            """
        # 获取最新发布的商品
        new_skus = GoodsSKU.objects.all().order_by('-create_time')[:2]
        # 根据条件查询所有商品
        if sort == '1':  # 按
            sumGoodList = GoodsSKU.objects.filter(type=typeid)
        elif sort == '2':  # 按价格从低到高
            sumGoodList = GoodsSKU.objects.filter(type=typeid).order_by('price')
        elif sort == '3':  # 按人气
            sumGoodList = GoodsSKU.objects.filter(type=typeid).order_by('-sales')
        # 分页
        paginator = Paginator(sumGoodList, 1)
        goodList = paginator.page(int(pageid))
        pindexlist = paginator.page_range

        goodtype = GoodsType.objects.get(id=typeid)
        types = GoodsType.objects.all()

        # 购物车数量
        user = request.user
        if user.is_authenticated:
            cart_count = get_cart_count(user)
        else:
            cart_count = 0

        context = {'list': 1,
                   'guest_cart': 1,
                   'goodtype': goodtype,
                   'new_skus': new_skus,
                   'goodList': goodList,
                   'typeid': typeid,
                   'sort': sort,
                   'pindexlist': pindexlist,
                   'pageid': int(pageid),
                   'cart_count': cart_count,
                   'types': types,
                   }

        # 渲染返回结果
        return render(request, 'goods/list.html', context)
