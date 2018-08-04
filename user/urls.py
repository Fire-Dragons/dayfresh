from django.conf.urls import url,include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    url (r'^login$', views.Login.as_view(),name='login'),
    url (r'^logout$', views.logout_view,name='logout'),#用户登出
    url (r'^register$', views.Register.as_view (),name='register'),
    url (r'^check_user_name$', views.check_user_name),
    url (r'^check_user_pwd$', views.check_user_pwd),
    url (r'^verificationcode$', views.verificationcode),
    url (r'^check_yzm$', views.check_yzm),
    url (r'^send_email$', views.send_email),
    # url (r'^activate/$', views.activate),
    # url (r'^activate/(?P<token>.*)$', views.activates),# 提取出activate后的所有字符赋给token
    url (r'^activate', views.Activate.as_view ()),


    # 密码重置链接
    url (r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    # 密码重置邮件发送完成后的页面
    url (r'^password_reset_done$', auth_views.password_reset_done, name='password_reset_done'),
    # 用户通过邮箱打开的重置密码页面
    url (r'^password_reset_confirm$', auth_views.password_reset_confirm, name='password_reset_confirm'),
    # 密码重置完成后跳转的页面
    url (r'^password_reset_complete$', auth_views.password_reset_complete, name='password_reset_complete'),

    url (r'^user_center_info$', views.user_center_info),
    url (r'^user_center_order/(?P<page>\d+)$', views.user_center_order,name='order'),


]
