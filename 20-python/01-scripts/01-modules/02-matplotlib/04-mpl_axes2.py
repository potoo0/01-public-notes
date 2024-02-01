import matplotlib.pyplot as plt
import numpy as np

# 修改坐标轴的位置。27-35
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

# gca = 'get current axis'
ax = plt.gca()  # 获取当前fig的axis属性
ax.spines['right'].set_color('none')  # ax.spines坐标轴边框。让右边边框消失
ax.spines['top'].set_color('none')
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
ax.xaxis.set_ticks_position('bottom')  # 设置ax的xaxis为下面的坐标轴
ax.yaxis.set_ticks_position('left')  # 设置ax的yaxis为左边的坐标轴
# 新axis定位方式是使用data。还有其他定位方法，axes, outward。axis：定位到axis的百分之几
ax.spines['bottom'].set_position(('data', 0))  # 设置下面的axis位置是数据的yaxis的0处
ax.spines['left'].set_position(('data', 0))  # 设置左边的axis位置是数据的xaxis的0处

plt.show()
