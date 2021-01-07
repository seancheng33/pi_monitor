from django.db import models

# Create your models here.
from django.utils import timezone


class MemInfoModel(models.Model):
    date = models.DateTimeField(default=timezone.now)   # 使用插入数据时的当前时间作为数据的采集时间，不用去想插入的数据的格式问题。
    mem_used = models.CharField(max_length=50)
    mem_free = models.CharField(max_length=50)
    mem_total = models.CharField(max_length=50)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.mem_used)

class LoginFailedModel(models.Model):
    date = models.DateField()
    fail_name = models.CharField(max_length=50)
    fail_ip = models.CharField(max_length=50)

    def __unicode__(self):
        return '%d:%s' % (self.pk, self.fail_ip)