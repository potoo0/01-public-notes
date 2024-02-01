树莓派3b+ 加 *Movidius NCS* 完整环境配置。

区别 [Python-Opencv4_withIE_onRaspi](https://www.brothereye.cn/ubuntu/611/) 中介绍的下载解压的方式，完整安装的可以使用 库 `openvino.inference_engine`，优点是可以利用多进程来同时使用 n 个计算设备，如果你只有一个计算设备那就别完整安装了，添加预编译的 OpenCV 到 PATH 就行了，具体见上面的链接。

前置条件：

- raspberry 3b+   OS: Raspbian
- Python3.5+ (Raspbian9 自带)

## 1. 安装 OpenVINO:

树莓派安装 OpenVINO 无须编译，只需下载解压添加环境变量即可使用。

OpenVINO 下载链接：[OpenVINO 2018.5.445](https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz)

官方教程：[Install the Intel Distribution of OpenVINO Toolkit for Raspbian OS](https://software.intel.com/en-us/articles/OpenVINO-Install-RaspberryPI)

官方提供的预训练模型：[Overview of OpenVINO Toolkit Pre-Trained Models](http://docs.openvinotoolkit.org/latest/_docs_Pre_Trained_Models.html)

## 2. 转换自己模型

OpenVINO 和 OpenCV dnn 使用的模型文件都是 IE(Inference Engine)模型，所以需要将自己的模型转化过去，对于 tensorflow 一般过程是： ckpt模型文件 --> pb 模型文件 --> IR 模型。我这里只说转换 tf model 到 IR，其他的六月份完善。

[Using the Model Optimizer to Convert TensorFlow Models](https://software.intel.com/en-us/articles/OpenVINO-Using-TensorFlow)。转换模型需要模块 *Model Optimizer* ，但是遗憾的是树莓派免编译版本并未预置此模块。于是我选择再在 [windows 上安装 OpenVINO](https://software.intel.com/en-us/articles/OpenVINO-Install-Windows#InstallCoreComponents) 转换模型后拷贝到树莓派上，我发现 *Model Optimizer*  使用是不需要其他依赖，所以可以从其他安装过的那里提取出来。这里是 windows 版的，可以下载直接使用。[百度云分享: model_Optimizer_windows](https://pan.baidu.com/s/1byOP4XpcqEyUzJIpVifSXQ) 密码: 2pxe

支持的 tf 的目标检测模型：[Supported Frozen Topologies from TensorFlow Object Detection Models Zoo](https://software.intel.com/en-us/articles/OpenVINO-Using-TensorFlow#inpage-nav-2-1-2) 

tensorflow 模型: [Object Detection Models Zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md)

以下是我电脑转换 [SSD Lite MobileNet V2 COCO](http://download.tensorflow.org/models/object_detection/ssdlite_mobilenet_v2_coco_2018_05_09.tar.gz) 的代码（win10的powershell脚本，linux 的话将文件目录和 shell 换行符修改即可）:

```powershell
cd E:\model_optimizer
python3 .\mo_tf.py `
--input_model E:\ssdlite_mobilenet_v2\frozen_inference_graph.pb `
--model_name ssd_mobilenet_v2 `
--data_type FP16 `
--output_dir E:\ssdlite_mobilenet_v2\ `
--batch 1 `
--tensorflow_object_detection_api_pipeline_config E:\ssdlite_mobilenet_v2\pipeline.config `
--tensorflow_use_custom_operations_config .\extensions\front\tf\ssd_v2_support.json
# --log_level DEBUG
```

首先 cd 到 model_optimizer 的目录，然后执行转换。

模型转化需要注意 (参数的官方解释[Converting_Model_General](https://docs.openvinotoolkit.org/latest/_docs_MO_DG_prepare_model_convert_model_Converting_Model_General.html), [Convert_Model_From_TensorFlow](https://docs.openvinotoolkit.org/latest/_docs_MO_DG_prepare_model_convert_model_Convert_Model_From_TensorFlow.html#tensorflow_specific_conversion_params))：

- `–batch` 或 `input_shape`: 输入层的shape，一般使用 batch 1 就好了
- `–data_type`: 数据的类型，可以默认 (2018R5 版本默认参数转化的模型在 2019R1 中无法使用，我测试了下只有值为 *FP16* 时，模型在两个版本下都可用)
- `--reverse_input_channels`: 是否颠倒 RGB 通道
- `--tensorflow_object_detection_api_pipeline_config`: 模型压缩包下的pipeline.config
- `--tensorflow_use_custom_operations_config`: model_optimizer 下的 ssd_v2_support.json，用来将 tf ssd 的网络层转化成 IR的网络层

使用时需要注意：

- 归一化参数，如果是使用预训练的模型或者其他人的模型，没有注明归一化的 `mean` 和 `std` ，那就使用是预先不自己做归一化
- RGB 通道，无法确定情况下，找几张图片测试下颠倒 RGB 和不颠倒哪个准确率高那就使用哪个

## 3. 其他问题

OpenVINO 2018R5 转化的模型在 2019R1 中不一定可以使用，需要注意其数据类型 `data_type` ，我测试了下，只有在参数 `data_type`  的值为 `FP16` 时才可通用。