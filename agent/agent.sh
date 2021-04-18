#!/usr/bin/env bash
#
# 使用以下的命令在后台挂起运行agent来获取系统的信息
# nohup sh agent.sh >> agent.log 2>&1 &
# 里面的sleep 10是指休眠十秒。
# 也可以不使用这个脚本挂起运行，但是系统的crontab只能精细到一分钟。
#


while true
do
python3 agent.py
sleep 10
done

