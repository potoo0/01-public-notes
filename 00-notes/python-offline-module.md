## 1. conda 离线

### 1.1 离线创建虚拟环境

复制 base 环境:

```bash
conda create --clone base --prefix $HOME/.conda/envs/YOUR_ENV_NAME
```

### 1.2 离线 py 包

#### 1.2.1 依赖简单的 py 包

离线依赖较少的 py 包。

1. 下载: 官网下载: https://repo.anaconda.com/pkgs/, 在这里找到自己需要的 channel 以及操作系统版本。

   此处使用 main channel ，linux-64: 链接为 https://repo.anaconda.com/pkgs/main/linux-64/

   查找安装包并下载到本地。

2. 安装: `conda install --use-local <package_name>`

   参数说明：--use-local 与 -c local 相同

如离线 nb_conda-2.2.1:

1. py 版本 py3.7 的包下载地址为: [nb_conda-2.2.1](https://repo.anaconda.com/pkgs/main/linux-64/nb_conda-2.2.1-py37_0.tar.bz2)
2. 安装: `conda install --use-local nb_conda-2.2.1-py37_0.tar.bz2`

#### 1.2.2 依赖复杂的 py 包

离线有很多层依赖的 py 包。

下载 py 包的目录为 conda 的 *package cache*，此路径通过命令 `conda info` 查看。

以 nb_conda 为例，nb_conda 插件作用：使 jupyterlab 自动发现 python kernel，只要安装 ipykernel 就会自动添加到 jupyterlab 中。

1. 下载之前先备份原环境缓存的包 ( 路径依照实际情况修改 ):

   ```bash
   mv /usr/local/miniconda3/pkgs /usr/local/miniconda3/pkgs.bak
   mkdir /usr/local/miniconda3/pkgs
   ```

2. 下载 ( 会下载到 pkgs 下):

   ```bash
   conda install nb_conda --download-only
   ```

   打包 pkgs ( 路径依照实际情况修改 ):

   ```bash
   tar -czvf ~/pkgs.tar /usr/local/miniconda3/pkgs
   # 恢复上面备份
   rm -rf /usr/local/miniconda3/pkgs
   mv /usr/local/miniconda3/pkgs.bak /usr/local/miniconda3/pkgs
   ```

   将此 pkgs.tar 上传到目的机器上，

3. 解压 ( 路径依照实际情况修改 ):

   ```bash
   mv /usr/local/miniconda3/pkgs /usr/local/miniconda3/pkgs.bak
   mkdir /usr/local/miniconda3/pkgs
   tar -xzvf ~/pkgs.tar /usr/local/miniconda3/pkgs
   ```

   安装:

   ```bash
   conda install nb_conda --offline
   ```

## 2. pip 离线 py 包

pip download 会下载依赖包。

以 numpy 为例。下载:

```bash
pip download numpy -d ./package
```

> -d 指定文件夹，默认为当前文件夹。

安装，将上面下载的 package 文件夹上传到目的机器上 :

```bash
pip install numpy --no-index --find-links=./package
```

## 3. jupyterlab 插件离线

适用于需要使用命令 `jupyter labextension install` 安装的插件，这类插件需要依赖 npm。

> jlab 3.0 后支持将插件资源全部打包发布到 pypi，不再依赖 npm。但目前尚有部分插件未使用此特性，如 plotly，故还需要 npm。

以 plotly 为例:

1. 下载:

   ```bash
   jupyter labextension install jupyterlab-plotly@4.14.3 --no-build

   # <conda_folder> 更改为自己的路径
   cd <conda_folder>/share/jupyter/lab/staging
   npm install

   # 打包
   cd ..
   tar -czvf ~/staging.tar ./staging
   ```

   下载 staging.tar 到目的机器。

2. 安装:

   ```bash
   cd <conda_folder>/share/jupyter/lab

   # 解压
   tar -xzvf ~/staging.tar ./

   # 安装
   cd staging && jupyter lab build
   ```
