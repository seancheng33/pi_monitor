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
        model = MemInfo
        fields = ('pk', 'date', 'mem_used', 'mem_free', 'mem_total', 'mem_shared', 'mem_buff', 'mem_available', 'swap_total', 'swap_used', 'swap_free',)


class LoginFailedSerrializers(serializers.ModelSerializer):
    class Meta:
        model = LoginFailed
        fields = ('pk', 'date', 'fail_name', 'fail_ip',)

class DiskInfoSerrializers(serializers.ModelSerializer):
    class Meta:
        model = DiskInfo
        fields = ('pk', 'date', 'mount_point', 'disk_type', 'disk_total', 'disk_used', 'disk_available', 'used_percent',)

class MechineInfoSerrializers(serializers.ModelSerializer):
    class Meta:
        model = MechineInfo
        fields = ('pk', 'os_system', 'os_node', 'os_release', 'os_version', 'os_machine', 'os_processor', 'hostname', 'host_ip', 'uptime', 'mac_address',)