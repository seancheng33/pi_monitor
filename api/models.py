from django.db import models

# Create your models here.
from django.utils import timezone


class MemInfoModel(models.Model):
    date = models.DateTimeField(default=timezone.now)
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