import json
import time
from datetime import datetime, timedelta

from django.shortcuts import render
from api.models import *


# Create your views here.
def index(request):
    # 因为这里我是要做单机的，所以这个我只取最后的数据
    result = MechineInfo.objects.last()

    # 获取当前的时间，用于获取数据时的时间范围用，设定的开始时间和结束时间为当前时间的24小时内
    now_time = datetime.now()

    # start_date = now_time - timedelta(hours=23, minutes=59, seconds=59)
    start_date = now_time - timedelta(minutes=29, seconds=59)
    end_date = now_time
    # 这里获取的是内存的信息，使用的是时间范围。
    memory_data = MemInfo.objects.filter(date__range=(start_date, end_date))

    # disk_data = DiskInfo.objects.filter(mount_point="/boot").order_by('-date').first()
    # 获取挂载点信息，并去重，用于下面查询各个挂载点自己的信息，
    disk_list = DiskInfo.objects.values('mount_point').distinct()

    # 磁盘信息插入为一个list。方便在页面用for循环来获取。首页显示的数据，去最新的时间（-date，时间倒序）的第一条即可。
    disk_data = []
    for item in disk_list:
        m_point = item['mount_point']
        disk_data.append(DiskInfo.objects.filter(mount_point=m_point).order_by('-date').first())
        # print(m_point)


    # 这里获取的是内存的信息，使用的是时间范围。
    cpu_data = CPUInfo.objects.filter(date__range=(start_date, end_date))
    # print(cpu_data)

    # print(disk_data)
    # for item in disk_data:
    #     print(item)
    context = {"result": result, "memory_data": memory_data, "disk_list": disk_list, "disk_data": disk_data, "cpu_data": cpu_data, }

    return render(request, "index.html", context)


def charts(request):

    context = {}
    return render(request, "charts.html", context)