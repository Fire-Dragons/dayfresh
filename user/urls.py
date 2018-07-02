from django.conf.urls import url
from . import views

urlpatterns = [
    url (r'^login$', views.Login.as_view()),
    url (r'^register$', views.Register.as_view()),
    url (r'^check_user_name$', views.check_user_name),
    url (r'^check_user_pwd$', views.check_user_pwd),
    url (r'^verificationcode$', views.verificationcode),
    url (r'^check_yzm$', views.check_yzm),
    url (r'^send_email$', views.send_email),
    url (r'^activate/$', views.activate),
    url (r'^activate/(?P<token>.*)$', views.activates),

]
