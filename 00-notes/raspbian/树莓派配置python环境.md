经过一整天的折腾，从 py3.6 到 py2.7 到 py3.5 又到 py3.6 最后到 py3.5，总结了主要过程与心得

---

以下配置的环境:

- os: Raspbian Debian 9.8 (stretch)
- Kernel: armv7l Linux

树莓派有桌面版镜像中以附带了 python2.7 与 python3.5.4，但是现在很多库都不支持 py2.7 ，所以推荐使用 3.5 以上的版本。但是由于不用处理器不同py版本之间的py库的 whl安装文件不同，树莓派官方仅提供了大多数 py35 的编译好的库文件，所以**推荐使用 py3.5**。如果真的需要装 3.6以上版本见 github：[**raspbian-python3.6.rst**](https://gist.github.com/dschep/24aa61672a2092246eaca2824400d37f)

> 关于 python 库 whl文件的编译：Python中 `pip` 可以直接安装的文件是 *whl文件*，而python 的包源文件是 *zip 压缩文件*，包含了 *py 文件*和 *c 文件*，其需要*编译*后生成 *whl 文件*，编译是个很漫长而且会出各种麻烦错误的过程。有的库没有系统或者 cpu 架构的限制，如`pyparsing`，它发布的 whl文件后缀就是 `none-any.whl`。有的库(我测试下来好像大多都是有大量计算的库) 需要使用当前用户的处理器来生成对应的 *whl文件*，python官方是给出了常见配置编译好的 *whl文件*，比如 windows 64位处理器那其专用的 *whl文件*后缀就应该是 `win_amd64.whl`(amd64 指的是 amd64 架构的处理器)。对于树莓派 3b+，那其对应的可直接安装的 whl文件的后缀就是 `linux_armv7l.whl`，树莓派 py3.5 提供了很多针对此架构的 *whl文件*，但是 py3.6 只有非常少一部分有编译好的。

linux 下安装 python 的包的途径有两种方式，一种是 linux 系统的 `apt install python(3)-xxx`，这种方式安装的是对应 linux 发行商把稳定的 python 包发布到了自己的 Package Archives，另一种是 python 的包管理器 `pip install xxx`。

## 1. 更换默认 python

注意：**不是特别需求或者不喜欢折腾的不要更换默认 python**。如果更换了默认的python，那以后就没办法再使用 `apt install python-xxx` 给 python2 安装包了，使用 `apt isntall python3-xxx` 安装 python3 的包的话需要按下面的错误总结解决两个 python 2与3 语法差异带来的错误。

```bash
sudo mv /usr/bin/python /usr/bin/python2
# 上面命令,若python2已存在则删除/usr/bin/python
sudo ln -s /usr/bin/python3.5 /usr/bin/python
sudo mv /usr/bin/pip /usr/bin/pip2
# 上面命令,若不存在pip忽略即可，若已存在pip2，则删除/usr/bin/pip
sudo ln -s /usr/bin/pip3.5 /usr/bin/pip
python -V  # 检查默认python版本
pip -V  # 检查默认pip版本，如果pip版本与上面的python版本不符，使用下面更新pip可自动解决
```

## 2. 更新 pip

```bash
# 推荐下面方法
wget -c https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

## 3. 安装库

更换源见：[python更换源及安装库](https://www.brothereye.cn/python/128)
安装库：

- 推荐先去 [www.piwheels.org/simple](https://www.piwheels.org/simple) ，这里可以下载到比较新版的，手动下载 whl文件，再安装 (**推荐使用 sudo 安装**，因为有的库会有附带文件需要添加到 path，如 numpy 附带的 f2py)。下面以 opencv 为例：

  ```bash
  # piwheels 下载
  wget -c https://www.piwheels.org/simple/opencv-python/opencv_python-3.4.4.19-cp35-cp35m-linux_armv7l.whl
  sudo pip install ./opencv-python/opencv_python-3.4.4.19-cp35-cp35m-linux_armv7l.whl
  ```

- 如果此网址中没有，那再考虑使用 `sudo apt install python3-***`

## 错误总结：

### 1. 自己编译 whl

如果需要自己编译 whl 来安装，事先需要安装好 `Python3.h` (py2对应的是`Python.h)`和 `freetype`、`png`：

```bash
sudo apt install Python3.h
sudo apt install libfreetype6-dev  # 包含freetype、png
```

### 2. `sudo apt install python-***` 错误

`sudo apt install python-xxx` 是给 python2 安装包，替换默认 python 后 python2 安装包会有很多错误，没有很好的解决办法。

`sudo apt install python3-xxx` 给 python3 安装包会有下面的错误，部分原因是因为 python2 与 python3 之间差异导致的，修改成 python3 语法即可解决。

- `from ConfigParser import SafeConfigParser ImportError: No module named 'ConfigParser'`，将 `ConfigParser` 修改为 `configparser` [参考链接: stackoverflow: importerror-no-module-named-configparser](https://stackoverflow.com/questions/14087598/python-3-importerror-no-module-named-configparser)

```bash
sudo vim /usr/share/python/debpython/version.py
# 将 ConfigParser 修改为 configparser
```

- `"except (IOError, OSError), e: SyntaxError: invalid syntax" when configuring python-lockfile`，将 `except (IOError, OSError), e` 修改为 `except (IOError, OSError) as e`

```bash
sudo vim /usr/share/python/debpython/namespace.py
# 将 `except (IOError, OSError), e` 修改为 `except (IOError, OSError) as e`
```

- `ModuleNotFoundError: No module named 'apt_pkg'` 这个错误没有找到解决方案，不过我发现它并不影响安装结果和使用
- `E: Sub-process /usr/bin/dpkg returned an error code`，解决方案( 参考自 百度经验 [如何解决dpkg: error processing install-info](https://jingyan.baidu.com/article/b2c186c8e95d1dc46ef6ff0c.html) )：

    ```bash
    sudo mv /var/lib/dpkg/info/ /var/lib/dpkg/info_old/
    sudo mkdir /var/lib/dpkg/info/
    sudo apt-get update
    sudo apt-get -f install
    sudo mv /var/lib/dpkg/info/* /var/lib/dpkg/info_old/
    sudo rm -rf /var/lib/dpkg/info
    sudo mv /var/lib/dpkg/info_old/ /var/lib/dpkg/info/
    ```

### 3. `import numpy` 错误

`import numpy` 错误: *Original error was: libf77blas.so.3: cannot open shared object file: No such file or directory*，解决方案(参考自[github issue](https://github.com/Kitt-AI/snowboy/issues/262)):

```bash
sudo apt install libatlas-base-dev
```

### 4. `import cv2` 错误

`import cv2` 错误: *ImportError: libjasper.so.1: cannot open shared object file: No such file or directory*，解决方案(参考自[github issue](https://github.com/amymcgovern/pyparrot/issues/34)):

```bash
sudo apt-get install libjasper-dev  libqtgui4  python3-pyqt5  libqt4-test
```

