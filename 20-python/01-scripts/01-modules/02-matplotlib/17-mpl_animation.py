import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation


# 动画
fig, ax = plt.subplots()
x = np.arange(0, 2 * np.pi, 0.01)
line, = ax.plot(x, np.sin(x))
# ax.plot(x, np.sin(x))返回一个列表，列表的第一个是line


def animate(i):
    line.set_ydata(np.sin(x + i / 100))
    return line,


def init():
    line.set_ydata(np.sin(x))
    return line,


ani = animation.FuncAnimation(fig=fig, func=animate,  # 动画方程
                              frames=100,  # 帧数=100
                              init_func=init,  # 起始函数
                              interval=20,  # 频率：20ms
                              blit=True)  # 只更新变化的点：是

plt.show()
