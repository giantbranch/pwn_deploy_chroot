#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 14:01:13
# @Author  : giantbranch (giantbranch@gmail.com)
# @Link    : http://www.giantbranch.cn/
# @tags : 

# Whether to replace /bin/sh
REPLACE_BINSH = False

FLAG_BAK_FILENAME = "flags.txt"
PORT_INFO_FILENAME = "ports.txt"
PWN_BIN_PATH = "./bin"
XINETD_CONF_FILENAME = "pwn.xinetd"
PORT_LISTEN_START_FROM = 10000

XINETD = '''service ctf
{
    disable = no
    socket_type = stream
    protocol    = tcp
    wait        = no
    user        = root
    type        = UNLISTED
    port        = %d
    bind        = 0.0.0.0
    server      = /usr/sbin/chroot   
    server_args = --userspec=%s /home/%s ./%s
    # safety options
    per_source  = 10 # the maximum instances of this service per source IP address
    rlimit_cpu  = 20 # the maximum number of CPU seconds that the service may use
    rlimit_as  = 100M # the Address Space resource limit for the service
    #access_times = 2:00-9:00 12:00-24:00
}

'''

DOCKERFILE = '''FROM ubuntu:16.04

RUN sed -i 's/archive.ubuntu.com/asia-east1.gce.archive.ubuntu.com/g' /etc/apt/sources.list && apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*
#apt update && apt-get install -y lib32z1 xinetd && rm -rf /var/lib/apt/lists/ && rm -rf /root/.cache && apt-get autoclean && rm -rf /tmp/* /var/lib/apt/* /var/cache/* /var/log/*

COPY ./'''+ XINETD_CONF_FILENAME +''' /etc/xinetd.d/pwn

COPY ./service.sh /service.sh

RUN chmod +x /service.sh

# useradd and put flag
%s

# copy bin
%s

# chown & chmod
%s

# copy lib,/bin 
%s

CMD ["/service.sh"]
'''

DOCKERCOMPOSE = '''version: '2'
services:
 pwn_deploy_chroot:
   image: pwn_deploy_chroot:latest
   build: .
   container_name: pwn_deploy_chroot
   ports:
    %s
'''

