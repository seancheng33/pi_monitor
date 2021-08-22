#!/bin/bash

# 开始服务的函数
startapp(){
echo "-----启动django网站服务-----"
# 直接指定虚拟环境的python来执行启动服务
nohup venv/bin/python manage.py runserver 0.0.0.0:8000 >> webserver.log 2>&1 & 
echo "启动服务完成"
}
# 停止服务的函数
stopapp(){
echo "-----停止django网站服务-----"
# 先查找有没有进程，如果有就把进程杀了
if ps -ef|grep runserver|grep -qv grep
then
	`ps -ef|grep runserver|grep -v grep|awk '{print $2}'|xargs kill`
	echo "停止服务完成"
else
	# 如果没有，就不用啥进程
	echo "没有进程，无需停止进程。"
fi
}


# 如果执行该脚本后面有跟参数，根据后面的传输来执行
case $1 in
	# 启动服务
	start) 
		startapp ;;
	# 停止服务
	stop) 
		stopapp ;;
	# 先停止再启动服务，就是重启
	restart) 
		stopapp
		sleep 5
		startapp ;;
	# 如果不是上面的三种参数，则执行重启的操作
	*) 
		stopapp
		sleep 5
		startapp ;;
esac
