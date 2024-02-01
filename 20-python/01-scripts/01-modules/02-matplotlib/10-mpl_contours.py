import matplotlib.pyplot as plt
import numpy as np

# 绘制等高线图  13-23


def f(x, y):
    return (1 - x / 2 + x ** 5 + y ** 3) * np.exp(-x ** 2 - y ** 2)


n = 256
x = np.linspace(-3, 3, n)
y = np.linspace(-3, 3, n)
X, Y = np.meshgrid(x, y)  # 把x, y mesh起来

# use plt.contourf to filling contour
# X, Y and value for (X, Y) point
plt.contourf(X, Y, f(X, Y), 8, alpha=0.75, cmap=plt.cm.hot)
# parameter:  8:分成10部分, 再如是0时，图像被分割成两部分   alpha:visibility
# cmap:颜色    plt.cm.hot/plt.cm.cool:热度图

# use plt.contour to add contour lines
C = plt.contour(X, Y, f(X, Y), 8, c='k', lw=0.5)
plt.clabel(C, inline=True, fontsize=10)

plt.show()
