from django.conf.urls import url

from . import views

app_name = 'wechattest'
urlpatterns = [
    url(r'^fromwechat/$', views.fromwechat, name='fromwechat'),
    url(r'^showqrcode/$', views.showqrcode, name='showqrcode'),
]
