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
    info = platform.uname()
    system = info[0]
    node = info[1]
    release = info[2]
    version = info[3]
    machine = info[4]
    processor = info[5]
    # hostname
    hostname = socket.gethostname()
    host_ip = socket.gethostbyname(hostname)
    # 获取mac地址
    mac = uuid.uuid1().hex
    mac = mac[-12:].upper()

    mac_address = re.findall(r".{2}",mac)
    mac_address = ':'.join(mac_address)

    # 这个系统运行时间没有办法用内置的模块获取，只能自己用命令获取
    uptime = os.popen("uptime|awk -F ',' '{print $1}'|awk '{print $3}'").readline().replace('\n','')

    sysinfo = {"os_system":system,"os_node":node,"os_release":release,"os_version":version,"os_machine":machine,"os_processor":processor,"hostname":hostname,"host_ip":host_ip,"mac_address":mac_address,"uptime":uptime,}

    print(sysinfo)


# 获取内存的信息，其中awk命令使用了或判断，防止某些系统free出来的结果是中文的
def getMemoryInfo():
    # 获取物理内存的信息
    mem_total = os.popen("free -m|awk '/Mem:/||/内存：/ {print $2}'").readline()
    mem_used = os.popen("free -m|awk '/Mem:/||/内存：/  {print $3}'").readline()
    mem_free = os.popen("free -m|awk '/Mem:/||/内存：/  {print $4}'").readline()
    mem_shared = os.popen("free -m|awk '/Mem:/||/内存：/  {print $5}'").readline()
    mem_buff = os.popen("free -m|awk '/Mem:/ ||/内存：/ {print $6}'").readline()
    mem_available = os.popen("free -m|awk '/Mem:/||/内存：/  {print $7}'").readline()
    # 获取交换空间的信息
    swap_total = os.popen("free -m|awk '/Swap:/||/交换：/  {print $2}'").readline()
    swap_used = os.popen("free -m|awk '/Swap:/||/交换：/  {print $3}'").readline()
    swap_free = os.popen("free -m|awk '/Swap:/||/交换：/  {print $4}'").readline()
    # 将获取到的内容拼接成一条到时需要传给接口的json数据。
    meminfo = {"mem_total": mem_total.replace('\n', '') + "M", "mem_used": mem_used.replace('\n', '') + "M",
               "mem_free": mem_free.replace('\n', '') + "M", "mem_shared": mem_shared.replace('\n', '') + "M",
               "mem_buff": mem_buff.replace('\n', '') + "M", "mem_available": mem_available.replace('\n', '') + "M",
               "swap_total": swap_total.replace('\n', '') + "M", "swap_used": swap_used.replace('\n', '') + "M",
               "swap_free": swap_free.replace('\n', '') + "M", }

    return meminfo


def getCPUInfo():
    pass

# 获取磁盘的空间信息，由于服务器可能挂载多个数据盘，所以需要获取多个分区和挂载点的信息
def getDiskInfo():
    disk = os.popen("df -Th|grep -v '/dev/loop'|awk '/^\/dev\// {print $0}'").readlines()
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

    getSyetemInfo()

    # 获取内存的信息
    # meminfo = json.dumps(getMemoryInfo())
    # print(meminfo)
    # os.popen("curl -H 'content-type: application/json' -d '"+str(meminfo)+"' -X post http://192.168.1.23:8000/api/meminfo/").readlines()


    # 获取磁盘的信息
    # diskinfo = getDiskInfo()
    # 因为磁盘信息传出来的是一个list，所以需要遍历数据，把每一个都拿出来。
    # for item in diskinfo:
    #    # list里面的元素在函数中拼接的时候是字典，这里需要转成json的格式传给接口，不然接口会接收不到数据
    #    info = json.dumps(item)
    #    os.popen("curl -H 'content-type: application/json' -d '"+str(info)+"' -X post http://192.168.1.23:8000/api/diskinfo/").readlines()

