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
    path('memery.html', views.memery, name='memery'),
    path('disk.html', views.disk, name='disk'),
    path('config.html', views.config, name='config'),
    path('about.html', views.about, name='about'),
]
