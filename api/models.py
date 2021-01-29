from django.db import models

# Create your models here.
from django.utils import timezone

class MechineInfo(models.Model):
    os_system = models.CharField(max_length=50, default="")
    os_node = models.CharField(max_length=50, default="")
    os_release = models.CharField(max_length=50, default="")
    os_version = models.CharField(max_length=50, default="")
    os_machine = models.CharField(max_length=50, default="")
    hostname = models.CharField(max_length=50, default="")
    host_ip = models.CharField(max_length=50, default="")
    uptime = models.CharField(max_length=50, default="")
    mac_address = models.CharField(max_length=50, default="")
    cpu_num = models.CharField(max_length=50, default="")
    cpu_modelname = models.CharField(max_length=50, default="")
    cpu_model = models.CharField(max_length=50, default="")

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.os_system)


class MemInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)   # 使用插入数据时的当前时间作为数据的采集时间，不用去想插入的数据的格式问题。
    mem_used = models.CharField(max_length=50, default="")
    mem_free = models.CharField(max_length=50, default="")
    mem_total = models.CharField(max_length=50, default="")
    mem_shared = models.CharField(max_length=50, default="")
    mem_buff = models.CharField(max_length=50, default="")
    mem_available = models.CharField(max_length=50, default="")
    swap_total = models.CharField(max_length=50, default="")
    swap_used = models.CharField(max_length=50, default="")
    swap_free = models.CharField(max_length=50, default="")

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.mem_used)

class LoginFailed(models.Model):

    date = models.DateTimeField(default=timezone.now)
    fail_name = models.CharField(max_length=50, default="")
    fail_ip = models.CharField(max_length=50, default="")

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.fail_ip)

class CPUInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)
    cpu_user_precent = models.CharField(max_length=10, default="")
    cpu_sys_precent = models.CharField(max_length=20, default="")
    cpu_load_averages1 = models.CharField(max_length=20, default="")
    cpu_load_averages5 = models.CharField(max_length=20, default="")
    cpu_load_averages15 = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.cpu_user_precent)


class DiskInfo(models.Model):
    date = models.DateTimeField(default=timezone.now)
    mount_point = models.CharField(max_length=30, default="")
    disk_type = models.CharField(max_length=20, default="")
    disk_total = models.CharField(max_length=20, default="")
    disk_used = models.CharField(max_length=20, default="")
    disk_available = models.CharField(max_length=20, default="")
    used_percent = models.CharField(max_length=20, default="")

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.mount_point)
