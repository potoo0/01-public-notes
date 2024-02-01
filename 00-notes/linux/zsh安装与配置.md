说明: 
  1. 修改默认 shell 前进行安装前备份 `/etc/passwd`。
  2. 安装 zsh 后安装 oh-my-zsh 用于快速配置 zsh。
  3. 安装 oh-my-zsh 后环境变量入口会从 `./bashrc` 变成 `./zshrc`。

## 1. 安装

```bash
sudo apt update
sudo apt upgrade

sudo apt install git zsh

# 更改为默认
chsh -s /bin/zsh
```

## 2. 配置

[ohmyzsh/**ohmyzsh**](https://github.com/ohmyzsh/ohmyzsh) 是 zsh 的一个配置框架，其继承许多 zsh 主题以及整合了插件。

通过 curl 安装:

```bash
# 如果要把 oh-my-zsh 安装为全局需要先设置 ZSH=/usr/share/oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
```

使 zshrc 更改生效:

```bash
source ~/.zshrc
```

## 5. 插件

### 5.1 自动跳转

[wting/**autojump**](https://github.com/wting/autojump) 可以学习使用最频繁切换的路径，通过 `j` 来跳转。

安装命令:

```bash
sudo apt-get install autojump
```

添加到 zshrc:

```bash
vim .zshrc
# 在最后一行加入，注意点后面是一个空格
. /usr/share/autojump/autojump.sh

# 生效
# source ~/.zshrc
```

### 5.2 语法高亮

[zsh-users/**zsh-syntax-highlighting**](https://github.com/zsh-users/zsh-syntax-highlighting) 增强 zsh 的语法高亮。

安装:

```bash
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

添加到 zshrc:
```bash
# vim ~/.zshrc
# zshrc plugins 中换行继续添加 zsh-autosuggestions，如
plugins=(
	git
	zsh-syntax-highlighting
)
```

### 5.3 命令建议

[zsh-users/**zsh-autosuggestions**](https://github.com/zsh-users/zsh-autosuggestions) 通过记录历史命令来进行命令建议。

安装：

```bash
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
```

添加到 zshrc:

```bash
# vim ~/.zshrc

# zshrc plugins 中添加 zsh-autosuggestions，如
plugins=(
	git
	zsh-syntax-highlighting
	zsh-autosuggestions
)
```

## 6. 其他自定义

添加常用设置到 `~/.zshrc`。

1. 通配符：ZSH 默认情况下会自己拦截如 `* ?` 之类的通配符，并尝试自己来解释，修改配置可解决
   ```bash
   setopt no_nomatch
   ```

2. 命令别名：ls 详细列表中文件夹与文件分开，文件夹在上
   ```bash
   # --group-directories-first
   alias l="ls -ahl --group-directories-first"
   ```

3. 历史命令去重：
   ```bash
   # ignore dups
   setopt hist_ignore_all_dups
   ```

## 7. 配置主题

官方主题：[ohmyzsh - External themes](https://github.com/robbyrussell/oh-my-zsh/wiki/External-themes)，此链接里包含了常用主题的截图对比，此处使用 *ys* 主题:

```bash
sudo vim ~/.zshrc
```

找到 `ZSH_THEME="robbyrussell"`，修改为：`ZSH_THEME="ys"`；

生效：

```bash
source ~/.zshrc
```
