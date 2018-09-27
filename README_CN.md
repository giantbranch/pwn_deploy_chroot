# pwn_deploy_chroot

> 可以方便地部署多个pwn题到一个docker容器中(使用chroot)

## 前置

```
# 安装 docker
curl -s https://get.docker.com/ | sh
# 安装 docker-compose
apt install docker-compose
```

## 如何使用

```
1. 将你的pwn二进制程序放到./bin 目录（注意文件名不要含有特殊字符，因为后面会这个文件名创建用户名）
2. python initialize.py
3. docker-compose up --build -d 	# 请用root用户启动
```

## 注意

flag会由`initialize.py`生成，并写入flags.txt中，并且pwn程序对应的端口信息也在里面

## 更新

2018.09.17 version v1

2018.09.23 version v2：使用catflag程序代替/bin/sh，这会更加安全

## 参考

https://github.com/Eadom/ctf_xinetd




