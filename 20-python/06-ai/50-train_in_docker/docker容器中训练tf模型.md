在 docker 下配置 cuda、tensorflow，以及训练模型（优点是多用户之间保持隔离）。docker 的安装见电子书 [Docker – 从入门到实践/安装docker](https://yeasy.gitbook.io/docker_practice/install/ubuntu)。

## 1. 创建用户

```bash
sudo useradd -m potoo  # 创建 potoo，
sudo usermod -aG sudo potoo  # 并分配到sudo组，使其可用sudo提权
sudo passwd potoo  # 更改 potoo 的密码

su potoo  # 切换到 potoo 用户
cd ~  # 切换到当前用户的家目录
```

## 2. 安装 cuda

使用 [Nvidia 容器工具包](https://github.com/NVIDIA/nvidia-docker/blob/master/README.md#quickstart) 来配置环境。此处从其官网中截取 nvidia-docker 的安装命令:

```bash
# 添加 Nvidia 容器工具源地址
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

# 安装 Nvidia 容器工具包
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit

# 重启 docker
sudo systemctl restart docker
```

docker 拉取 cuda 镜像:

```bash
docker pull nvidia/cuda:latest
```

测试 cuda:

```bash
docker run --gpus all --rm nvidia/cuda:latest nvidia-smi
```

注意：截止 docker == 19.03.8, docker-compose == 1.25.5，还未正式支持 docker-compose 部署和启动 nvidia-docker，相关 issue: [Support for NVIDIA GPUs under Docker Compose](https://github.com/docker/compose/issues/6691)。有个曲折的方法是：通过 [nvidia-container-runtime](https://github.com/NVIDIA/nvidia-container-runtime#docker-engine-setup) 设置启动前的 hook。

## 3. 安装 Tensorflow-GPU

Tensorflow 安装详细见官方文档: [Tensorflow Install/docker](https://www.tensorflow.org/install/docker#examples_using_gpu-enabled_images)。

[TensorFlow Docker images](https://hub.docker.com/r/tensorflow/tensorflow/) 镜像拉取，由于我下面要使用 tfhub V2，故这里拉取最新镜像(py 3.6, tf 2.x) (自从 220.1.27 起有标签 py3 和无标签的均指向同一份 py3 的镜像):

```bash
docker pull tensorflow/tensorflow:latest-gpu-jupyter
```

关于 tag 带 jupyter 的镜像，查看[其镜像构建](https://hub.docker.com/layers/tensorflow/tensorflow/latest-gpu-jupyter/images/sha256-f5227081c37421d8ed9ec7e08968a047794fb7b3cebbb2a6ce7cd286ed6a346c?context=explore)会发现其会自动启动 jupyter-notebook，并且目录为 `/tf`，镜像构建的最后一条命令如下:

```bash
/bin/bash -c #(nop)  CMD ["bash" "-c" "source /etc/bash.bashrc && jupyter notebook --notebook-dir=/tf --ip 0.0.0.0 --no-browser --allow-root"]
```

测试:

```bash
# 运行镜像并进入容器内
docker run --gpus all -it tensorflow/tensorflow:latest-gpu-jupyter /bin/bash

# 查看 python 与 tensorflow 版本
python -V  #  本次版本为 Python 3.6.9
pip list | grep tensorflow  # 本次版本为 2.2.0
jupyter --version  # jupyter notebook 为 6.0.3

# 测试 GPU，能正确看到 GPU 信息说明以上环境全部成功配置
python -c "import tensorflow as tf; print(tf.reduce_sum(tf.random.normal([1000, 1000])))"
```

## 4. 训练

先介绍下我所知的开源图像分类模型训练方法，有以下两种方法:

- [tensorflow/**hub**](https://github.com/tensorflow/hub): 模型下载链接: [tfhub.dev](https://tfhub.dev) ，其根据版本又分为:
  - V1: 例程 [hub/examples/image_retraining](https://github.com/tensorflow/hub/tree/master/examples/image_retraining)，仅支持 tf1.x 版本，模型仅限制为 [hub.Modules for TensorFlow 1](https://github.com/tensorflow/hub/blob/master/docs/tf1_hub_module.md);
  - V2: 例程 [hub/examples/colab](https://github.com/tensorflow/hub/tree/master/examples/colab)，仅支持 tf2.x 版本，模型可用 hub.Modules for TensorFlow 1 也可用 [SavedModels for TensorFlow 2](https://github.com/tensorflow/hub/blob/master/docs/tf2_saved_model.md)。
- [tensorflow/**models**/research/slim](https://github.com/tensorflow/models/tree/master/research/slim): 预训练模型下载链接 [slim#pre-trained-models](https://github.com/tensorflow/models/tree/master/research/slim#pre-trained-models)。

我对这两种使用开源模型的优缺点看法:

- hub:
  - 优点：训练十分简单，数据集不需要额外处理;
  - 缺点：~~版本太高~~。
- slim:
  - 优点：开源模型很丰富;
  - 缺点：图像数据需要转化成 tfrecord。

### 4.1 文件准备

此处使用 hub V2，下载官方提供 [notebook 例程](https://github.com/tensorflow/hub/blob/master/examples/colab/tf2_image_retraining.ipynb) 以及模型，国内无法访问 tfhub，所以此处先下载模型解压使用。本次使用模型为 [imagenet 预训练的 mobilenet V2](https://tfhub.dev/google/imagenet/mobilenet_v2_140_224/classification/4)，下载到 models 目录下并解压:

```bash
tar zxvf ./models/imagenet_mobilenet_v2_140_224_classification_4.tar.gz -C ./models
```

启动 #3 拉取的镜像，将 V2 的 notebook 例程、下载的模型以及自己的数据集映射到容器的 `/tf` 文件夹下即可，如:

```bash
docker run \
	--name trainTfModel \
	-p 8888:8888 \
	-v /home/potoo/trainTfModel:/tf/trainTfModel \
	--gpus all \
	tensorflow/tensorflow:latest-gpu-jupyter
```

其中我的 trainTfModel 目录结构:

```bash
$ tree trainTfModel -L 2 -p
trainTfModel
├── [drwxr-xr-x]  datasets
│   ├── [drwxr-xr-x]  fish
│   ├── [drwxr-xr-x]  garbage
│   └── [drwxr-xr-x]  ship
├── [drwxr-xr-t]  models
│   ├── [drwxr-xr-t]  assets
│   ├── [-rwxr-xr-x]  imagenet_mobilenet_v2_140_224_classification_4.tar.gz
│   ├── [-rw-r--r--]  saved_model.pb
│   └── [drwxr-xr-t]  variables
├── [drwxr-xr-x]  output
│   └── [drwxr-xr-x]  saved_model
├── [-rw-r--r--]  tf2_image_fineTune.ipynb
└── [-rw-r--r--]  tf2_image_retraining-Copy1.ipynb

9 directories, 4 files
```

在官方提供的 notebook 例子中需要修改自己数据集路径和模型路径。

### 4.2 notebook 中训练

训练之前安装 tfhub, pillow，此处均在 notebook 中进行:

```python
!pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U tensorflow_hub pillow
```

以及我这里出现的错误: *OSError: image file is truncated*，猜测是因为服务器允许的单次数据大小问题，详细讨论见 [Python PIL “IOError: image file truncated” with big images](https://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images)，此处引用其解决方案:

```python
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
```

更改模型路径以及输入图像尺寸，根据上面我的 trainTfModel 目录结构，此处更改数据集路径为:

```python
MODULE_HANDLE = "./models"
IMAGE_SIZE = (224, 224)
```

更改自己数据集路径，根据上面我的 trainTfModel 目录结构，此处更改数据集路径为:

```python
data_dir = './datasets'
```

最后按照自己需要修改是否 Data Augmentation, Fine-Tune。

我的 notebook 完整如下:

```markdown
# Retraining an Image Classifier

## 1. 环境配置

安装镜像中未安装的 tensorflow_hub 与 pillow，以及我这里出现的错误: *OSError: image file is truncated*，猜测是因为服务器允许的单次数据大小问题，详细讨论见 [Python PIL “IOError: image file truncated” with big images](https://stackoverflow.com/questions/12984426/python-pil-ioerror-image-file-truncated-with-big-images)。

​```python
!pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -U tensorflow_hub pillow
​```

​```python
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
​```

​```python
import itertools
import os

import matplotlib.pylab as plt
import numpy as np

import tensorflow as tf
import tensorflow_hub as hub

print("TF version:", tf.__version__)
print("Hub version:", hub.__version__)
print("GPU is", "available" if tf.test.is_gpu_available() else "NOT AVAILABLE")
​```

## 2. 模型加载
这里是自己手动下载的方式。下载后需要解压。取消下面一行的注释并执行即可。

​```python
#!tar zxvf ./models/imagenet_mobilenet_v2_140_224_classification_4.tar.gz -C ./models
​```

​```python
!ls models
​```

​```python
MODULE_HANDLE = "./models"
IMAGE_SIZE = (224, 224)
print("Using {} with input size {}".format(MODULE_HANDLE, IMAGE_SIZE))

BATCH_SIZE = 16 #@param {type:"integer"}
​```

## 3. 数据集处理

将图片缩放裁剪以符合模型输入，以及划分训练验证集、打乱顺序、数据集增强。

​```python
data_dir = './datasets'
#!ls ./datasets
​```

​```python
datagen_kwargs = dict(rescale=1./255, validation_split=.20)
dataflow_kwargs = dict(target_size=IMAGE_SIZE, batch_size=BATCH_SIZE,
                   interpolation="bilinear")

valid_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
    **datagen_kwargs)
valid_generator = valid_datagen.flow_from_directory(
    data_dir, subset="validation", shuffle=False, **dataflow_kwargs)

do_data_augmentation = True #@param {type:"boolean"}
if do_data_augmentation:
    train_datagen = tf.keras.preprocessing.image.ImageDataGenerator(
        rotation_range=40,
        horizontal_flip=True,
        width_shift_range=0.2, height_shift_range=0.2,
        shear_range=0.2, zoom_range=0.2,
        **datagen_kwargs
    )
else:
    train_datagen = valid_datagen

train_generator = train_datagen.flow_from_directory(
    data_dir, subset="training", shuffle=True, **dataflow_kwargs)
​```

## 4. 模型定义

丢弃原模型的输出层，新建输出层以适应自己数据集的种类。

​```python
do_fine_tuning = True #@param {type:"boolean"}
​```

​```python
print("Building model with", MODULE_HANDLE)
model = tf.keras.Sequential([
    # Explicitly define the input shape so the model can be properly
    # loaded by the TFLiteConverter
    tf.keras.layers.InputLayer(input_shape=IMAGE_SIZE + (3,)),
    hub.KerasLayer(MODULE_HANDLE, trainable=do_fine_tuning),
    tf.keras.layers.Dropout(rate=0.2),
    tf.keras.layers.Dense(train_generator.num_classes,
                          kernel_regularizer=tf.keras.regularizers.l2(0.0001))
])
model.build((None,)+IMAGE_SIZE+(3,))
model.summary()
​```

## 5. 模型训练

### 5.1 优化器

此处使用默认的 SGB，随机梯度下降法。

​```python
model.compile(
    optimizer=tf.keras.optimizers.SGD(lr=0.005, momentum=0.9), 
    loss=tf.keras.losses.CategoricalCrossentropy(from_logits=True, label_smoothing=0.1),
    metrics=['accuracy']
)
​```

### 5.2 训练

​```python
steps_per_epoch = train_generator.samples // train_generator.batch_size
validation_steps = valid_generator.samples // valid_generator.batch_size
hist = model.fit(
    train_generator,
    epochs=5, steps_per_epoch=steps_per_epoch,
    validation_data=valid_generator,
    validation_steps=validation_steps).history
​```

### 5.3 loss、accuracy 曲线

​```python
plt.figure()
plt.ylabel("Loss (training and validation)")
plt.xlabel("Training Steps")
plt.ylim([0,2])
plt.plot(hist["loss"], label='loss')
plt.plot(hist["val_loss"], label='val_loss')
plt.legend();

plt.figure()
plt.ylabel("Accuracy (training and validation)")
plt.xlabel("Training Steps")
plt.ylim([0,1])
plt.plot(hist["accuracy"], label='accuracy')
plt.plot(hist["val_accuracy"], label='val_accuracy')
plt.legend();
​```

### 5.4 保存模型

​```python
saved_model_path = "./output/saved_model"
tf.saved_model.save(model, saved_model_path)
​```

```

