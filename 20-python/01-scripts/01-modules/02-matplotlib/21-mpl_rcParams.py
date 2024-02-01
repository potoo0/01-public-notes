# import numpy as np
# import matplotlib
import matplotlib.pyplot as plt

# plt.rcParamsDefault  # 查看所有默认参数
plt.rcParams['xtick.labelbottom'] = False
plt.rcParams['ytick.labelleft'] = False
plt.rcParams['figure.subplot.top'] = 0.7
plt.rcParams['figure.subplot.wspace'] = 0.3
plt.rcParams['figure.subplot.hspace'] = 0.6

plt.ion()

plt.plot(1, 1)

plt.ioff()
plt.show()
