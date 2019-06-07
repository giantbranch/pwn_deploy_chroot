# pwn_deploy_chroot

> A project for deploying ctf pwn challenge use chroot

中文请点击：

[README_CN.md](https://github.com/giantbranch/pwn_deploy_chroot/blob/master/README_CN.md)

## Before

```
# Install the latest version docker
curl -s https://get.docker.com/ | sh
# Install docker compose
apt install docker-compose
```

## How to use

```
1. Put your pwn program to ./bin （Note that the filename should not contain special characters.）
2. python initialize.py
3. docker-compose up --build -d     # please run as root
```

You can edit config.py to decide whether to replace /bin/sh with catflag

```
# Whether to replace /bin/sh
REPLACE_BINSH = True
```

## Attention

The flag will be generated by the initialize.py and it store in flags.txt

The port information of the pwn program is also inside the flags.txt.

## Update

2018.09.17 version v1

2018.09.23 version v2：Use the catflag program instead of /bin/sh, which is more secure

## Reference

https://github.com/Eadom/ctf_xinetd

## Reward

paypal: https://www.paypal.me/giantbranch

![自愿打赏][1]


  [1]: http://pic.giantbranch.cn/pic/1551450728861.jpg
