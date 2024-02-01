import numpy as np
import plotly.express as px
import plotly.graph_objects as go

'''
filled-area doc:
    https://plotly.com/python/filled-area-plots/
'''

x = np.arange(1, 5, 0.01)
y = np.sin(x)

fig = px.line(
    y=x, x=y,
    title='area color'
)

fig.add_trace(
    go.Scatter(
        y=x, x=y,
        fill='tozerox',
        # "tozeroy" | "tozerox" | "tonexty" | "tonextx" | "toself" | "tonext"
        fillcolor='rgba(237, 160, 150, 0.3)'
    )
)

fig.show()
