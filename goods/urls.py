from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^detail/(?P<sku_id>\d+)$', views.detail.as_view(), name='detail'),
    url(r'^goods_list/(\d+)/(\d+)/(\d+)$', views.goods_list.as_view(), name='goods_list'),
]
