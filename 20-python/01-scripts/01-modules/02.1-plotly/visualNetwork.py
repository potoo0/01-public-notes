import networkx as nx
import plotly.graph_objects as go


class visualNetwork(object):
    """plotly 可视化 network.
    Usage: visualNetwork(G, arrow=False)()
    """

    def __init__(self, G: nx.classes.graph.Graph, arrow=False):
        self.G = G
        self.arrow = arrow
        # 生成节点坐标数据
        self.pos = nx.spring_layout(self.G)
        # 箭头数据
        self.annotations = []
        # trace 数据
        self.traces = [
            self.initEdgeTrace(),
            self.initNodeTrace(),
        ]

    def initEdgeTrace(self):
        # 线条
        edge_x = []
        edge_y = []
        for edge in self.G.edges():
            x0, y0 = self.pos[edge[0]]
            x1, y1 = self.pos[edge[1]]
            edge_x += x0, x1, None
            edge_y += y0, y1, None
            # 如果需要画箭头，则生成
            if self.arrow:
                self.annotations.append(
                    dict(
                        ax=self.pos[edge[0]][0],
                        ay=self.pos[edge[0]][1],
                        axref="x",
                        ayref="y",
                        x=self.pos[edge[1]][0],
                        y=self.pos[edge[1]][1],
                        xref="x",
                        yref="y",
                        showarrow=True,
                        arrowhead=3,
                        arrowsize=2,
                    )
                )

        edge_trace = go.Scatter(
            x=edge_x,
            y=edge_y,
            line=dict(width=0.5, color="#888"),
            hoverinfo="none",
            mode="lines",
        )

        return edge_trace

    def initNodeTrace(self):
        # 节点
        node_x = []
        node_y = []
        for node in self.G.nodes():
            x, y = self.pos[node]
            node_x.append(x)
            node_y.append(y)

        node_trace = go.Scatter(
            x=node_x,
            y=node_y,
            mode="markers+text",
            hoverinfo="text",
            text=list(self.G.nodes()),
            textposition="bottom center",
            marker=dict(
                showscale=True,
                colorscale="YlGnBu",
                color=[],
                reversescale=True,
                size=10,
                colorbar=dict(
                    thickness=15,
                    title="Node Connections",
                    xanchor="left",
                    titleside="right",
                ),
                line_width=2,
            ),
        )

        # 生成节点文字(邻接数)
        node_adjacencies = []
        node_text = []
        for idx, adjacencies in enumerate(self.G.adjacency()):
            node_adjacencies.append(len(adjacencies[1]))
            node_text.append(
                f"node: {adjacencies[0]}, con: {len(adjacencies[1])}")

        node_trace.marker.color = node_adjacencies
        node_trace.text = node_text

        return node_trace

    def show(self):
        fig = go.Figure(
            data=self.traces,
            layout=go.Layout(
                title="<br>Network graph with Plotly",
                titlefont_size=16,
                width=500,
                height=500,
                annotations=self.annotations,
                showlegend=False,
                hovermode="closest",
                xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                yaxis=dict(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False,
                    scaleanchor="x",
                    scaleratio=1,
                ),
            ),
        )

        fig.show()

    def __call__(self):
        self.show()
