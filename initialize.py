#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 14:32:32
# @Author  : giantbranch (giantbranch@gmail.com)
# @Link    : http://www.giantbranch.cn/
# @tags : 

from config import *
import os
import uuid

def getFileList():
    filelist = []
    for filename in os.listdir(PWN_BIN_PATH):
        filelist.append(filename)
    filelist.sort()
    return filelist

def generateFlags(filelist):
    tmp = ""
    flags = []
    if os.path.exists(FLAG_BAK_FILENAME):
        os.remove(FLAG_BAK_FILENAME)
    with open(FLAG_BAK_FILENAME, 'a') as f:
        for filename in filelist:
            tmp = "flag{" + str(uuid.uuid4()) + "}"
            f.write(filename + ": " + tmp + "\n")
            flags.append(tmp)
    return flags

def generateXinetd(filelist):
    port = PORT_LISTEN_START_FROM
    conf = ""
    uid = 1000
    for filename in filelist:
        conf += XINETD % (port, str(uid) + ":" + str(uid), filename, filename)
        port = port + 1
        uid = uid + 1
    with open(XINETD_CONF_FILENAME, 'w') as f:
            f.write(conf)

def generateDockerfile(filelist, flags):
    conf = ""
    # useradd and put flag
    runcmd = "RUN "
    
    for filename in filelist:
        runcmd += "useradd -m " + filename + " && "
   
    for x in xrange(0, len(filelist)):
        if x == len(filelist) - 1:
            runcmd += "echo '" + flags[x] + "' > /home/" + filelist[x] + "/flag.txt" 
        else:
            runcmd += "echo '" + flags[x] + "' > /home/" + filelist[x] + "/flag.txt" + " && "
    # print runcmd 

    # copy bin
    copybin = ""
    for filename in filelist:
        copybin += "COPY " + PWN_BIN_PATH + "/" + filename  + " /home/" + filename + "/" + filename + "\n"
        copybin += "COPY ./catflag" + " /home/" + filename + "/bin/sh\n"    
    # print copybin

    # chown & chmod
    chown_chmod = "RUN "
    for x in xrange(0, len(filelist)):
        chown_chmod += "chown -R root:" + filelist[x] + " /home/" + filelist[x] + " && "
        chown_chmod += "chmod -R 750 /home/" + filelist[x] + " && "
        if x == len(filelist) - 1:
            chown_chmod += "chmod 740 /home/" + filelist[x] + "/flag.txt"
        else:
            chown_chmod += "chmod 740 /home/" + filelist[x] + "/flag.txt" + " && "
    # print chown_chmod

    # copy lib,/bin 
    # dev = '''mkdir /home/%s/dev && mknod /home/%s/dev/null c 1 3 && mknod /home/%s/dev/zero c 1 5 && mknod /home/%s/dev/random c 1 8 && mknod /home/%s/dev/urandom c 1 9 && chmod 666 /home/%s/dev/* && '''
    dev = '''mkdir /home/%s/dev && mknod /home/%s/dev/null c 1 3 && mknod /home/%s/dev/zero c 1 5 && mknod /home/%s/dev/random c 1 8 && mknod /home/%s/dev/urandom c 1 9 && chmod 666 /home/%s/dev/* '''
    # ness_bin = '''mkdir /home/%s/bin && cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
    # ness_bin = '''cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
    copy_lib_bin_dev = "RUN "
    for x in xrange(0, len(filelist)):
        copy_lib_bin_dev += "cp -R /lib* /home/" + filelist[x]  + " && "        
        copy_lib_bin_dev += dev % (filelist[x], filelist[x], filelist[x], filelist[x], filelist[x], filelist[x])
        if x == len(filelist) - 1:
            # copy_lib_bin_dev += ness_bin % (filelist[x], filelist[x], filelist[x])
            pass                
        else:    
            # copy_lib_bin_dev += ness_bin % (filelist[x], filelist[x], filelist[x]) + " && "
            copy_lib_bin_dev += " && "

    # print copy_lib_bin_dev

    conf = DOCKERFILE % (runcmd, copybin, chown_chmod, copy_lib_bin_dev)

    with open("Dockerfile", 'w') as f:
        f.write(conf)

def generateDockerCompose(length):
    conf = ""
    ports = ""
    port = PORT_LISTEN_START_FROM
    for x in xrange(0,length):
        ports += "- " + str(port) + ":" + str(port) + "\n    "
        port = port + 1

    conf = DOCKERCOMPOSE % ports
    # print conf
    with open("docker-compose.yml", 'w') as f:
        f.write(conf)

def generateBinPort(filelist):
    port = PORT_LISTEN_START_FROM
    tmp = "\n"
    for filename in filelist:
        tmp += filename  + "'s port: " + str(port) + "\n"
        port = port + 1
    print tmp
    with open(FLAG_BAK_FILENAME, 'a') as f:
        f.write(tmp)

    
filelist = getFileList()
flags = generateFlags(filelist)
generateBinPort(filelist)
generateXinetd(filelist)
generateDockerfile(filelist, flags)
generateDockerCompose(len(filelist))



