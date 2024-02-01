## git-bash 安装

windows 的 git-bash 安装 zsh/rsync 等工具。

> git bash 是基于 MSYS2 的，可以安装 pacman 包管理器来安装下面工具

> 参考
> [Using fish shell with git bash on windows](https://gist.github.com/rafaelpadovezi/1cfc1026f78255458f5a2ea56291ed23)

git-bash 在文件管理器打开文件夹:

```bash
# open path in windows file explore, default to current
win() { : $(cd "${1:-.}" && echo 'start .' | cmd) ; }
```

### 1. 手动安装

对于有子依赖的包安装比较麻烦，收集所有依赖可以在某一台未安装的环境上先清空 pacman 的缓存( 目录 *var/cache/pacman*)，然后安装，然后缓存目录里就包含需要的依赖。

流程:
1. 在 [msys2 packages](https://packages.msys2.org/search?t=binpkg&q=pacman) 中搜索下载 (搜索类型需要改为 *Packages* 而不是 *Base Packages*);
2. 如果压缩格式为 zst，则使用 [zstd](https://github.com/facebook/zstd) 解压: `zstd -d xxx.pkg.tar.zst` 再 tar 解压 `tar -zxvf xxx.pkg.tar` (等效于 `tar -xvf xxx.pkg.tar.zst`, 需要 zstd 在环境变量中);
3. 复制到对应目录下。

手动安装单个包示例:
1. 下载二进制包 `mingw-w64-x86_64-jq-1.6-5-any.pkg.tar.zst`
2. 解压 tar 解压命令: `mkdir jq_bin; tar -xvf mingw-w64-x86_64-jq-1.6-5-any.pkg.tar.zst -C jq_bin`。
3. 复制(git-bash 下执行): `cp -r jq_bin/mingw64 /`

### 2. pacman

下载并解压到 git 根目录 [pacman](https://packages.msys2.org/package/pacman?repo=msys&variant=x86_64), [pacman-mirrors](https://packages.msys2.org/package/pacman-mirrors?repo=msys), [msys2-keyring](https://packages.msys2.org/package/msys2-keyring?repo=msys)

设置 pacman 镜像:
```bash
pacman-key --init
pacman-key --populate msys2  # 设置 key
pacman -Syu  # 更新
```

pacman 安装命令:

```bash
pacman -S <package-name>
```

如果提示 exists-on-filesystem，则强制覆盖:  `pacman -S --overwrite "*" <package-name>`

清除 pacman 所有缓存: `pacman -Scc`

#### 安装 zsh

此处将 oh-my-zsh 安装到 git 文件夹下:

```bash
pacman -S --overwrite "*" zsh

export ZSH=/usr/share/oh-my-zsh

# install oh-my-zsh
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# install plugin
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-$ZSH}/plugins/zsh-autosuggestions
```

在命令行里打开 windows 资源管理器命令:

- cmd: `start E:\Master`
- powershell: `ii E:\Master`
- bash，调 cmd 来实现，例如:
  ```bash
  # open path in windows file explore, default to current
  win() { : $(cd "${1:-.}" && echo 'start .' | cmd) ; }
  ```

默认 zsh:
```bash
# ~/.bashrc
export MSYS=enable_pcon
export TIME_STYLE=long-iso
# immediately append current history
#export PROMPT_COMMAND='history -a'

# Launch zsh
if [ -t 1 ]; then
  if [[ $(bash --version) =~ .*5\.2\. ]]; then
      exec zsh
  fi
fi

source /0_config/0_shell_init.sh
```

> 注意: git-for-windows(在 2.38-2.43 之间已被修复，具体版本未知) 环境下 zsh 在有 git 仓库下调整窗口大小会卡死, 原因是 prompt_info 里调任何 git 都会卡死, 所以可以在 oh-my-zsh/lib/git.zsh 的函数 git_prompt_info 的第一行 `return 0` 退出  

