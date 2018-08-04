from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^$', views.Order.as_view(), name='Order'),
    # url(r'^buy/(?P<sku_id>\d+)/(?P<sku_count>\d+)$',views.order.as_view()),
    url(r'^buy$', views.order.as_view()),
    url(r'^commit$', views.commit, name='order_commit'),
    url(r'^pay$', views.OrderPay.as_view(), name='order_pay'),
    url(r'^check$', views.OrderCheck.as_view(), name='order_check'),
]
