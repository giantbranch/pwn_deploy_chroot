#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-09-17 14:32:32
# @Author  : giantbranch (giantbranch@gmail.com)
# @Link    : http://www.giantbranch.cn/
# @tags : 

from config import *
import os
import uuid
import json

def getFileList():
    filelist = []
    for filename in os.listdir(PWN_BIN_PATH):
        filelist.append(filename)
    filelist.sort()
    return filelist

def isExistBeforeGetFlagAndPort(filename, contentBefore):
    filename_tmp = ""
    tmp_dict = ""
    ret = False
    for line in contentBefore:
        tmp_dict = json.loads(line)
        filename_tmp = tmp_dict["filename"]
        if filename == filename_tmp:
            ret = [tmp_dict["flag"], tmp_dict["port"]]
    return ret

def generateFlags(filelist):
    tmp_flag = ""
    contentBefore = []
    if not os.path.exists(FLAG_BAK_FILENAME):
        os.popen("touch " + FLAG_BAK_FILENAME)

    with open(FLAG_BAK_FILENAME, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            contentBefore.append(line)
    # bin's num != flags.txt's linenum, empty the flags.txt
    if len(filelist) != len(contentBefore):
        os.popen("echo '' > " + FLAG_BAK_FILENAME)
        contentBefore = []
    port = PORT_LISTEN_START_FROM + len(contentBefore)
    flags = []
    with open(FLAG_BAK_FILENAME, 'w') as f:
        for filename in filelist:
            flag_dict = {}
            ret = isExistBeforeGetFlagAndPort(filename, contentBefore)
            if ret == False:
                tmp_flag = "flag{" + str(uuid.uuid4()) + "}"
                flag_dict["port"] = port
                port = port + 1
            else:
                tmp_flag = ret[0]
                flag_dict["port"] = ret[1]

            flag_dict["filename"] = filename
            flag_dict["flag"] = tmp_flag
            flag_json = json.dumps(flag_dict)
            print flag_json
            f.write(flag_json + "\n")
            flags.append(tmp_flag)
    return flags

def generateXinetd(filelist):
    contentBefore = []
    with open(FLAG_BAK_FILENAME, 'r') as f:
        while 1:
            line = f.readline()
            if not line:
                break
            contentBefore.append(line)
    conf = ""
    uid = 1000
    for filename in filelist:
        port = isExistBeforeGetFlagAndPort(filename, contentBefore)[1]
        conf += XINETD % (port, str(uid) + ":" + str(uid), filename, filename)
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
        if REPLACE_BINSH:
            copybin += "COPY ./catflag" + " /home/" + filename + "/bin/sh\n"
        else:
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
    if not REPLACE_BINSH:
        # ness_bin = '''mkdir /home/%s/bin && cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
        ness_bin = '''&& cp /bin/sh /home/%s/bin && cp /bin/ls /home/%s/bin && cp /bin/cat /home/%s/bin'''
    copy_lib_bin_dev = "RUN "
    for x in xrange(0, len(filelist)):
        copy_lib_bin_dev += "cp -R /lib* /home/" + filelist[x]  + " && "
        copy_lib_bin_dev += "cp -R /usr/lib* /home/" + filelist[x]  + " && "
        copy_lib_bin_dev += dev % (filelist[x], filelist[x], filelist[x], filelist[x], filelist[x], filelist[x])
        if x == len(filelist) - 1:
            if not REPLACE_BINSH:
                copy_lib_bin_dev += ness_bin % (filelist[x], filelist[x], filelist[x])
            pass                
        else: 
            if not REPLACE_BINSH:   
                copy_lib_bin_dev += ness_bin % (filelist[x], filelist[x], filelist[x]) + " && "
            else:
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

# def generateBinPort(filelist):
#     port = PORT_LISTEN_START_FROM
#     tmp = ""
#     for filename in filelist:
#         tmp += filename  + "'s port: " + str(port) + "\n"
#         port = port + 1
#     print tmp
#     with open(PORT_INFO_FILENAME, 'w') as f:
#         f.write(tmp)
    
filelist = getFileList()
flags = generateFlags(filelist)
# generateBinPort(filelist)
generateXinetd(filelist)
generateDockerfile(filelist, flags)
generateDockerCompose(len(filelist))



