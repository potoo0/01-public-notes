import matplotlib.pyplot as plt
import numpy as np

# 标注。47-68
x = np.linspace(-3, 3, 50)
# y1 = x ** 2
y2 = 2 * x + 1

plt.figure(figsize=(6, 4))
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
ax.xaxis.set_ticks_position('bottom')  # 设置ax的xaxis为下面的坐标轴
ax.yaxis.set_ticks_position('left')  # 设置ax的yaxis为左边的坐标轴
# 新axis定位方式是使用data。还有其他定位方法，axes, outward。axis：定位到axis的百分之几
ax.spines['bottom'].set_position(('data', 0))  # 设置下面的axis位置是数据的yaxis的0处
ax.spines['left'].set_position(('data', 0))  # 设置左边的axis位置是数据的xaxis的0处


# plt.plot(x, y1, label='up')
plt.plot(x, y2, color='red', linewidth=1.0, linestyle='--', label='down')
plt.legend()
'''
# l1, = plt.plot(x, y1, label='up')
# l2, = plt.plot(x, y2, color='red',
                 linewidth=1.0, linestyle='--', label='down')
# plt.legend(handles=[l1, l2, ], labels=['aa', 'bb'], loc='best')
# handles: 由plt.plot返回的对象，在接收这个对象的变量后要加逗号！！！
# labels: 需要显示的图例
# loc: 'upper/lower right/left',  或者自动选择最好的位置：best。推荐
'''
x0 = 0.5
y0 = 2 * x0 + 1  # 需要标注的点
plt.scatter(x0, y0, s=50, color='b')  # 在图像上画出需要标记的点   plt.scatter:画散点图
plt.plot([x0, x0], [y0, 0],  # 画出虚线
         'k--',  # 曲线参数。'k'：黑色, '--'：虚线
         lw=2.5)  # 线宽2.5

# method 1
plt.annotate(r'$2x+1=%s$' % y0,  # 显示的内容
             xy=(x0, y0),  # annotate指向的点
             xycoords='data',  # 上面的xy以data为基准
             xytext=(+30, -30),  # annotate内容的位置，以x0,y0偏移(+30, -30)
             textcoords='offset points',  # 内容位置的定位方式：标注点偏移
             fontsize=16,
             arrowprops=dict(arrowstyle='->',  # 箭头类型
                             connectionstyle='arc3, rad=0.3')  # 弧线，角度2
             )

# method 2
plt.text(-1, 2.5,   # 标注内容的位置
         r'$ this\ is\ the\ text.\ \mu\ \sigma_i\ \alpha_t$',
         fontdict={'size': 16, 'color': 'r'})


plt.show()
