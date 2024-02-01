import matplotlib.pyplot as plt
import numpy as np

# 次坐标轴
x = np.arange(0, 10, .1)
y1 = 0.05 * x ** 2
y2 = -1 * y1

fig, ax1 = plt.subplots()
ax2 = ax1.twinx()  # ax2原点对称与ax1
ax1.plot(x, y1, 'g-')
ax2.plot(x, y2, 'b--')

ax1.set_xlabel('x_data')
ax1.set_ylabel('y1', color='g')
ax2.set_ylabel('y1', color='b')

plt.show()
