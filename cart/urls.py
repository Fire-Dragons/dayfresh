from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^add$', views.cart_add, name='cart_add'),
    url(r'^update$', views.Cart_Update.as_view(), name='cart_update'),
    url(r'^delete$', views.Cart_Delete.as_view(), name='cart_delete'),
    url(r'^total',views.Get_cart_count.as_view()),
    url(r'^$', views.Cart_List.as_view(), name='cart_list'),
]
