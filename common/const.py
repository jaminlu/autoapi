#!/usr/bin/env python
# -*- coding: utf-8 -*-


debug = False
log_dir = '/var/log/'                                           #debug模式运行
UFSM_LOG_MAX_SIZE = 100 * 1024 * 1024                           # 默认100M
UFSM_LOG_MAX_FILE = 5                                           # 保留日志文件个数
UFS_LOG_LEVEL = 30                                              #日志的等级default
#  30; FATAL=50,ERROR=40,WARNING=30,INFO=20,DEBUG=10,NOTSET=0
http_port = 8888                                                #后台服务端口
http_ip = '127.0.0.1'                                           #后台服务监听ip
limit_time = 100                                                 #限制频率单位豪秒
command_time_out = 30                                            #后端执行超时时间
secert = ''         #协商密钥
redis_host = ''                                       #redis ip
redis_port =                                                #redis 端口
redis_pass = ''                                     #redis 密码
ssize = 1024 * 1024 *50                                         #文件大小
