import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D

# 绘制3D
fig = plt.figure(figsize=(6, 5))
ax = Axes3D(fig)  # 3D坐标轴

# X, Y value
X = np.arange(-4, 4, 0.25)
Y = np.arange(-4, 4, 0.25)
X, Y = np.meshgrid(X, Y)  # x-y 平面的网格

# z轴数据
R = np.sqrt(X ** 2 + Y ** 2)  # 用于绘制XOY的等高线图
Z = np.sin(R)

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=plt.get_cmap('rainbow'))
# rstride=1, cstride=1   : r：横网格跨度，c：列网格跨度
ax.contourf(X, Y, Z, zdir='x', offset=-2, cmap='rainbow')
ax.contourf(X, Y, Z, zdir='y', offset=-2, cmap='rainbow')
ax.contourf(X, Y, Z, zdir='z', offset=-2, cmap='rainbow')
# zdir: 从哪个方向投影下去  offset:等高图偏移原点多少单位
ax.set_zlim(-2, 2)

plt.show()
