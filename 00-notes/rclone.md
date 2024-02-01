doc: https://rclone.org/docs/

```bash
# 开启命令行提示, oh-my-zsh 不要 compinit 相关
rclone genautocomplete zsh

# 如果提示 /zsh/vendor-completions 不存在，可以放到家目录下:
acdef_path="${ZSH_CUSTOM:-${ZSH:-~/.oh-my-zsh}/custom}/plugins/rclone"
mkdir -p "$acdef_path"
rclone genautocomplete zsh "$acdef_path/_rclone"
# 然后添加 rclone 到 .zshrc 的 plugins 列表里
plugin=(... rclone)
```

## 0. config

```bash
rclone config paths
rclone config show
```

命令行交互式创建配置:

```bash
rclone config
# s) Set configuration password 可以为配置设置密码，这样在浏览远程时均需要此密码
```

也可以在 web ui 里创建，启动命令:

```bash
rclone rcd --rc-web-gui
```

手动配置示例:

```ini
[al]
# storage systems, from `rclone help backends`
type = webdav
url = http://code-dav:5244/dav
vendor = other
user = al
pass = Q-001-ada
```

## 1. 过滤器

doc:

- [过滤器](https://rclone.org/filtering/)

- [Filter pattern examples](https://rclone.org/filtering/#examples)

可供的选项有 include,exclude,filter。

-  使用范围: `sync`, `move`, `ls`, `lsl`, `md5sum`, `sha1sum`, `size`, `delete`, `check` 等命令；
- 不要同时使用 include 与 exclude，这种需求应使用 filter；
- 如果没有 include  相关配置，则默认会添加 `--include=**` 来选中所有；
- 这三个命令都支持从文件中读取选择；
- 默认区分大小写， `--ignore-case` 可忽略大小写；
-  默认在同步时不删除已排除的文件，`--delete-excluded` 将删除；
   -  例如：a.bak 已被 excluded，则 src 同步到 dst 时，不会删除 dst 的 a.bak，如果加了此参数则会删除 dst 的 a.bak。

-  过滤器设置的路径不管什么操作系统都用 `/`；
-  三个命令生效顺序依次为:  include,exclude,filter；

示例 *(下面仅仅是实际不要同时用三个命令中的两种及以上!!!)*:

```bash
# include
rclone copy /tmp/src /tmp/dst --include="*.jpg" --include-from=in_ex-rules.txt

# exclude
rclone copy /tmp/src /tmp/dst --exclude="*.jpg" --exclude-from=in_ex-rules.txt

# filter
rclone copy \
	/tmp/src /tmp/dst \
  --filter-from=/tmp/filter-rules.txt
  --create-empty-src-dirs
  --ignore-case
```

`/tmp/in_ex-rules.txt`:

```
# a sample include/exclude rule file
*.bak
file2.jpg
```

`/tmp/filter-rules.txt`:

```
# filter
- zz-**
- {tmp,temp}.*
- {tmp,temp}/
- vo/

# ignore git ???
- .git/

# IDE
- .idea/
- .vscode/

# py
- __pycache__/
- .ipynb_checkpoints**

+ *.{jpg,png}
+ /mydir/**
```

### 其他过滤器

https://rclone.org/filtering/#other-filters

- `--[min|max]-[size|age]`： 根据大小，时间过滤
- `--metadata-<same-to-ex/in/filter>`: 根据元数据过滤

## 2. 通用参数

常用参数:

```bash
-n, --dry-run # 不真正执行动作
--log-level LEVEL
	DEBUG  # same to -vv
	INFO   # same to -v
	NOTICE # default
	ERROR  # -q
```

## 3. 查看

下面说明默认为递归, 通过`--max-depth=1` 可不递归.


### 3.1 大小:

- `size`: 大小单位已经处理, `--json` 输出为 json

### 3.2 列表

- `ls` 所有文件及其大小
- `lsl` 比 `ls` 多一个修改时间
- `lsd` 只列文件夹及其时间, 默认不递归, 加 `-R` 递归
- `lsf` 文件[夹]输出结果类似 unix 的 ls(目录后又斜杠), 默认不递归, 加 `-R` 递归
- `lsjson` 文件[夹]输出为 JSON, 默认不递归, 加 `-R` 递归

示例:

```bash
rclone ls al: # list remote root
rclone ls /tmp # list local
```

### 3.3 树形

- `tree` 类似 unix 的 tree
  - `-a` 包含隐藏文件
  - `-s` 大小
- `ncdu` 交互式查看, [rclone_ncdu](https://rclone.org/commands/rclone_ncdu/), 截取部分快捷键
  - ?: 查看快捷键帮助
  - 上下: move; 左右: 上一级和下一级
  - d: 删除所有; D: 删除选中
  - v: 选中, 选中后会高亮; V: 进入或退出 visual select mode

## 4. 同步

- `copy`: 不会删除目标的任何文件
- `sync`: 会删除目标文件, 只会更改目标不会更改源
- `bisync`: 双向同步，两侧都会根据修改时间(ModTime)合并删改，优先不删除(一侧修改一侧删除，同步后会保留)，官方示例: [normal-sync-checks](https://rclone.org/bisync/#normal-sync-checks)
  - 关于 ModTime: [modified-time-and-hashes](https://rclone.org/webdav/#modified-time-and-hashes), 原生 webdav 不支持 ModTime, 但 *Fastmail Files*/*Owncloud*/*Nextcloud* 可通过 header `X-OC-Mtime` 来传递 ModTime, 对于 alist 可选择 *Fastmail Files* 后端来配合 rclone  

常用参数:

- `-n`/`--dry-run`: 不真正生效
- `--create-empty-src-dirs`: 空文件夹也创建
- `--ignore-case`: filter 规则匹配时忽略大小写
- `-P`/`--progress`: 显示进度条


简单同步脚本:

```bash
# arg1: src, default to script path
# dst: last part of src path
SRC="${1:-$(dirname "$(realpath "$0")")}"
REMOTE="al:/local/${2:-public/}"

DST="$(basename "$SRC")"
FILTER_RULES="/etc/rclone/filter-rules.txt"

echo "sync to remote, src=$SRC, dst=$REMOTE$DST, using filter rules=$FILTER_RULES"

rclone bisync "$SRC" "$REMOTE$DST" \
    --filter-from="$FILTER_RULES" \
    --ignore-case \
    --create-empty-src-dirs \
    -P
```
