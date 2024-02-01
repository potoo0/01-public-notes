import numpy as np
import plotly.graph_objects as go

'''
go: https://plotly.com/python/

line 和 scatter 都使用 gp.Scatter 类

颜色:
https://plotly.com/python/builtin-colorscales/
'''

x = np.linspace(1, 10, 100)
y = np.sin(x)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x, y=y,
        mode='markers+lines',
        name='demo',  # trace name
        marker=dict(
            size=x,
            color=x,
            colorscale='sunset'
        ),
        line=dict(
            color='green',
            width=4
            # colorscale='sunset'  # 不识别此参数？？？
        ),
        # mode 可以选择 markers 还是 lines，或者同时
        # marker/line 可以设置 marker/line 颜色等等，值可以为:
        #     1.单值;
        #     2.(line不可) 等长的序列，对于颜色可以设置渐变规则，规则有: px.colors.named_colorscales()
    )
)
# marker
'''
all markers:
from plotly.validators.scatter.marker import SymbolValidator
raw_symbols = SymbolValidator().values

marker=dict(
    symbol='x',
    color='red',
    size=10
),
'''
fig.update_layout(title='go_demo')  # 标题
fig.update_yaxes(
    scaleanchor="x",
    scaleratio=1,
)  # 设置 y 的比例与 x 一致

fig.show()
