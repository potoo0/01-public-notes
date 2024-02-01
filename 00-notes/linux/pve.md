## pve 首页添加温度

### 1. 依赖配置

```bash
# 安装依赖
apt install lm-sensors

# 检测可用传感器
sensors-detect

# 测试 -j 参数表示 json 输出
sensors -j
```

### 2. 修改源码

> vi 编辑按键不对解决:
> *nano /etc/vim/vimrc.tiny*
> 将 `set compatible` 改为 `set nocompatible`

#### 修改后端

*/usr/share/perl5/PVE/API2/Nodes.pm*, 修改完成后需要重启 `systemctl restart pveproxy`

```perl
# 搜索此部分
$res->{ksm} = {
    shared => $meminfo->{memshared},
};

# 追加的内容
$res->{sensinfo} = `sensors -j`; 
```

#### 修改前端

*/usr/share/pve-manager/js/pvemanagerlib.js*, 修改完成后强制刷新浏览器

1. 在 cpu 信息下展示:
   ```javascript
   # 搜索此部分
   {
       itemId: 'cpus',
       colspan: 2,
       printBar: false,
       title: gettext('CPU(s)'),
       textField: 'cpuinfo',
       renderer: Proxmox.Utils.render_cpu_model,
       value: '',
   },

   # 追加的内容, getattr 具体参数根据 `sensors -j` 调整
   {
     itemId: 'sensinfo',
     colspan: 2,
     printBar: false,
     title: gettext('SensorInfo'),
     textField: 'sensinfo',
     renderer: function (value) {
       const getattr = (data, field) => field.split('.').reduce((p, c) => p ? p[c] : null, data);
   
       const unit = '°C';
       const data = JSON.parse(value);
       const cpuPkg = getattr(data, "coretemp-isa-0000.Package id 0.temp1_input")?.toFixed(1);
       const cpus = [
         getattr(data, "coretemp-isa-0000.Core 0.temp2_input"),
         getattr(data, "coretemp-isa-0000.Core 1.temp3_input"),
         getattr(data, "coretemp-isa-0000.Core 2.temp4_input"),
         getattr(data, "coretemp-isa-0000.Core 3.temp5_input"),
       ];
       const disks = [
         getattr(data, "nvme-pci-0400.Composite.temp1_input"),
         getattr(data, "nvme-pci-0400.Sensor 1.temp2_input"),
         getattr(data, "nvme-pci-0400.Sensor 2.temp3_input"),
       ];
   
       return `CPU温度: ${cpuPkg}${unit} (${cpus.map(d => d?.toFixed(1) + unit).join(' | ')})<br/>
               硬盘: &emsp;&emsp;${disks.map(d => d?.toFixed(1) + unit).join(' | ')}`;
     },
     value: '',
   },
   ```

2. 调整高度:
   - 搜索 `Ext.create('Ext.window.Window'` 其 height 增加 200;
   - 搜索 `Ext.define('PVE.node.StatusView'` 其 height 增加 50;
3. 隐藏仓库订阅提示:
   ```javascript
   # 注释下面内容
   me.items.push({
         xtype: 'pmxNodeInfoRepoStatus',
         itemId: 'repositoryStatus',
         product: 'Proxmox VE',
         repoLink: `#${repoLink}`,
     }); 
   ```
