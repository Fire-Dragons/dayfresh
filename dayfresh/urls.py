from django.conf.urls import include, url
from django.contrib import admin
from goods.views import index

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user/', include('user.urls', namespace='user')),
    url(r'^user/', include('django.contrib.auth.urls')),
    url(r'^address/', include('address.urls', namespace='address')),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^goods/', include('goods.urls', namespace='goods')),
    url(r'^search/',include('haystack.urls')),
    url(r'^cart/',include('cart.urls')),
    url(r'^order/', include('order.urls')),
    url(r'^$', index.as_view()),
]
