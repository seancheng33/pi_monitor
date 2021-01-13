import json
import time
from datetime import datetime,timedelta

from django.shortcuts import render
from api.models import *


# Create your views here.
def index(request):
    # 因为这里我是要做单机的，所以这个我只取最后的数据
    result = MechineInfo.objects.last()

    # 获取当前的时间，用于获取数据时的时间范围用，设定的开始时间和结束时间为当前时间的24小时内
    now_time = datetime.now()

    start_date = now_time - timedelta(hours=23, minutes=59, seconds=59)
    end_date = now_time
    # 这里获取的是内存的信息，使用的是时间范围。
    memory_data = MemInfo.objects.filter(date__range=(start_date, end_date))



    # print(memory_data)
    context = {"result": result, "memory_data": memory_data,}
    return render(request, "index.html", context)