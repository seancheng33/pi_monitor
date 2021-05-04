'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/8
@Program      : 利用os模块，使用系统本身的shell命令，采集各种数据。
'''
import datetime
import os
import json
import platform
import socket
import uuid
import re
import redis

# 获取系统的信息内容。
def getSyetemInfo():
    # 使用python自己的模块来获取系统的信息，比如操作系统的名称、节点名（hostname）、版本号、等等
    # 这个函数获取的结果，基本和在linux系统下用uname -a获取的结果一致。但是这个函数同样在windows下同样可以取值。
    info = platform.uname()
    system = info[0]
    node = info[1]
    release = info[2]
    version = info[3]
    machine = info[4]

    # 通过socket模块获取hostname和ip地址。但是可能存在ip地址非内网地址的情况
    hostname = socket.gethostname()
    # host_ip = socket.gethostbyname(hostname)
    host_ip = os.popen("ip a|grep eth0|grep inet|awk '{print $2}'").readline().replace('\n', '')
    # 获取mac地址，这个办法在虚拟机的ubuntu中是出现有误，但是在其他真机的测试中暂时没有发现有误。
    mac = uuid.uuid1().hex
    # 最后12位就是mac的内容，将其取出，然后全部小写改为大写。
    mac = mac[-12:].upper()
    # 将数据拼接成两位然后冒号隔开的一般常用的mac地址的形式。
    mac_address = re.findall(r".{2}", mac)
    mac_address = ':'.join(mac_address)

    # 这个系统运行时间没有办法用内置的模块获取，只能自己用命令获取
    uptime = os.popen(
        "uptime|awk -F ',' '{print $1}'|awk '{print $3}'").readline().replace('\n', '')

    # 获取cpu的型号信息，这三项不要用readlines拿一个列表，只取第一个值就可以了
    cpu_num = os.popen("grep 'processor' /proc/cpuinfo|wc -l").readline().replace('\n', '')
    cpu_modelname = os.popen(
        "grep 'model name' /proc/cpuinfo|awk -F ': ' '{print $2}'").readline().replace('\n', '')
    cpu_model = os.popen(
        "grep 'model' /proc/cpuinfo|awk -F ': ' '{print $2}'").readline().replace('\n', '')

    sysinfo = {"os_system": system, "os_node": node, "os_release": release, "os_version": version, "os_machine": machine,
               "hostname": hostname, "host_ip": host_ip, "mac_address": mac_address,
               "uptime": uptime, "cpu_num": cpu_num, "cpu_modelname": cpu_modelname, "cpu_model": cpu_model,}

    return sysinfo


# 获取内存的信息，其中awk命令使用了或判断，防止某些系统free出来的结果是中文的
def getMemoryInfo():
    # 获取物理内存的信息
    mem_total = os.popen("free -m|awk '/Mem:/||/内存：/ {print $2}'").readline()
    mem_used = os.popen("free -m|awk '/Mem:/||/内存：/  {print $3}'").readline()
    mem_free = os.popen("free -m|awk '/Mem:/||/内存：/  {print $4}'").readline()
    mem_shared = os.popen("free -m|awk '/Mem:/||/内存：/  {print $5}'").readline()
    mem_buff = os.popen("free -m|awk '/Mem:/ ||/内存：/ {print $6}'").readline()
    mem_available = os.popen(
        "free -m|awk '/Mem:/||/内存：/  {print $7}'").readline()
    # 获取交换空间的信息
    swap_total = os.popen(
        "free -m|awk '/Swap:/||/交换：/  {print $2}'").readline()
    swap_used = os.popen("free -m|awk '/Swap:/||/交换：/  {print $3}'").readline()
    swap_free = os.popen("free -m|awk '/Swap:/||/交换：/  {print $4}'").readline()
    # 将获取到的内容拼接成一条到时需要传给接口的json数据。
    meminfo = {"mem_total": mem_total.replace('\n', '') + "M", "mem_used": mem_used.replace('\n', '') + "M",
               "mem_free": mem_free.replace('\n', '') + "M", "mem_shared": mem_shared.replace('\n', '') + "M",
               "mem_buff": mem_buff.replace('\n', '') + "M", "mem_available": mem_available.replace('\n', '') + "M",
               "swap_total": swap_total.replace('\n', '') + "M", "swap_used": swap_used.replace('\n', '') + "M",
               "swap_free": swap_free.replace('\n', '') + "M", }

    return meminfo

# 获取CPU的用户使用量百分比，系统使用量百分比，一分钟负载，五分钟负载，十五分钟负载
def getCPUInfo():
    # 这里的执行top命令要加一个-b的参数，否则的话，会有问题，报错“  top: failed tty get 错误”。导致cpu的内容无法获取并写入。
    '''
    通过其他程序或脚本在非交互式模式下调用top命令，经常会出现:
    top: failed tty get 错误
    解决办法：加个-b 选项即可
    '''
    cpu_user_precent = os.popen(
        "top -bn1|awk -F ' ' '/%Cpu/ {print $2}'").readline()
    cpu_sys_precent = os.popen(
        "top -bn1|awk -F ' ' '/%Cpu/ {print $4}'").readline()
    cpu_load_averages1 = os.popen(
        "uptime|awk -F 'load average:' '{print $2}'|awk -F ',' '{print $1}'").readline()
    cpu_load_averages5 = os.popen(
        "uptime|awk -F 'load average:' '{print $2}'|awk -F ',' '{print $2}'").readline()
    cpu_load_averages15 = os.popen(
        "uptime|awk -F 'load average:' '{print $2}'|awk -F ',' '{print $3}'").readline()

    cpuinfo = {"cpu_user_precent":cpu_user_precent.replace('\n', ''), "cpu_sys_precent":cpu_sys_precent.replace('\n', ''), "cpu_load_averages1":cpu_load_averages1.replace('\n', ''),
          "cpu_load_averages5":cpu_load_averages5.replace('\n', ''), "cpu_load_averages15":cpu_load_averages15.replace('\n', '')}

    return cpuinfo

# 获取磁盘的空间信息，由于服务器可能挂载多个数据盘，所以需要获取多个分区和挂载点的信息
def getDiskInfo():
    disk = os.popen(
        "df -Th|grep -v '/dev/loop'|awk '/^\/dev\// {print $0}'").readlines()
    all_disk_info = []
    for item in disk:
        disk_item = item.replace('\n', '').split(' ')
        while '' in disk_item:
            disk_item.remove('')
        diskinfo = {"mount_point": disk_item[6], "disk_type": disk_item[1], "disk_total": disk_item[2],
                    "disk_used": disk_item[3], "disk_available": disk_item[4], "used_percent": disk_item[5], }
        # print(diskinfo)
        all_disk_info.append(diskinfo)
    return all_disk_info


# 获取登录失败的数据信息
def getLastb():
    lastb = os.popen("lastb|grep -v btmp").readlines()
    all_lastb_info = []
    for item in lastb:
        n_item = item.replace('\n', '').split('   ')
#         print(n_item)
#        print(type(n_item))
        last_item ={}
        if len(n_item) == 4 :
            last_item['fail_name']=n_item[0]
            last_item['terminal']=n_item[1].replace(' ','')
            last_item['fail_ip']=n_item[2].replace(' ','')
            last_item['date']=n_item[3].lstrip()    # 2021年5月4日发现用切片[1:]存在问题，改为lstrip去掉左边的空格。
        elif len(n_item) == 3 :
            last_item['fail_name']=n_item[0].split(' ')[0]
            last_item['terminal']=n_item[0].split(' ')[1]
            last_item['fail_ip']=n_item[1].replace(' ','')
            last_item['date']=n_item[2].lstrip()    # 2021年5月4日发现用切片[1:]存在问题，改为lstrip去掉左边的空格。
        else:
            continue

        all_lastb_info.append(last_item)
    return all_lastb_info


# 与上面的有时间判断不同，这个会随着每次执行，获取到lastb中显示的数据，并且是存到redis里面，
# 数据的存储和检查速度比存在mysql里面的要快，且不是每个月获取一次的问题。
def getLastbNow():
    r_pool = redis.ConnectionPool(host='192.168.1.90', port=6379, db=1, password='test123456', decode_responses=True)
    r = redis.Redis(connection_pool=r_pool)

    lastb = os.popen("lastb|grep -v btmp").readlines()
    i = 0
    for item in lastb:
        n_item = item.replace('\n', '').split('   ')
        last_item = []
        if len(n_item) == 4:
            last_item.append(n_item[0])
            last_item.append(n_item[1].replace(' ', ''))
            last_item.append(n_item[2].replace(' ', ''))
            last_item.append(n_item[3].lstrip())
        elif len(n_item) == 3:
            last_item.append(n_item[0].split(' ')[0])
            last_item.append(n_item[0].split(' ')[1])
            last_item.append(n_item[1].replace(' ', ''))
            last_item.append(n_item[2].lstrip())
        else:
            continue
        # print(last_item)
        for item2 in last_item:
            r.lpush('failed' + str(i), item2)
        #print(r.lrange('failed' + str(i), 0, 3))
        i += 1



if __name__ == '__main__':

    # 获取系统的信息
    sysinfo = json.dumps(getSyetemInfo())
    # print(sysinfo)
    check_sys = os.popen('curl http://127.0.0.1:8000/api/mechineinfo/').readlines()
    # 这里有作一个判断，如果mac地址相同，就只是更新对应主键的数据，如果没有，就新添加数据。
    # print(sysinfo)
    if len(check_sys) > 0:
        for item in json.loads(check_sys[0]):
            # print(item)
            if item.get('mac_address') == eval(sysinfo)['mac_address']:
                # 获取系统信息数据的pk值，用于到时更新数据时使用。
                pk = item.get('pk')
                # print("1"+sysinfo)
                os.popen("curl -H 'content-type: application/json' -d '"+str(sysinfo)+"' -X put http://127.0.0.1:8000/api/mechineinfo/"+str(pk)+"/").readlines()
    else:
        # print("2"+sysinfo)
        os.popen("curl -H 'content-type: application/json' -d '"+str(sysinfo)+"' -X post http://127.0.0.1:8000/api/mechineinfo/").readlines()

    # 获取内存的信息
    meminfo = json.dumps(getMemoryInfo())
    # print(meminfo)
    os.popen("curl -H 'content-type: application/json' -d '"+str(meminfo)+"' -X post http://127.0.0.1:8000/api/meminfo/").readlines()

    # 获取磁盘的信息
    diskinfo = getDiskInfo()
    # print(diskinfo)
    # 因为磁盘信息传出来的是一个list，所以需要遍历数据，把每一个都拿出来。
    for item in diskinfo:
       # list里面的元素在函数中拼接的时候是字典，这里需要转成json的格式传给接口，不然接口会接收不到数据
       info = json.dumps(item)
       os.popen("curl -H 'content-type: application/json' -d '"+str(info)+"' -X post http://127.0.0.1:8000/api/diskinfo/").readlines()

    cpuinfo = json.dumps(getCPUInfo())
    # print(cpuinfo)
    os.popen("curl -H 'content-type: application/json' -d '"+str(cpuinfo)+"' -X post http://127.0.0.1:8000/api/cpuinfo/").readlines()


    # 获取登录失败的信息
    lastbinfo = getLastb()

    # 获取四个时间，用于写入登录失败的信息用的。
    # 首先直接获取一个明天的日期数，用今天的日期加1天，就是明天的日期了。
    tomorrow = datetime.date.today()+datetime.timedelta(days=1)
    # 下面的三个时间，一个是开始的时间范围，一个是结束的时间范围，一个是当前时间。
    s_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59:30', '%Y-%m-%d%H:%M:%S')
    e_time = datetime.datetime.strptime(str(datetime.datetime.now().date()) + '23:59:59', '%Y-%m-%d%H:%M:%S')
    now_time = datetime.datetime.now()

    # 两个判断，一个是判断明天的日期是不是等于1日，一个是当前的时间是否是在23点59分30秒到59秒之间。tomorrow后面点day就是只显示日期，就可以直接和数字1做比对了。
    # 因为脚本的运行时间是10秒一次，所以，30-59秒之间的话，是在40秒之后会运行一次。从而实现了只在每个月的最后一天的最后一次运行采集lastb的数据。
    if tomorrow.day == 1 and (s_time < now_time and now_time < e_time):
        for item in lastbinfo:
            info = json.dumps(item)
            os.popen("curl -H 'content-type: application/json' -d '" + str(info) + "' -X post http://127.0.0.1:8000/api/loginfailed/").readlines()

    # 获取实时登录失败的数据信息
    getLastbNow()