import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker


x = np.arange(1, 15, 0.1)
y = np.sin(x)

# 为每个 y 的刻度加单位以及格式化
# plt.gca(): 返回当前 figure 的 axis 对象
plt.gca().yaxis.set_major_formatter(mticker.FormatStrFormatter('%.1f s'))

plt.plot(x, y)
plt.show()
