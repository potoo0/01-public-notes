import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
labels:
    https://plotly.com/python/figure-labels/
'''

x = np.arange(1, 5, 0.01)
y = np.sin(x)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=x,
        y=y,
        mode='markers',
        hovertext=y,
        hovertemplate='x: %{x}, y: %{y}<br>date: %{hovertext}',
        name='实际值'
    ),
)

fig.add_trace(
    go.Scatter(
        x=x,
        y=y - 0.5,
    ),
)

fig.update_layout(
    title="Plot Title",
    xaxis_title="X Axis Title",
    yaxis_title="Y Axis Title",
    legend_title="Legend Title",
)

fig.show()
