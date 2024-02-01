import matplotlib.pyplot as plt
import numpy as np

# 绘制image图像, 显示灰度图时要修改 cmap='binary'
# image data
a = np.array([0.31, 0.37, 0.42,
              0.37, 0.44, 0.53,
              0.42, 0.53, 0.65]).reshape(3, 3)

"""
for the value of "interpolation", check this:
http://matplotlib.org/examples/images_contours_and_fields/interpolation_methods.html
for the value of "origin"= ['upper', 'lower'], check this:
http://matplotlib.org/examples/pylab_examples/image_origin.html
"""
# 显示灰度图时要修改 cmap='binary'
plt.imshow(a, interpolation='nearest',
           cmap='bone',  # 其他写法： cmap=plt.cm.bone
           origin='lower')  # 'lower', 'upper'
plt.colorbar(shrink=0.9)  # 原图的90%长度


plt.show()
