import matplotlib.pyplot as plt
import numpy as np

# 绘制柱状图 11-22
n = 12  # 柱状图数量
x = np.arange(n)
# uniform distribution：均匀分布
y1 = (1 - x / float(n)) * np.random.uniform(0.5, 1.0, n)
y2 = (1 - x / float(n)) * np.random.uniform(0.5, 1.0, n)

plt.bar(x, +y1, facecolor='#9999ff', edgecolor='white')
plt.bar(x, -y2, facecolor='#ff9999', edgecolor='white')

for x0, y0 in zip(x, y1):
    # zip函数此处功能是使for每次输出两个值
    # ha: horizontal alignment  水平对齐方式
    # va: vertical alignment  竖直对齐方式
    plt.text(x0 + 0.4, y0 + 0.05, '%.2f' % y0, ha='center', va='bottom')

for x0, y0 in zip(x, y2):
    plt.text(x0 + 0.4, -y0 - 0.05, '-%.2f' % y0, ha='center', va='top')

plt.xlim((-0.5, n))
plt.ylim((-1.25, 1.25))
plt.xticks(())  # 设置x坐标轴无
plt.yticks(())  # 设置y坐标轴无

plt.show()
