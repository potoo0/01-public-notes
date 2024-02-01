import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
bar api: https://plotly.com/python/reference/#bar
'''

fig = go.Figure(
    go.Bar(
        x=[20, 14, 23],
        y=['giraffes', 'orangutans', 'monkeys'],
        orientation='h',
    )
)

fig.update_layout(
    xaxis=dict(autorange="reversed"),
)

fig.show()
