import matplotlib.pyplot as plt
import numpy as np

# 坐标透明度  23-26
x = np.linspace(-3, 3, 50)
y = 0.5 * x

plt.figure(figsize=(6, 4))
# 在 plt 2.0.2 或更高的版本中, 设置 zorder 给 plot 在 z 轴方向排序
plt.plot(x, y, lw=10, zorder=1)
plt.ylim(-2, 2)
ax = plt.gca()  # 获取当前fig的axis属性
ax.spines['right'].set_color('none')  # ax.spines坐标轴边框。让右边边框消失
ax.spines['top'].set_color('none')
ax.xaxis.set_ticks_position('bottom')  # 设置ax的xaxis为下面的坐标轴
ax.yaxis.set_ticks_position('left')  # 设置ax的yaxis为左边的坐标轴
# 新axis定位方式是使用data。还有其他定位方法，axes, outward。axis：定位到axis的百分之几
ax.spines['bottom'].set_position(('data', 0))  # 设置下面的axis位置是数据的yaxis的0处
ax.spines['left'].set_position(('data', 0))  # 设置左边的axis位置是数据的xaxis的0处
# 调整坐标，对被遮挡的图像调节相关透明度，本例中设置 x轴 和 y轴 的刻度数字进行透明度设置
# label.set_fontsize(12)重新调节字体大小，bbox设置目的内容的透明度相关参，facecolor调节
# box 前景色edgecolor 设置边框， 本处设置边框为无，alpha设置透明度
for label in ax.get_xticklabels() + ax.get_yticklabels():
    label.set_fontsize(12)
    label.set_bbox(dict(facecolor='white', edgecolor='None',
                        alpha=0.7, zorder=2))

plt.show()
