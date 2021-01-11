from django.db import models

# Create your models here.
from django.utils import timezone

class MechineInfo(models.Model):
    os_system = models.CharField(max_length=20)
    os_node = models.CharField(max_length=20)
    os_release = models.CharField(max_length=20)
    os_version = models.CharField(max_length=20)
    os_machine = models.CharField(max_length=20)
    os_processor = models.CharField(max_length=20)
    hostname = models.CharField(max_length=20)
    host_ip = models.CharField(max_length=20)
    uptime = models.CharField(max_length=20)
    mac_address  = models.CharField(max_length=50)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.os_name)


class MemInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)   # 使用插入数据时的当前时间作为数据的采集时间，不用去想插入的数据的格式问题。
    mem_used = models.CharField(max_length=50)
    mem_free = models.CharField(max_length=50)
    mem_total = models.CharField(max_length=50)
    mem_shared = models.CharField(max_length=50)
    mem_buff = models.CharField(max_length=50)
    mem_available = models.CharField(max_length=50)
    swap_total = models.CharField(max_length=50)
    swap_used = models.CharField(max_length=50)
    swap_free = models.CharField(max_length=50)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.mem_used)

class LoginFailed(models.Model):

    date = models.DateTimeField(default=timezone.now)
    fail_name = models.CharField(max_length=50)
    fail_ip = models.CharField(max_length=50)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.fail_ip)

class CPUInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cpu_temp = models.CharField(max_length=10)
    cpu_user = models.CharField(max_length=20)
    cpu_system = models.CharField(max_length=20)
    cpu_free = models.CharField(max_length=20)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.cpu_temp)


class DiskInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)
    mount_point = models.CharField(max_length=30)
    disk_type = models.CharField(max_length=20)
    disk_total = models.CharField(max_length=20)
    disk_used = models.CharField(max_length=20)
    disk_available = models.CharField(max_length=20)
    used_percent = models.CharField(max_length=20)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.mount_point)