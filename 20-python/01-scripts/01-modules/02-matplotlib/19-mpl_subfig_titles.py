import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['ytick.labelleft'] = False
plt.rcParams['figure.subplot.top'] = 0.7
plt.rcParams['figure.subplot.wspace'] = 0.3
plt.rcParams['figure.subplot.hspace'] = 0.6

examples_to_show = 10
trainImgs = np.zeros((10, 10))

plt.ion()

f, a = plt.subplots(2, examples_to_show,
                    figsize=(examples_to_show, 2))
for i in range(examples_to_show):
    x = np.linspace(-i, i, 50)
    y = x ** 2
    a[0][i].plot(x, y)
    a[1][i].plot(x, y)

fig, axes = plt.subplots(2, examples_to_show // 2)
fig.suptitle(f'Train data 1-{examples_to_show}', fontsize=16)
# fig.subplots_adjust(hspace=0.3, wspace=0.8)
# hspace上下间距，wspace左右间距
# also available in rcParams
for i, ax in enumerate(axes.flat):  # 需要把 axes 转成一维，使用 flat属性 或者 flatten()方法
    ax.imshow(trainImgs, cmap='binary')
    ax.set_title(f'train data {i}')

plt.ioff()
plt.show()
