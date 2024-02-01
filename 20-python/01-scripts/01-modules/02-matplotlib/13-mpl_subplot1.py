import matplotlib.pyplot as plt

# 分格绘图
plt.figure(num=1)

plt.subplot(2, 2, 1)
plt.plot([0, 1], [0, 1])

plt.subplot(222)
plt.plot([0, 1], [0, 2])

plt.subplot(223)
plt.plot([0, 1], [0, 3])

plt.subplot(224)
plt.plot([0, 1], [0, 4])


# figure(2) 两行，第一行放一个图，第二行三个图
plt.figure(num=2)

plt.subplot(211)
plt.plot([0, 1], [0, 1])

plt.subplot(234)
plt.plot([0, 1], [0, 2])

plt.subplot(235)
plt.plot([0, 1], [0, 3])

plt.subplot(236)
plt.plot([0, 1], [0, 4])

plt.show()
