#!/usr/bin/env bash
'''
初始化项目以及数据库的离线脚本。
'''

./venv/bin/pip3 install -r requirement.txt
./venv/bin/python3 manage.py makemigrations
./venv/bin/python3 manage.py migrate

./venv/bin/python3 manage.py createsuperuser
user="admin"
passwd="Admin1234"
expect <<EOF
      set timeout 10
      expect {
        "leave blank to use '$(USER)'" { send "$user\n"}
        "Password" { send "$passwd\n" }
        "Password (again)" { send "$passwd\n"}
      }
EOF

