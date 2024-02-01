import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
style-line-plots:
  https://plotly.com/python/line-charts/#style-line-plots
'''

x = np.arange(1, 10, 0.1)
y1 = np.sin(x)
y2 = np.cos(x)

# 虚线 - px
fig = px.line(
    x=x, y=y1,
    title='dash',
    line_dash_sequence=['dash'],
)

# 虚线 - Scatter
fig.add_trace(
    go.Scatter(
        x=x,
        y=y2,
        mode='lines',
        name=f'Scatter dash',
        line=dict(
            color='blue',
            dash='dash',
        )
    )
)

fig.show()
