'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/7
@Program      : 
'''

from django.conf.urls import include, url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index.html', views.index, name='index'),
    path('cpu.html', views.cpu, name='cpu'),
    path('memory.html', views.memory, name='memory'),
    path('disk.html', views.disk, name='disk'),
    path('lastb.html', views.lastb, name='lastb'),
    path('config.html', views.config, name='config'),
    path('about.html', views.about, name='about'),
    path('login.html', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]
