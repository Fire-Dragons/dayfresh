from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^login$',views.login),
    url(r'^login_handle$',views.login_handle),
    url(r'^register$',views.register),
    url(r'^register_handle$',views.register_handle),
    url(r'^check_user_name$',views.check_user_name),
    url(r'^check_user_pwd$',views.check_user_pwd),
    url(r'^verificationcode$',views.verificationcode),
    url(r'^check_yzm$',views.check_yzm),
    url(r'^send_email$',views.send_email),
    url(r'^activate$',views.activate),

]