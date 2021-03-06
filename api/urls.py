'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/7
@Program      : 
'''

from django.conf.urls import include, url
from rest_framework import routers
from api import views

route = routers.DefaultRouter()

route.register(r'meminfo', views.MemInfoView)
route.register(r'loginfailed', views.LoginFailedView)
route.register(r'diskinfo', views.DiskInfoView)
route.register(r'mechineinfo', views.MechineInfoView)
route.register(r'cpuinfo', views.CPUInfoView)

urlpatterns = [
    url('api/', include(route.urls)),
]
