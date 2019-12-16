# 常见问题

1、pwn题目对应的端口及flag在哪里

这个信息储存在flags.txt里面

2、为什么我部署了之后，题目对应的端口与实际监听的端口不对应

那可能是你部署过一次，之后删掉了bin目录的题目，之后又拉进去一些新的题目，而flags.txt储存了之前被删掉的pwn题目的信息，所以导致不对应

或者你修改了配置文件，而flags.txt储存了之前部署的pwn题目的信息

解决方法：将flags.txt删掉后，重新部署

注意：我保留flags.txt实际是为了方便不断添加新的题目，而旧的题目的flag，以及端口保持不变。

3、假如我不想用ubuntu 16.04部署题目，我要用18.04，怎么办？

- 你可以修改config.py里面的DOCKERFILE变量的第一行`FROM ubuntu:16.04`为`FROM ubuntu:18.04`
- 或者运行了python initialize.py后，再去修改Dockerfile文件，最后再build
这个也在issue中回答过了
https://github.com/giantbranch/pwn_deploy_chroot/issues/4

当然可能有些docker容器可能需要修改apt安装的库，或者自己解决一些问题

4、为什么本地正常getshell，用这个部署会输出：So you must call system(\"sh\") or system(\"/bin/sh\") ？

因为默认情况下，我使用了我写的catflag程序替换/bin/sh，你可以在config.py中关闭替换

```
# Whether to replace /bin/sh

## replace
REPLACE_BINSH = True
## not replace(default)
REPLACE_BINSH = False
```

5、可不可在同一台机子运行多个这种容器实例，比如一个ubuntu16.04，另一个是18.04？

可以的，

- 将项目clone到不同文件夹
- 修改其中一个的config.py的PORT_LISTEN_START_FROM变量，修改起始监听端口
- 在执行完python initialize.py后，修改docker-compose.yml里面的所有pwn_deploy_chroot，比如都加个后缀pwn_deploy_chroot_1804
- 最后再docker-compose up --build -d



**其他问题请先看下面的文章再问**

[如何安全快速地部署多道ctf pwn比赛题目 - How to deploy many ctf pwn game safely and quickly](http://www.giantbranch.cn/2018/09/24/%E5%A6%82%E4%BD%95%E5%AE%89%E5%85%A8%E5%BF%AB%E9%80%9F%E5%9C%B0%E9%83%A8%E7%BD%B2%E5%A4%9A%E9%81%93ctf%20pwn%E6%AF%94%E8%B5%9B%E9%A2%98%E7%9B%AE/)










