'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/7
@Program      : 
'''
from rest_framework import serializers
from .models import *


class MemInfoSerrializers(serializers.ModelSerializer):
    class Meta:
        model = MemInfoModel
        fields = ('pk', 'date', 'mem_used', 'mem_free', 'mem_total',)


class LoginFailedSerrializers(serializers.ModelSerializer):
    class Meta:
        model = LoginFailedModel
        fields = ('pk', 'date', 'fail_name', 'fail_ip',)
