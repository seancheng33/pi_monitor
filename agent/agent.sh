#!/usr/bin/env bash

while true
do
free=$(free|awk '/Mem/ {print $3}')
used=$(free|awk '/Mem/ {print $4}')
total=$(free|awk '/Mem/ {print $2}')


curl -H 'content-type: application/json' -d '{"mem_free": "'${free}'","mem_used": "'${used}'","mem_total":"'${total}'"}' -X post http://127.0.0.1:8000/api/meminfo/
sleep 10
done

