为 python3 编译带 Inference Engine backend 的 Opencv，可以让 Opencv 的 dnn 使用 [intel 的一些边缘计算设备](https://software.intel.com/en-us/articles/OpenVINO-InferEngine)

官方文档：[github repo opecv's wiki: Intel's Deep Learning Inference Engine backend](https://github.com/opencv/opencv/wiki/Intel's-Deep-Learning-Inference-Engine-backend)
	[Opencv docs: Installation in Linux](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html)

这里再重现一遍是因为有些需要注意的问题（一是版本问题，二是视频接口问题），我在 Opencv 的官方论坛和 github 里有提问，想看原回答的详见 [Potoo: Build error with Opencv with Inference Engine backend on raspberry](http://answers.opencv.org/question/211313/build-error-with-opencv-with-inference-engine-backend-on-raspberry/)，[github raspberrypi/linux issue: Webcam failed to set camera param](https://github.com/raspberrypi/linux/issues/2910)

## 1. 安装依赖

参考：[Install OpenCV 3 + Python on your Raspberry Pi](https://www.pyimagesearch.com/2017/09/04/raspbian-stretch-install-opencv-3-python-on-your-raspberry-pi/)
	    [Intel's Deep Learning Inference Engine backend](https://github.com/opencv/opencv/wiki/Intel's-Deep-Learning-Inference-Engine-backend)


```bash
sudo apt-get install \
	cmake pkg-config \
	libjpeg-dev libtiff5-dev libjasper-dev \
	libavcodec-dev libavformat-dev libswscale-dev libv4l-dev \
	libxvidcore-dev libx264-dev \
	libgtk2.0-dev libgtk-3-dev \
	libatlas-base-dev gfortran \
	build-essential \
    xz-utils \
    libgtk2.0-dev:armhf \
    libgstreamer1.0-dev:armhf \
    libgstreamer-plugins-base1.0-dev:armhf \
    python3-dev python3-numpy
```

下载 OpenVINO (我这里将其放在了当前用户家目录):
```bash
cd ~
wget --no-check-certificate https://download.01.org/openvinotoolkit/2018_R5/packages/l_openvino_toolkit_ie_p_2018.5.445.tgz && \
    tar -xf l_openvino_toolkit_ie_p_2018.5.445.tgz
```

## 2. cmake

需要注意版本，OpenCV 与 OpenVINO 版本需要一致，如都是 2018 R5。如果不一致时就需要指定 cmake 参数 `INF_ENGINE_RELEASE`（如 OpenVINO 2018R5 的值是 2018050000），且需要注意 `INF_ENGINE_LIB_DIRS` 的路径（如 OpenVINO 2018R5 的 `INF_ENGINE_LIB_DIRS` 是 `xxx/lib/raspbian_9/armv7l` 而OpenVINO 2019R1 对应的是 `xxx/lib/armv7l`）。

如下面的是编译 OpenCV 2019R1 与 OpenVINO 2018R5 的 cmake 参数:

```bash
cmake -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_INSTALL_PREFIX=/usr/local \
      -DOPENCV_CONFIG_INSTALL_PATH="cmake" \
      -DWITH_IPP=OFF \
      -DBUILD_TESTS=OFF \
      -DBUILD_PERF_TESTS=OFF \
      -DPYTHON3_EXECUTABLE=/usr/bin/python3.5 \
      -DPYTHON_LIBRARY=/usr/lib/arm-linux-gnueabihf/libpython3.5m.so \
      -DPYTHON_INCLUDE_DIR=/usr/include/python3.5m \
      -DPYTHON_INCLUDE_DIR2=/usr/include/arm-linux-gnueabihf/python3.5m \
      -DPYTHON3_NUMPY_INCLUDE_DIRS=/usr/local/lib/python3.5/dist-packages/numpy/core/include \
      -DPYTHON3_CVPY_SUFFIX=".cpython-35m-arm-linux-gnueabihf.so" \
      -DENABLE_NEON=ON \
      -DCPU_BASELINE="NEON" \
      -DWITH_INF_ENGINE=ON \
      -DINF_ENGINE_RELEASE=2018050000 \
      -DINF_ENGINE_LIB_DIRS="~/inference_engine_vpu_arm/deployment_tools/inference_engine/lib/raspbian_9/armv7l" \
      -DINF_ENGINE_INCLUDE_DIRS="~/inference_engine_vpu_arm/deployment_tools/inference_engine/include" \
      -DCMAKE_FIND_ROOT_PATH="~/inference_engine_vpu_arm/" \
      -DENABLE_CXX11=ON ..
```

相对于官方文档的改动：由于我没有使用 docker 来交叉编译，所以就需要去掉一些 *cmake* 的参数:

- `CMAKE_TOOLCHAIN_FILE`: 交叉编译，用于指定编译器和工具链实用程序的位置
- `PKG_CONFIG_EXECUTABLE`: 此参数用于指定 *pkg-config* 执行文件位置，可不使用此参数，会使用系统默认环境变量
- `OPENCV_ENABLE_PKG_CONFIG`: 没有搞明白这个是什么作用，我去掉了，发现并不影响使用


如果上面依赖等没有问题，应当有如下信息:

- Video backend（下面 `DC1394`, `FFMPEG`, `GStreamer`, `v4l/v4l2`有一个就可以了）:
![1554810316209](/md_img/Python-Opencv4_withIE_onRaspi.assets/1554810316209.png)

- inference engine backend:
![1554810333044](/md_img/Python-Opencv4_withIE_onRaspi.assets/1554810333044.png)

- python3:
![1554810343880](/md_img/Python-Opencv4_withIE_onRaspi.assets/1554810343880.png)

## 3. install

```bash
sudo make install
sudo ldconfig

# 有时安装后 import cv2 提示没有，执行下面两行就可以了
cd /usr/local/lib/python3.5/dist-packages/cv2/python-3.5
sudo cp cv2.cpython-35m-arm-linux-gnueabihf.so cv2.so
```

## 4. 其他问题

1. 编译错误

   错误原因主要是依赖和版本不对应造成的，安装上面整理的安装就可以了，详细错误信息这里就不提了。

2. 如果打开摄像头非常缓慢，而且 `cam.set()` 设置摄像头速度也十分十分慢并返回 `False`（其实已经设置成功），且 `cam.get()` 也无法拿到实际数值。代码如下:

    ```python
    import cv2

    cam = cv2.VideoCapture(0)
    
    ret_FPS = cam.set(cv2.CAP_PROP_FPS, 30)
    ret_Wid = cam.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
    ret_Hei = cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
    print('ret_FPS: {}, ret_Wid: {}, ret_Hei: {}'.format(
        ret_FPS, ret_Wid, ret_Hei))  # 总是返回 False
    
    print('cam.get(5): {}; cam.get(3): {}; cam.get(4): {}'.format(cam.get(5), cam.get(3), cam.get(4)))
    ret_frame, frame = cam.read()
    # 返回的并不是刚刚设置的参数(240, 320)，但实际上获取每帧图像满足自己设置的参数，见下面一行代码
    print("frame's shape: ", frame.shape)
    # frame's shape: (240, 320, 3)
    
    cam.release()  # 关闭摄像头
    ```
    
    如果遇到这种情况，修改视频接口就好了，视频接口 api 大全: [opencv: VideoCapture backend](https://docs.opencv.org/3.2.0/d4/d15/group__videoio__flags__base.html#gga023786be1ee68a9105bf2e48c700294dab6ac3effa04f41ed5470375c85a23504)。挨个测试就好了，在我这里使用 v4l 接口就完全正常了，代码如下：
    
    ```python
    cam = cv2.VideoCapture(0 + cv2.CAP_V4L)
    ```

3. 相机经常无故无法连接，需要重新插拔才可使用。是linux内核 FIQ 事件的问题机制，使用 *"NOP" FIQ*机制，就可以了。关于 *"FSM" FIQ* 与 *"NOP" FIQ* 以及相关参数见官方更新日志 [Call for beta testers: FIQ_FSM USB driver rewrite](https://www.raspberrypi.org/forums/viewtopic.php?t=70437)，解决方案( 参考: [github/raspberrypi/linux: Webcam random failure with kernel 3.12.21+](https://github.com/raspberrypi/linux/issues/623#issuecomment-46602819))，在 `/boot/cmdline.txt` 添加:

    ```
    dwc_otg.fiq_fsm_mask=0x3 uvcvideo.trace=0x408
    ```

    > 相关参数解释：
    >
    > - dwc_otg.fiq_enable: Support using the ARM FIQ.
    > - dwc_otg.fiq_fsm_enable: If 1, then the larger FSM handler is installed. If 0, the NOP FIQ is installed.
    > - dwc_otg.fiq_fsm_mask：
    >     - Bit 0: Accelerate non-periodic split transactions
    >     - Bit 1: Accelerate periodic split transactions
    >     - Bit 2: Accelerate high-speed isochronous transactions
    > 
    > 默认值是 0x7，使能全部
    
4. 使用 V4L 接口时分辨率大于 (240, 320) 时无法读取图像，出现错误：`select timeout   VIDIOC_DQBUF: Resource temporarily unavailable` 错误。解决方案(来自：[OpenCV v4l2 select timeout error SOLVED! High FPS!](https://www.raspberrypi.org/forums/viewtopic.php?t=35689)):

    ```bash
    sudo rmmod uvcvideo
    sudo modprobe uvcvideo nodrop=1 timeout=5000 quirks=0x80
    ```

## 5. 偷懒

如果不想自己编译，或者自己编译有错误搞不定，其实也可以使用 OpenVINO 预编译的 Opencv，OpenVINO的下载和解压见上面 <#1. 安装依赖> 的“下载 OpenVINO”。

OpenVINO 2018R5 预编译 Opencv 版本是 4.0.1，对应 OpenVINO 的路径将其添加到 PATH 里，以我的为例：

```bash
vim .zshrc # 没有使用zsh的话就是默认的bash: vim .bashrc
# .zshrc 下添加，注意需要对应 OpenVINO 的路径
export PYTHONPATH="/home/pi/inference_engine_vpu_arm/python/python3.5/"
export LD_LIBRARY_PATH="/home/pi/inference_engine_vpu_arm/opencv/lib:/home/pi/inference_engine_vpu_arm/inference_engine/lib/raspbian_9/armv7l/"
```

**注意**: 

1. 如果使用 jupyter 系列的话，需要将上面依赖库的 PATH 重新添加到 python 环境中，同类型问题见：[jupyternotebook环境变量不同步问题](https://www.brothereye.cn/ubuntu/565/)，但那篇是为了使用完整的 OpenVINO，而这里只想使用它的 OpenCV 所以这里添加 PATH 时就可以去掉一些无关的路径，具体我的处理代码为：在 jupyter 配置文件(生成：`jupyter notebook --generate-config` , 生成后默认在家目录的 `.jupyter/jupyter_notebook_config.py`)中加入：

   ```bash
   import os
   c = get_config()
   os.environ['LD_LIBRARY_PATH'] = '/home/pi/inference_engine_vpu_arm/opencv/lib:/home/pi/inference_engine_vpu_arm/inference_engine/lib/armv7l/'
   c.Spawner.env.update('LD_LIBRARY_PATH')
   ```


2. 在上文 <#2. cmake> 中也提到，OpenVINO 2019R1中相对 2018 R5 有个路径变化了，所以添加 PATH 时也要注意，将路径中的 *raspbian_9* 去掉即可。

