## 服务器运行性能监控

### 背景
希望监控自己的树莓派的日常的运行情况，准备使用django的drf弄一个rest的接口，
用来收集和存储各硬件的运行指标，拟计划先收集内存、cpu、硬盘、网络的使用情况。
同时再将这些数据用图表统计出来。
- 服务器端的后台使用rest，然后客户端使用agent向后台的接口发送数据。agent使用python编写，只使用了本身的库。不需要另外添加额外的外部库。
- 数据存储在数据库中，目前是使用mongo或者mysql来存储。但是比较倾向于使用mongodb
- django站点的一个app用来查询后展示数据的各种图表。
- 添加一个查看lastb的数据采集
- 后续会考虑将整体集成为一个docker的镜像这类问题。
- 

### 开发所使用的环境
开发的语言python
使用到的插件

Package               |Version
--------------------- |-------
asgiref               |3.3.1
Django                |3.1.5
django-rest-framework |0.1.0
djangorestframework   |3.12.2
mongoengine           |0.22.1
pip                   |20.3.3
pytz                  |2020.5
setuptools            |51.1.1
sqlparse              |0.4.1


### 更新内容
2021年1月7日：创建项目，并开始初始化项目的配置。并上传。<br />
2021年1月8日：修改agent脚本为python脚本，不用shell脚本。脚本的磁盘信息获取功能和内存信息获取基本测试完成。<br />
2021年1月11日：添加系统信息的手机，调整和完善系统信息表的model。<br />
2021年1月12日：基本信息收集的agent脚本基本完成。开始添加数据展示的页面<br />
2021年1月13日：完善数据展示页面，并添加了django-crontab的定时任务的准备。<br />
2021年1月29日：针对树莓派的特殊性，删除了agent里面的系统信息的processor值。<br />
2021年1月30日：添加一个启动django服务的shell脚本。<br />
2021年04月18日： agent的小错误修复。并且添加两个shell脚本，用于后台运行django和agent。<br />
调整显示规则，由原来的24小时的数据调整为显示30分钟的数据<br />
2021年4月19日：开始美化数据展示的页面。<br />
2021年4月20日：添加展示的页面及确定了页面的数量。<br />
2021年4月23日：构建CPU、内存使用详情的页面。修改首页的数据图表为显示10分钟的内容，
详细页为30分钟及默认显示640条数据。<br />
2021年4月25日：完成了首页的初稿,修改agent的机器获取，并添加关于lastb的获取内容。<br />
2021年4月26日：agent添加获取登录失败的信息的功能，并且添加了获取的时间范围。<br />
2021年4月27日：添加一个目录，存放本系统的脑图及一些其他的文件。<br />
2021年5月3日：添加登陆失败页面及逻辑<br />


### 目前出现的情况及待处理的问题汇总
- 连接mongodb报错，原因未知，目前暂时使用的是mysql（关于后续修改为mongodb的问题暂时不考虑）
- 接口大部分已经完成，剩下部分细微的微调。
- 需要优（美）化后台的查看界面，同时考虑添加用户登录才能访问数据。
- 使用多种表格显示详细的信息
- 考虑是否需要删除某些时间范围之外的内容。优化数据库。
- 一个需要思考的问题，是每10秒过去一次数据，拿比较准确的数据呢？还是每分钟获取一次数据，减低使用的资源及数据量。