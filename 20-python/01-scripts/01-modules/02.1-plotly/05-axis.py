import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
layout-axis doc:
    https://plotly.com/python/reference/layout/yaxis/#layout-yaxis-tickformat

update_layout(<x,y>axis_xxx) == update_<x,y>axes(xxx)
eg: update_layout(yaxis_tickformat='>0.1f')
    == update_yaxes(tickformat='>0.1f')
'''

x = np.arange(1, 10, 0.1)
y = np.linspace(1e6, 2e6, num=len(x))

fig = px.line(x=x, y=y)

# tick format: >: 右对齐，0.1f: 一位小数
fig.update_yaxes(tickformat='>0.1f')

fig.update_xaxes(
    range=(-3, 13),
    tickmode='array',
    tickvals=list(range(1, 10)),
    ticktext=list(map(lambda v: str(v) + 's', range(1, 10)))
)
# tickmode: array 以手动设置 tick
# tickvals: 选定的 tick 位置
# ticktext: tickvals 的位置放置的文字


fig.show()
