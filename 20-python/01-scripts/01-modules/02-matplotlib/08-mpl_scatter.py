import matplotlib.pyplot as plt
import numpy as np

# 绘制散点图  8-10
n = 10  # 生成随机数个数
x = np.random.normal(0, 1, n)  # 均值0。方差1的n个随机数
y = np.random.normal(0, 1, n)  # 均值0。方差1的n个随机数
colo = np.arctan2(y, x)

print(colo)

plt.scatter(x, y, s=75, c=colo, alpha=0.5)  # s:size  c:color  alpha:透明度
plt.xlim((-1.5, 1.5))
plt.ylim((-1.5, 1.5))
plt.xticks(())  # 设置x坐标轴无
plt.yticks(())  # 设置y坐标轴无

plt.show()
