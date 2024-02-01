import matplotlib.pyplot as plt
import numpy as np

# 修改坐标轴范围，坐标轴描述 13-25
x = np.linspace(-3, 3, 50)
y1 = x ** 2
plt.plot(x, y1, color='red', linewidth=2)


# ax = plt.gca()  # 获取当前fig的axis属性
# ax.spines['right'].set_color('none')  # ax.spines坐标轴边框。让右边边框消失
# ax.spines['top'].set_color('none')

plt.show()
