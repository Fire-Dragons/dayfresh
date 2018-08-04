from django.conf.urls import include, url
from . import views

urlpatterns = [
    url(r'^$',views.address.as_view(),name='address'),
    url(r'^update/(\d+)$',views.Update.as_view(),name='update'),
    url (r'^remove/(\d+)$', views.remove, name='update'),
    url (r'^set_default/(\d+)$', views.set_default, name='update'),

]
