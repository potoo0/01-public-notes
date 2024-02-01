import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection


n = 10
x = np.arange(0, n, step=.5)
y = x ** 2

# y 的值归一化到[0, 1]
# 因为 y 大到一定程度超过临界数值后颜色就会饱和不变(不使用循环colormap)。
norm = plt.Normalize(y.min(), y.max())
# matplotlib.colors.Normalize 对象，可以作为参数传入到绘图方法里
# 也可给其传入数值直接计算归一化的结果
norm_y = norm(y)

# ## 1. 散点图颜色渐变
# `plt.scatter` 可以接收参数 `c` , `c` 是一维的数值(与坐标点数量相同), 它会将这单个的数值映射成 rgb 色彩值.
# 官方例子: [scatter demo](https://matplotlib.org/gallery/lines_bars_and_markers/scatter_custom_symbol.html#sphx-glr-gallery-lines-bars-and-markers-scatter-custom-symbol-py)  
plt.scatter(x, y, c=norm_y, cmap='viridis')


# ## 2. 条形图颜色渐变与colormap
# `plt.bar` 的参数 `color` 可以接收一组颜色，用于给每个柱子上色。所以实现颜色渐变只需要将当前的纵坐标值映射成 rgb 颜色  
# 使用 `cm(colormap)` 可以完成单值到 rgb 的映射。具体做法是 `cm.get_cmap()` 拿到想要的 colormap，然后给其传入数值就会返回 rgb。  
# 可用的 colormap 以及方法见官方文档 [colormaps](https://matplotlib.org/tutorials/colors/colormaps.html)
map_vir = cm.get_cmap(name='viridis')
# name 参数用来选择使用哪个 colormap, 可选的见上面官方链接
# lut 参数推荐不要设置。是用来定义生成的 colormap 的长度也就是 map_vir 的长度
# 如果 colormap 的长度小于绘图坐标 y 的长度，那程序就会将多个 y 的颜色设置成一样。
color = map_vir(norm_y)

ax = plt.bar(x, y, color=color)

# ## 3. 线条图颜色渐变
# `plt.plot` 的参数 `color` 只能接收 rgb 色彩值，且接收的的颜色是整条线的颜色，要实现线条上的颜色渐变不能使用 `plot`，使用[LineCollection](https://matplotlib.org/api/collections_api.html#matplotlib.collections.LineCollection), 此方法较难，详见官方文档。 
# 官方例子: [plot multicolored_line](https://matplotlib.org/gallery/lines_bars_and_markers/multicolored_line.html#sphx-glr-gallery-lines-bars-and-markers-multicolored-line-py)
points = np.array([x, y]).T.reshape(-1, 1, 2)
segments = np.concatenate([points[:-1], points[1:]], axis=1)

fig, axs = plt.subplots()

lc = LineCollection(segments, cmap='viridis')
# Set the values used for colormapping
lc.set_array(norm_y)
line = axs.add_collection(lc)

axs.set_xlim(x.min(), x.max())
axs.set_ylim(y.min() - 1, y.max() + 1)

plt.show()
