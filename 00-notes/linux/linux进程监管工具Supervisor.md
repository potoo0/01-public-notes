linux 下进程管理工具，可直接将脚本文件等作为其子进程进行管理，优点就是不需要自己对一个个脚本文件写服务程序，而且其管理子进程非常方便，可web远程或者命令行管理子进程，支持子进程自启动、重新启动等.

python3 目前没有正式版，开发版本：[supervisor-lrn 4.0.0](https://pypi.org/project/supervisor-lrn/)

官方文档：[Supervisor docs](http://supervisord.org/index.html) ，官方repo：[Supervisor/supervisor](https://github.com/Supervisor/supervisor)

主要包含三部分
- `supervisord`: 父进程，用于启动和守护子进程
- `supervisorctl`: 命令行命令来管理子进程
- `Web Server`: web 管理子进程

## 1. 父进程配置

1. 生成默认配置：
    ```bash
    sudo sh -c "echo_supervisord_conf > /etc/supervisord.conf"
    ```

2. 默认配置的简单更改：
    ```ini
    [include]
    files = /etc/supervisor/conf.d/*.ini
    # 将所有子进程的配置全部放于/etc/supervisor/conf.d，启动 supervisord 时会调用此文件夹下所有 ini 配置文件
    ```
> *.ini 有颜色高亮。而 *.conf 没有颜色高亮，所以推荐使用 ini

3. 其他常用项的说明：
    ```ini
    [inet_http_server]
    # 此项用于 web 远程监控子进程，可设置端口号、账号等，有时需要将 IP 设置成 0.0.0.0来允许远程
    [unix_http_server]
    file=/tmp/supervisor.sock
    # sock 文件目录，后期运行出现错误时 unlink 它可解决一定错误
    [supervisord]
    logfile=/tmp/supervisord.log
    # log 文件目录，需要注意路径，修改其权限为 777 可解决一定错误
    ```

## 2. 子进程配置

以我的内网穿透程序为例：

在 `/etc/supervisor/conf.d/` 下新建 `ngrok_py.ini`，写入：

```ini
[program:ngrok_py]
# [program:APP_NAME]，APP_NAME用于标识

# 目标程序所在目录
directory = /opt/bin/ngrok/

# 启动命令
command = /usr/bin/python3 /opt/bin/ngrok/ngrok.py --arg

# 用户
user = pi

# 自启动与重新启动
## 子进程优先级，值越小表示越优先启动越后关闭
priority = 1
## 自动启动，会随着父进程启动启动
autostart = true
## 程序中断后自动重新启动
autorestart = true
## 自动重新启动的间隔时间
startsecs = 5
## 自动重启的次数
startretries = 3

# 日志设置
## 进程的错误stderr写到输出stdout文件
redirect_stderr = true
## stdout文件路径
stdout_logfile = /var/log/ngrok_py.log
## stdout文件上限大小
stdout_logfile_maxbytes = 1MB
## 上限数量，每个存满后会新建一个新的
stdout_logfile_backups = 10
```

## 3. 父进程自启动

python 安装的没有自启动服务，需要手动添加。

官方提供的 deamon 脚本：[Supervisor initscripts](https://github.com/Supervisor/initscripts)

1. 根据自己系统版本下载后重名命成 `supervisord` 放到 `/etc/init.d/`

2. 修改权限：`sudo chmod 755 /etc/init.d/supervisord` 
   测试：`sudo /etc/init.d/supervisord restart`，*如果有出现信息日志，说明已正常配置服务，若没有任何信息，解决方案见下《注意》*

3. 设置开机自启：
   ```bash
   cd /etc/init.d
   sudo update-rc.d supervisord defaults 90  # 自启
   # sudo update-rc.d -f supervisord remove # 取消自启
   # 加入列表后可通过 sysv-rc-conf 使用GUI来配置。
   ```
> 杂谈：有时移出某个服务的自启动后 ，发现 `sysv-rc-conf` 中仍残留此服务，这时在自启动列表的配置文件 `/var/lib/sysv-rc-conf/services`中删去对应的即可。

**注意**：

在配置前需要确保 supervisor 处于关闭状态，如果自己启动了需要先 `sudo kill  supervisord_pid` 来杀死。

需要核对 `supervisord` 和 `supervisorctl` 的路径：

```bash
whereis supervisord
whereis supervisorctl
```

修改脚本中的路径 `DAEMON`  和 `SUPERVISORCTL` 项的路径。并在上面的 `PATH` 中也追加(不加也不影响使用…)

如，我自己的配置如下：

```bash
whereis supervisord
# -> supervisord: /etc/supervisord.conf /usr/local/bin/supervisord /usr/share/man/man1/supervisord.1.gz
whereis supervisorctl
# -> supervisorctl: /usr/local/bin/supervisorctl /usr/share/man/man1/supervisorctl.1.gz
```

所以需要修改 `supervisord` 和 `supervisorctl` 路径路径为: `/usr/local/bin`:

```bash
sudo vim /etc/init.d/supervisord

# PATH 追加 :/usr/local/bin
PATH=/sbin:/usr/sbin:/bin:/usr/bin:/usr/local/bin
# DAEMON 和 SUPERVISORCTL 修改为:
DAEMON=/usr/local/bin/$NAME
SUPERVISORCTL=/usr/local/bin/supervisorctl
```

## 4. 细节须知

### 4.1 子进程环境变量

在文档中有这么一句话 *“No shell is executed by **supervisord** when it runs a subprocess, so environment variables such as `USER`, `PATH`, `HOME`, `SHELL`, `LOGNAME`, etc. are not changed from their defaults or otherwise reassigned. This is particularly important to note when you are running a program from a **supervisord** run as root with a `user=` stanza in the configuration.”*[Docs > subprocess ##subprocess-environment](http://supervisord.org/subprocess.html#subprocess-environment)，意思是说运行子进程时并不会启动 shell，所以 shell 中自定义的环境变量子进程无法同步，子进程只有默认的环境变量，如果有自己自定义的环境变量，那就需要自己添加。

添加环境变量到子进程中有两个办法，一个是使用此工具的配置文件，另一个是子进程自己添加(如我的 python 脚本，python 有函数来添加临时环境变量)：

- 配置文件添加，在子进程的配置文件中使用参数 `environment`，参数赋值环境变量，如我的代码:

  ```ini
  environment=PYTHONPATH="/home/pi/inference_engine_vpu_arm/python/python3.5/",LD_LIBRARY_PATH="/home/pi/inference_engine_vpu_arm/opencv/lib:/home/pi/inference_engine_vpu_arm/inference_engine/lib/raspbian_9/armv7l/"
  ```

- 子进程是 python 脚本时，可以使用 `os.environ()`，如：

  ```python
  import os
  os.environ['PYTHONPATH'] = "/home/pi/inference_engine_vpu_arm/python/python3.5/"
  os.environ['LD_LIBRARY_PATH'] = "/home/pi/inference_engine_vpu_arm/opencv/lib:/home/pi/inference_engine_vpu_arm/inference_engine/lib/raspbian_9/armv7l/"
  ```

但是！事实上 python 里使用 `os.environ()` 因为加载顺序关系不一定起作用。

### 4.2 子进程日志清除

子进程的日志只能在运行期间才能清除。问题提出：[#1228 Can't clear subprocess's log](https://github.com/Supervisor/supervisor/issues/1228) 及 [#804 ClearProcessLogs xmlrpc command only works when process running](https://github.com/Supervisor/supervisor/issues/804)


> 我在调试程序期间由于 #4.1 问题，所以我需要清除它的日志，结果！每次都无法清除，无论使用 web interface 还是 supervisorctl 都会提示清除成功但是实际上没有，折腾了半天权限，仍无济于事，后来在 github 提问得到了解决。由于我的程序每次都由于环境变量问题很早就出错而停止，所以我都是在停止状态下清除日志，所以失败。

## Fatal error

1. *Error: Another program is already listening on a port that one of our HTTP servers is configured to use...*
   **解决方案**( 参考自:[stackoverflow: supervisor-on-debian-wheezy-another-program-is-already-listening-on-a-port-that](https://stackoverflow.com/questions/25121838/supervisor-on-debian-wheezy-another-program-is-already-listening-on-a-port-that) )：

   ```bash
   sudo /etc/init.d/supervisord stop  # 结束父进程 supervisord
   sudo unlink /tmp/supervisor.sock  # 解除 sock，其路径定义在/etc/supervisord.conf 的 [unix_http_server] 下 file
   ```

2. *unknown error making dispatchers for 'APP_NAME': EACCES*
   **解决方案**：
       `sudo` 来运行 supervisord，若仍有此错误再修改父进程和子进程日志的权限为 777，其路径定义在 `/etc/supervisord.conf` 的 `[supervisord]` 下 `logfile` 和 子进程配置文件的 `stdout_logfile/stderr_logfile`。

