import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

'''
scatter:
  https://plotly.com/python/reference/scatter/
'''

df = pd.DataFrame({
    'pos_x': [1, 2, 3],
    'pos_y': [5, 4, 3],
    'text': ['a', 'b', 'c']})

# px
fig = px.line(df, x="pos_x", y="pos_y", text="text")
fig.update_traces(textposition="bottom right")

# go
fig.add_trace(
    go.Scatter(
        x=df['pos_x'] + 5,
        y=df['pos_y'],
        mode='markers+text',
        text=df['text'],
        textposition="bottom right"
    )
)


fig.show()
