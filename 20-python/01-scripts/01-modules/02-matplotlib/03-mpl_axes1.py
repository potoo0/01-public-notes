import matplotlib.pyplot as plt
import numpy as np

# 修改坐标轴范围，坐标轴描述 13-25
x = np.linspace(-3, 3, 50)
y1 = x ** 2
y2 = 2 * x + 1

plt.figure(figsize=(6, 4))
plt.plot(x, y2)
plt.plot(x, y1, color='red', linewidth=1.0, linestyle='--')

plt.xlim(-1, 2)
plt.ylim(-2, 3)
plt.xlabel('I"m x')
plt.ylabel('I"m y')

new_ticks = np.linspace(-1, 2, 5)
print(new_ticks)
plt.xticks(new_ticks)
plt.yticks([-2, -1.8, -1, 1.22, 3, ],   # ticks的位置
           [r'$really\ bad$', r'$bad$', r'$normal$',
            r'$good\ \alpha$', r'$really\ good$'])  # ticks内容
# 在输出到屏幕中字体设置成数学形式方法：内容前后加$，注意空格需要加转义符号\
# 比如alpha的显示

plt.show()
