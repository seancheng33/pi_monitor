## 服务器运行性能监控

### 背景
希望监控自己的树莓派的日常的运行情况，准备使用django的drf弄一个rest的接口，
用来收集和存储各硬件的运行指标，拟计划先收集内存、cpu、硬盘、网络的使用情况。
同时再将这些数据用图表统计出来。
- 服务器端的后台使用rest，然后客户端使用agent向后台的接口发送数据。agent使用python编写，只使用了本身的库。不需要另外添加额外的外部库。
- 数据存储在数据库中，目前是使用mongo或者mysql来存储。但是比较倾向于使用mongodb
- django站点的一个app用来查询后展示数据的各种图标，估计一个页面即可。
- 添加一个查看lastb的数据采集
- 后续会考虑将整体集成为一个docker的镜像这类问题。
- 

### 开发所使用的环境
开发的语言python3.6.2
使用到的插件

Package               |Version
--------------------- |-------
asgiref               |3.3.1
Django                |3.1.5
django-rest-framework |0.1.0
djangorestframework   |3.12.2
mongoengine           |0.22.1
pip                   |20.3.3
pymongo               |3.11.2
pytz                  |2020.5
setuptools            |51.1.1
sqlparse              |0.4.1

### 目前出现的情况
- 连接mongodb报错，原因未知，目前暂时使用的是mysql
- 接口大部分已经完成，剩下部分细微的微调。
- 

### 更新内容
2021年1月7日：创建项目，并开始初始化项目的配置。并上传。<br />
2021年1月8日：修改agent脚本为python脚本，不用shell脚本。脚本的磁盘信息获取功能和内存信息获取基本测试完成。<br />
2021年1月11日：添加系统信息的手机，调整和完善系统信息表的model。<br />
2021年1月12日：基本信息收集的agent脚本基本完成。开始添加数据展示的页面<br />
2021年1月13日：完善数据展示页面，并添加了django-crontab的定时任务的准备。