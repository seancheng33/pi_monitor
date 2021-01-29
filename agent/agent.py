'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/8
@Program      : 利用os模块，使用系统本身的shell命令，采集各种数据。
'''
import os
import json
import platform
import socket
import uuid
import re

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
    host_ip = socket.gethostbyname(hostname)
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
    cpu_num = os.popen("grep 'processor' /proc/cpuinfo|wc -l").readline()
    cpu_modelname = os.popen(
        "grep 'model name' /proc/cpuinfo|awk -F ': ' '{print $2}'").readline()
    cpu_model = os.popen(
        "grep 'model' /proc/cpuinfo|awk -F ': ' '{print $2}'").readline()

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
    cpu_user_precent = os.popen(
        "top -n1|awk -F ' ' '/%Cpu/ {print $2}'").readline()
    cpu_sys_precent = os.popen(
        "top -n1|awk -F ' ' '/%Cpu/ {print $4}'").readline()
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


if __name__ == '__main__':

    # 获取系统的信息
    sysinfo = json.dumps(getSyetemInfo())
    # print(sysinfo)
    check_sys = os.popen('curl http://192.168.1.23:8000/api/mechineinfo/').readlines()
    # 这里有作一个判断，如果mac地址相同，就只是更新对应主键的数据，如果没有，就新添加数据。
    if len(check_sys):
        for item in json.loads(check_sys[0]):
            # print(item)
            if item.get('mac_address') == eval(sysinfo)['mac_address']:
                # 获取系统信息数据的pk值，用于到时更新数据时使用。
                pk = item.get('pk')
                # print(sysinfo)
                os.popen("curl -H 'content-type: application/json' -d '"+str(sysinfo)+"' -X put http://192.168.1.23:8000/api/mechineinfo/"+str(pk)+"/").readlines()
    else:
        os.popen("curl -H 'content-type: application/json' -d '"+str(sysinfo)+"' -X post http://192.168.1.23:8000/api/mechineinfo/").readlines()

    # 获取内存的信息
    meminfo = json.dumps(getMemoryInfo())
    # print(meminfo)
    os.popen("curl -H 'content-type: application/json' -d '"+str(meminfo)+"' -X post http://192.168.1.23:8000/api/meminfo/").readlines()

    # 获取磁盘的信息
    diskinfo = getDiskInfo()
    # 因为磁盘信息传出来的是一个list，所以需要遍历数据，把每一个都拿出来。
    for item in diskinfo:
       # list里面的元素在函数中拼接的时候是字典，这里需要转成json的格式传给接口，不然接口会接收不到数据
       info = json.dumps(item)
       os.popen("curl -H 'content-type: application/json' -d '"+str(info)+"' -X post http://192.168.1.23:8000/api/diskinfo/").readlines()

    cpuinfo = json.dumps(getCPUInfo())
    # print(cpuinfo)
    os.popen("curl -H 'content-type: application/json' -d '"+str(cpuinfo)+"' -X post http://192.168.1.23:8000/api/cpuinfo/").readlines()
