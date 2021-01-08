'''
@Author       : sean cheng
@Email        : aya234@163.com
@CreateTime   : 2021/1/8
@Program      : 利用os模块，使用系统本身的shell命令，采集各种数据。
'''
import os


def getSyetemInfo():
    info = os.popen('cat /etc/issue').readline()
    print(info)

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


def getDiskInfo():
    disk = os.popen("df -Th|grep -v '/dev/loop'|awk '/^\/dev\// {print $0}'").readlines()
    all_disk_info = []
    for item in disk:
        disk_item = item.replace('\n', '').split(' ')
        while '' in disk_item:
            disk_item.remove('')
        diskinfo = {"mount_point": disk_item[6], "disk_type": disk_item[1], "disk_total": disk_item[2],
                    "disk_used": disk_item[3], "disk_available": disk_item[4], "disk_percent": disk_item[5], }
        # print(diskinfo)
        all_disk_info.append(diskinfo)
    return all_disk_info


if __name__ == '__main__':
    print(getMemoryInfo())
    print(getDiskInfo())
