import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
bar api: https://plotly.com/python/reference/#bar
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

fig.show()
