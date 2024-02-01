主要描述 powershell 美化、自动补全，以及配合 git-bash 使用部分 Linux 命令。

文档:

- [powershell install-module](https://learn.microsoft.com/zh-cn/powershell/module/powershellget/install-module?view=powershellget-3.x&viewFallbackFrom=powershell-5.1)。
- [powershell profile-types-and-locations](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_profiles?view=powershell-5.1#profile-types-and-locations)

## 1. 配合git-bash

使 powershell 使用 grep、awk、which...。

需要安装 [Git for windows](https://git-scm.com/download/win)(关于 git-bash 安装 zsh 等的记录见 [git-bash安装](./git-bash安装.md))，PATH 中除了 git 所需的 `Git`、`Git\cmd` 之外，额外加入 `Git\usr\bin` 即可，如我的完整路径为:

```
D:\Git
D:\Git\cmd
D:\Git\usr\bin
```

这样就可以使用 grep 等等了，如下面提取 wlan 的 ip (图2):

```powershell
ipconfig | grep -azio 'wlan.*' | grep -ai 'v4' -m 1 | awk '{print $NF}'
```

> 解释: 
>
> grep 参数 `-a` : 指定二进制的类型为 text，`-z`: 使结束符为文末，而不是换行符，用来全文匹配，`-i`: 忽略大小写，`-o`: 仅输出匹配部分，`-m 1`:  显示第一个匹配。
>
> awk: 默认以 空格和  TAB 分割，`'{print $NF}'` 表示打印每行分割后的最后一项，`$NF` 为其内部变量，代表最后一项。

## 2. vim

使用 Git 中附带的 VIM，其 RUNTIME 在: `\usr\share\vim\vim82`，其可以自动检测到，故无所配置此项。

用户自定义配置在 `$HOME\.vimrc`，写入自己配置即可。

关于 vim 配置有以下三点需要额外增加:

1. 关于 *Vim E303: Unable to open swap file for "[No Name]", recovery impossible* 问题的解决方案(均测试通过)

    - 更改缓存和备份文件目录，引自 [Disabling swap files creation in vim](https://stackoverflow.com/questions/821902/disabling-swap-files-creation-in-vim) 的回答: [Set the following variables in .vimrc or /etc/vimrc to make vim put swap](https://stackoverflow.com/a/15317146/9825841) (需要手动创建这三个文件夹):

      ```
      set backupdir=~/.vim/backup//
      set directory=~/.vim/swap//
      set undodir=~/.vim/undo//
      ```

    - 禁止缓存和备份文件，引自 [Disable any kind of backup/swap file?](https://stackoverflow.com/questions/49707315/disable-any-kind-of-backup-swap-file):

      ```
      set nobackup
      set noswapfile
      ```
    
2. <ctrl+left>与<ctrl+right> 无法以 word 移动解决方案（引自 [control-left and control-right not working in vim, within a screen session](https://superuser.com/questions/532431/control-left-and-control-right-not-working-in-vim-within-a-screen-session) 的回答 [My `.vimrc` in Ubuntu to handle ctrl arrow keys](https://superuser.com/a/1513950/1178506)）:

    ```
    map  <Esc>[1;5A <C-Up>
    map  <Esc>[1;5B <C-Down>
    map  <Esc>[1;5D <C-Left>
    map  <Esc>[1;5C <C-Right>
    cmap <Esc>[1;5A <C-Up>
    cmap <Esc>[1;5B <C-Down>
    cmap <Esc>[1;5D <C-Left>
    cmap <Esc>[1;5C <C-Right>
    
    map  <Esc>[1;2D <S-Left>
    map  <Esc>[1;2C <S-Right>
    cmap <Esc>[1;2D <S-Left>
    cmap <Esc>[1;2C <S-Right>
    ```

3. 中文乱码，设置编码即可:

    ```
    set encoding=utf-8
    set fileencoding=utf-8
    ```

## 3. 主题

这一部分的主题配置参考自 [PowerShell 美化指南](https://coolcode.org/2018/03/16/how-to-make-your-powershell-beautiful/#Windows-10-%E6%8E%A7%E5%88%B6%E5%8F%B0%E7%9A%84%E9%A2%9C%E8%89%B2%E8%AE%BE%E7%BD%AE) 。

以下过程推荐在 powershell 管理员权限下进行，这样会将模块放到全局用户的 `C:\Program Files\WindowsPowerShell\Modules`。

步骤（有需要选择“是否”的，选择“是”）：

1. 使用 [colortool](https://github.com/Microsoft/Terminal/tree/master/src/tools/ColorTool) 更改控制台配色方案。colortool 官方下载链接: [Color Tool April 2019](https://github.com/microsoft/terminal/releases/tag/1904.29002)，iTerm2 配色方案: [mbadolato/**iTerm2-Color-Schemes**](https://github.com/mbadolato/iTerm2-Color-Schemes)，在 [schemes](https://github.com/mbadolato/iTerm2-Color-Schemes/tree/master/schemes) 下下载自己喜欢的配色方案，下载后把 colortool  和配色文件放在一起，在当前文件夹打开 powershell，如我选择 DimmedMonokai，则输入以下:

   ```powershell
   .\ColorTool.exe -b .\DimmedMonokai.itermcolors
   ```

    输入完成之后右击标题栏 --> 属性 --> 确定。上面文件就可以删除了。
    完成之后需要再微调下属性中的背景颜色，否则背景色很奇怪。

2. 信任 PS 官方库:

   ```powershell
   Set-PSRepository -Name PSGallery -InstallationPolicy Trusted
   ```

3. 安装 [PSColor](https://github.com/Davlind/PSColor) 以彩色显示文件列表:

   ```powershell
   Install-Module PSColor
   ```

   加载 PSColor，首次加载时需要设置脚本执行策略:

   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser Bypass  # 加载策略更改
   Import-Module PSColor  # 加载测试 PSColor
   ```

4. 安装 [DirColors](https://github.com/DHowett/DirColors) 以更改 PSColor 彩色文件列表的配色:

   ```powershell
   Install-Module DirColors
   ```

   DirColors 配色方案 [seebi/**dircolors-solarized**](https://github.com/seebi/dircolors-solarized)，例如我下载 *dircolors.256dark*，在 $home 路径下新建 *.dircolors* 文件夹，复制配色文件到此处，生效配色方案:

   ```powershell
   Update-DirColors ~\.dircolors\dircolors.256dark
   ```

5. 命令行 git 信息:

   ```powershell
   Install-Module posh-git
   ```

6. [oh-my-posh](https://ohmyposh.dev/docs/installation/windows#installation)，Powershell 的主题，类似 ohmyzsh，安装:

   ```powershell
   Set-ExecutionPolicy Bypass -Scope Process -Force; Invoke-Expression ((New-Object System.Net.WebClient).DownloadString('https://ohmyposh.dev/install.ps1'))
   ```

   配置主题:

   ```powershell
   oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/ys.omp.json" | Invoke-Expression
   ```


主题和配色配置只在当前会话生效，建议写入到全局启动脚本中（见下面的<6. 启动脚本>）

其他常用命令:

```powershell
# 查看全部 profile
$PROFILE | Select-Object *

# 查看已安装 module 列表
Get-InstalledModule
# 查看某个已安装 module 的所有版本
Get-InstalledModule -Name PSReadLine -AllVersions
# 查看某个已安装 module 的详情
get-installedModule -Name PSReadLine | Select-Object *
```

## 4. 自动补全

基本需求是可以像 [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) 那样提示和补全历史命令。

此功能由 [PowerShell/**PSReadLine** issue 687: Fish-like autocompletion](https://github.com/PowerShell/PSReadLine/issues/687) 发起讨论，并在 [issue 1468: Predictive IntelliSense](https://github.com/PowerShell/PSReadLine/issues/1468) 中得到实现，有时间的伙伴可以点击链接去查看作者的解答，我这里简述下 1468 中完成的功能：1. 完成提示和补全历史命令；2. 增加动态提示函数以及参数。

将 [PSReadLine](https://www.powershellgallery.com/packages/PSReadLine/2.1.0-beta1) 更新到 2.1.0-beta1 以上即可:

```powershell
Install-Module -Name PowerShellGet -Force  # 升级 PSGEt
Install-Module -Name PSReadLine -AllowPrerelease -Force  # 升级 PSReadLine
```

在全局启动脚本中（见下面的<6. 启动脚本>）加入快捷键绑定:

```powershell
Set-PSReadLineKeyHandler -Key "Ctrl+d" -Function MenuComplete
Set-PSReadLineKeyHandler -Key "Ctrl+f" -Function ForwardWord
Set-PSReadLineKeyHandler -Key "Ctrl+b" -Function BackwardWord
Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward
```

~~在加入颜色更改，此处修改提示的颜色为暗绿色(默认的浅灰色在 vscode 暗色主题下阅读困难):~~

```powershell
# 当前版本 (2.2.6) 此配置已被移除
# Set-PSReadLineOption -Colors @{ Prediction = '#2F7004'}
```


## 5. sudo 提权

Linux 终端下比较便捷的一点就是让当前用户临时具有 root 权限，插件 [gerardog/**gsudo**](https://github.com/gerardog/gsudo) 可以实现 cmd/powershell 的提权，下面内容均取自作者 repo。

通过 powershell 安装:

```powershell
PowerShell -Command "Set-ExecutionPolicy RemoteSigned -scope Process; iwr -useb https://raw.githubusercontent.com/gerardog/gsudo/master/installgsudo.ps1 | iex"
```

其命令是 `gsudo`，在首次执行时其可以提示是否创建 `sudo` 的软链接。

其特性:

- 默认在当前窗口提权。(参数 `-n` 可以新打开窗口);
- 权限缓存：UAC 弹窗一次后，几分钟内再次提权不再 UAC 弹窗（0.7 版本下我测试未起效）;
- 可直接追加操作，如: `gsudo touch testSudo.md`

~~目前已知问题：直接追加的操作不支持自定义函数，如: `sudo TestUserFunc` 会报错~~。相关解决方案见 repo 中发起 issue: [Cannot call the function defined in profile](https://github.com/gerardog/gsudo/issues/33).

## 6. 启动脚本

综上，此处将文件列表配色、主题加载、自动补全快捷键、自动补全背景色的配置加入全局启动脚本:

```powershell
# 使用 `vim $PROFILE.AllUsersAllHosts` 编辑全局启动脚本
# 使用 `vim $hostfile` 编辑 hosts 文件
## variables
$hostfile = "C:\Windows\System32\drivers\etc\hosts"

## Prediction from history
Set-PSReadLineOption -PredictionSource History
# autosuggestion key bind
Set-PSReadLineKeyHandler -Key "Ctrl+d" -Function MenuComplete
Set-PSReadLineKeyHandler -Key "Ctrl+f" -Function ForwardWord
Set-PSReadLineKeyHandler -Key "Ctrl+b" -Function BackwardWord
Set-PSReadLineKeyHandler -Key "Ctrl+z" -Function Undo
Set-PSReadLineKeyHandler -Key UpArrow -Function HistorySearchBackward
Set-PSReadLineKeyHandler -Key DownArrow -Function HistorySearchForward

# gsudo
Import-Module 'gsudoModule'

## terminal theme
#Import-Module DirColors
#Import-Module posh-git
Update-DirColors ~/.dircolors/dircolors.256dark
oh-my-posh init pwsh --config "$env:POSH_THEMES_PATH/ys.omp.json" | Invoke-Expression

```

