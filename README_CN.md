# pwn_deploy_chroot

> 可以方便地部署多个pwn题到一个docker容器中(使用chroot)

详细部署示例请看:

[如何安全快速地部署多道ctf pwn比赛题目](http://www.giantbranch.cn/2018/09/24/%E5%A6%82%E4%BD%95%E5%AE%89%E5%85%A8%E5%BF%AB%E9%80%9F%E5%9C%B0%E9%83%A8%E7%BD%B2%E5%A4%9A%E9%81%93ctf%20pwn%E6%AF%94%E8%B5%9B%E9%A2%98%E7%9B%AE/)

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

你可以编辑config.py决定是否用我的catflag程序去替换/bin/sh

```
# Whether to replace /bin/sh

## 替换
REPLACE_BINSH = True
## 不替换（默认）
REPLACE_BINSH = False
```

## 注意

flag会由`initialize.py`生成，并写入flags.txt中

pwn程序对应的端口信息也在flags.txt中

## 更新

2018.09.17 version v1

2018.09.23 version v2：使用catflag程序代替/bin/sh，这会更加安全

## 参考

https://github.com/Eadom/ctf_xinetd

## 自愿打赏

paypal: https://www.paypal.me/giantbranch

![自愿打赏][1]


[1]: http://pic.giantbranch.cn/pic/1551450728861.jpg


