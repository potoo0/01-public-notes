import numpy as np
import plotly.express as px

'''
px: https://plotly.com/python/plotly-express/
px.scatter: https://plotly.com/python/line-and-scatter/

line 使用 px.line 函数
scatter 使用 px.scatter 函数
'''

x = np.linspace(1, 10, 100)
y = np.sin(x)

fig = px.scatter(
    {'ts': x, 'sin': y},
    x='ts',
    y='sin',
    color="ts",
    size="ts"
)
# 输入数据必须是 dataframe 或者 字典；
# x, y, color, size 指定分别指定源数据的哪个列做数据


fig.update_layout(title='px_demo')  # 标题
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)  # 设置 y 的比例与 x 一致

fig.show()
