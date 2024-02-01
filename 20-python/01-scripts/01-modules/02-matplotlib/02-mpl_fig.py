import matplotlib.pyplot as plt
import numpy as np

# 新建多个figure。并在一个figure中显示多个内容 9-14
x = np.linspace(-1, 1, 50)
y1 = x ** 2
y2 = 2 * x + 1

plt.figure()
plt.plot(x, y1)

plt.figure(num=3, figsize=(6, 4))
plt.plot(x, y2)
plt.plot(x, y1, color='red', linewidth=10.0, linestyle='--')

plt.show()
