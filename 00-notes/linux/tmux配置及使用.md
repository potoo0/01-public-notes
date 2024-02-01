## 1. 安装

```bash
apt update
apt install tmux
```

## 2. 配置

这里使用 github 中一个使用人数非常多的配置：repo: [gpakosz/**.tmux**](https://github.com/gpakosz/.tmux)，下面是他的配置的使用方法。

```bash
cd ~
git clone https://github.com/gpakosz/.tmux.git
ln -s -f .tmux/.tmux.conf
cp .tmux/.tmux.conf.local .
```

## 3. 命令及快捷键

参考自：[github gist: ryerh/**tmux-cheatsheet.markdown**](https://gist.github.com/ryerh/14b7c24dfd623ef8edc7)，下面是节选的一部分常用的命令和快捷键。

终端中常用命令：

```bash
tmux [new -s $sess_name]  # 启动新会话, 并可以命令
tmux at [-t $sess_name]  # 恢复会话最后一个会话, 也可以指定会话名
tmux ls  # 会话列表
tmux kill-session -t $sess_name  # 关闭某会话
```

tmux 会话中常用快捷键，需要先按下 *C-b* (`ctrl +  b`)。如果使用第二步的配置文件，则也可以使用 *C-a* (`ctrl + a`)，推荐 *C-a* 因为这两个键距离很近，更容易按。

```bash
c  # 创建新窗口
d  # 后台当前会话并返回到原bash
w  # 列出所有窗口
p/n  # 切换到前/后一个窗口
&  # 关闭当前窗口
:  # 命令提示符

# 多窗口系列
"  #-- 上下分屏
%  #-- 左右分屏
o  #-- 切换焦点分屏
<space>  #-- 上下左右互换
z  #-- 最大最小焦点窗口
!  #-- 当前焦点窗口置于新窗口
x  #-- close windows

join-pane -s 2 -t 1 # 移动source窗口2作为子窗到target窗口1
break-pane          # join-pane 的反操作

:set mouse on	# 鼠标模式后按 shift 固定视图

# pane 重命名, window 可以是序号
tmux rename-window -t <window> <your new title>
# 或者在所在窗口使用快捷键: <Ctrl + b + ,> 然后修改
```

## 4. 自启动

打开终端时自动进入 tmux。

如果安装了 zsh 以及配置了 [ohmyzsh](https://github.com/ohmyzsh/ohmyzsh)(我记录的过程 [zsh安装及配置](https://www.brothereye.cn/ubuntu/26/))，可以直接引入 ohmyzsh plugin 即可，关于此插件的官方说明: [ohmyzsh/plugins/tmux](https://github.com/ohmyzsh/ohmyzsh/tree/master/plugins/tmux)。这里贴出配置自启动的方法:

```bash
#vim ~/.zshrc
# 1. 在 zshrc 中添加 `tmux` 到 plugins 字段中
plugins=(... tmux)

# 2. 默认设置 ZSH_TMUX_AUTOSTART == false, 关闭了新终端中自启动，设置为 true 启用自启动。
vim ~/.oh-my-zsh/plugins/tmux/tmux.plugin.zsh
# 此文件中修改 ZSH_TMUX_AUTOSTART:=false 为 true
ZSH_TMUX_AUTOSTART:=true

# 3. source
source ~/.zshrc
```

如果未安装 zsh 或者ohmyzsh，那可以把 ohmyzsh/plugins/zsh 中相关实现代码复制出来放到自己的 zshrc 中。实现自启动的代码在 [ohmyzsh/plugins/tmux/tmux.plugin.zsh](https://github.com/ohmyzsh/ohmyzsh/blob/master/plugins/tmux/tmux.plugin.zsh) 的 92-end（需要去掉部分无关设置）。

## 5. 脚本启动某程序

使用脚本在 tmux 启动某个程序时建议使用 `send-keys` 将命令发送到 bash 里。

下面是启动 frpServer 的脚本。

```bash
touch frps
chmod +x frps
vim frps
```

根据自己的服务修改 *sess_name* 和 *tmux send-keys -t* 后的内容，写入以下内容：

```bash
#!/bin/bash
# frp - start frpServer in tmux

sess_name="frpServer"

export DISABLE_AUTO_TITLE="true"

tmux has-session -t $sess_name
if [ $? = 0 ];then
    echo $sess_name "already exist. attaching..."
    tmux attach-session -t $sess_name
    # exit
else
    echo $sess_name "doesn't exist. creating..."
    tmux new -d -s $sess_name -n home
    tmux send-keys -t $sess_name:1 "cd frp_0.30.0_linux_amd64" Enter
    tmux send-keys -t $sess_name:1 "./frps -c ./frps.ini" Enter
fi
```

### 批量

```bash
SESSION_NAME="batch-job"

# associative arrays(hash, no order):
# 1. `declare -A array=([k1]='v1' [k2]='v2')`
# 2. `${!array[*]}` is the key of array
# 3. `for k in ${!array[*]}` to iterate key, `${array[$k]}` get value
# # demo:
# declare -A array=([k1]='v1' [k2]='v2')
# for k in ${!array[*]}; do
#   echo "key: ${k}, val: ${array[$k]}"
# done

# order by key
PROJECT_DIR='/prj-test/'
PY_DIR='/miniconda3/envs/'
declare -A WINDOW_JOBS=(
    [1-server-8001]="cd ${PROJECT_DIR}server;${PY_DIR}/py311_dj32/python manage.py runserver 8001"
    [2-ui-8081]="cd ${PROJECT_DIR}ui/vue_app;npm run serve -- --port 8081"
)


tmux has-session -t ${SESSION_NAME}
if [ $? = 0 ]; then
    echo ${SESSION_NAME} "already exist. attaching..."
    tmux attach-session -t ${SESSION_NAME}
    # #tmux kill-session -t ${SESSION_NAME}
else
    echo ${SESSION_NAME} "doesn't exist. creating..."
    tmux new-session -d -s ${SESSION_NAME} -n home
    # #-d detach, -n for first windows name

    # #new windows and start job
    # #tmux new-window -n itsm-web -t ${SESSION_NAME}
    # #tmux send-keys -t ${SESSION_NAME}:1 "echo 'run...'" Enter

    keys=( $( echo ${!WINDOW_JOBS[@]} | tr ' ' $'\n' | sort ) )
    idx=0
    for k in ${keys[@]}; do
        echo "start: ${k}"
        idx=$(($idx+1))
        tmux new-window -n "${k}" -t ${SESSION_NAME}
        IFS=';;' read -ra CMDS <<< ${WINDOW_JOBS[$k]}
        for cmd in "${CMDS[@]}"; do
            tmux send-keys -t ${SESSION_NAME}:$idx "$cmd" Enter
        done
    done
fi

```

