# pwn_deploy_chroot

> 可以方便地部署多个pwn题到一个docker容器中(使用chroot)

## 前置

```
# 安装 docker
curl -s https://get.docker.com/ | sh
# 安装 docker-compose
apt install docker-compose
```

## 配置

将你的pwn二进制程序放到`./bin` 目录（注意文件名不要含有特殊字符，因为后面会这个文件名创建用户名）

监听端口从10000开始，每多一个pwn就加1，你可以在`config.py`中修改起始监听端口

## 启动

```
python initialize.py
# 请用root用户启动
docker-compose up --build -d
```

## 注意

flag会由`initialize.py`生成，并写入flags.txt中，并且pwn程序对应的端口信息也在里面

## 更新

2018.09.17 version v1
2018.09.23 version v2：使用catflag程序代替/bin/sh，这会更加安全

## 参考

https://github.com/Eadom/ctf_xinetd




