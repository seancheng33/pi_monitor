from datetime import datetime, timedelta

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from api.models import *
import redis
# 导入配置文件及初始化配置
import configparser
from pi_monitor import settings

path = settings.CONF_DIR
cf = configparser.ConfigParser()
cf.read(path)



# Create your views here.
@login_required(login_url='login.html')     # 后面的login_url指明了登录页面。如果没有指明，就是默认的account/login的路径
def index(request):
    print(request.method)
    # 因为这里我是要做单机的，所以这个我只取最后的数据
    result = MechineInfo.objects.last()

    # 获取当前的时间，用于获取数据时的时间范围用，设定的开始时间和结束时间为当前时间的10分钟内
    now_time = datetime.now()

    # start_date = now_time - timedelta(hours=23, minutes=59, seconds=59)
    start_date = now_time - timedelta(minutes=9, seconds=59)
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

    # 这里获取的是内存的信息，使用的是时间范围。
    cpu_data = CPUInfo.objects.filter(date__range=(start_date, end_date))

    context = {"result": result, "memory_data": memory_data, "disk_list": disk_list, "disk_data": disk_data, "cpu_data": cpu_data, }

    return render(request, "index.html", context)

@login_required(login_url='login.html')
def cpu(request):
    # 获取当前的时间，用于获取数据时的时间范围用，设定的开始时间和结束时间为当前时间的24小时内
    now_time = datetime.now()

    start_date = now_time - timedelta(minutes=29, seconds=59)
    start_date2 = now_time - timedelta(hours=1, minutes=59, seconds=59)
    end_date = now_time

    # 这里获取的是内存的信息，使用的是时间范围。
    cpu_data = CPUInfo.objects.filter(date__range=(start_date, end_date))
    all_data = CPUInfo.objects.filter(date__range=(start_date2, end_date))



    context = {"cpu_data":cpu_data,"all_data":all_data[:640]}
    return render(request, "cpu.html", context)

@login_required(login_url='login.html')
def memory(request):

    # 获取当前的时间，用于获取数据时的时间范围用，设定的开始时间和结束时间为当前时间的24小时内
    now_time = datetime.now()

    start_date = now_time - timedelta(minutes=29, seconds=59)
    start_date2 = now_time - timedelta(hours=1, minutes=59, seconds=59)
    end_date = now_time

    # 这里获取的是内存的信息，使用的是时间范围。
    mem_data = MemInfo.objects.filter(date__range=(start_date, end_date))
    mem_all = MemInfo.objects.filter(date__range=(start_date2, end_date))

    context = {"mem_data": mem_data, "mem_all": mem_all}
    return render(request, "memory.html", context)

@login_required(login_url='login.html')
def disk(request):

    # 获取挂载点信息，并去重，用于下面查询各个挂载点自己的信息，
    disk_list = DiskInfo.objects.values('mount_point').distinct()

    # 磁盘信息插入为一个list。方便在页面用for循环来获取。首页显示的数据，去最新的时间（-date，时间倒序）的第一条即可。
    disk_data = []
    for item in disk_list:
        m_point = item['mount_point']
        disk_data.append(DiskInfo.objects.filter(mount_point=m_point).order_by('-date').first())

    context = {'disk_list': disk_list, 'disk_data': disk_data}
    return render(request, "disk.html", context)

@login_required(login_url='login.html')
def lastb(request):
    # 获取当前的总登陆失败的数据总量
    failed_count = LoginFailed.objects.count()

    all_fail_name = LoginFailed.objects.values('fail_name').distinct()
    total_name_num = LoginFailed.objects.values('fail_name').distinct().count()
    # print(all_fail_name)
    all_fail_ip = LoginFailed.objects.values('fail_ip').distinct()
    total_ip_num = LoginFailed.objects.values('fail_ip').distinct().count()
    # print(all_fail_ip)



    # 连接redis库，获取redis中的一些高频信息
    pool = redis.ConnectionPool(host=cf.get('redis', 'redis_host'), port=cf.get('redis', 'redis_port'),
                                db=cf.get('redis', 'redis_db'), password=cf.get('redis', 'redis_password'),
                                decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    # 获取该库的数据总数
    db_num = r.dbsize()
    lastb_list = []
    for i in range(0, db_num):
        tmp = {}
        item = r.lrange('failed' + str(i), 0, 3)
        tmp['time'] = item[0]
        tmp['ip'] = item[1]
        tmp['terminal'] = item[2]
        tmp['name'] = item[3]
        lastb_list.append(tmp)
    # print(lastb_list)

    context = {'count': failed_count, 'total_ip_num': total_ip_num, 'total_name_num': total_name_num, 'db_num': db_num,
               'lastb_list': lastb_list}
    return render(request, "lastb.html", context)


@login_required(login_url='login.html')
def config(request):

    context = {}
    return render(request, "config.html", context)

@login_required(login_url='login.html')
def about(request):

    context = {}
    return render(request, "about.html", context)

# 登录系统的验证
def login(request):
    # 超管用户名是用python manage.py createsuperuser创建的（admin/admin123）
    # print(request.method)

    # 判断是不是post过来的数据，是的话，就是提交登陆数据的操作
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        # 利用知道的认证功能，把页面post过来的用户名和密码，利用该功能验证并返回user对象，
        # 这个user对象在下面的登陆中需要用到。
        user = auth.authenticate(username=u,password=p)
        print(u,p)
        # 如果user对象有返回，就是用户是存在的，可以调用login函数登陆，如果没有，就是验证失败，返回错误提示信息。
        if user is not None:
            auth.login(request,user)
            return HttpResponseRedirect(reverse('index'))
        else:
            context = {"error": "用户名或密码错误，请核对后重试或联系系统管理员。"}
            return render(request, "login.html", context)

    context = {"error":"请登陆系统已正常使用各种功能。"}
    return render(request, "login.html", context)


# 登出系统，利用logout函数清理掉登录信息。
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('login'))

