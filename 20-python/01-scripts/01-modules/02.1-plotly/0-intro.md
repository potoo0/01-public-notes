官方 demo: [Plotly Python Open Source Graphing Library](https://plotly.com/python/)

ployly 创建 figure:
  - `plotly.graph_objects`: 相对 express 底层一点，返回 figure, 由源码可知 graph_objects 相当于 graph_objs 的别名；
  - `plotly.express`: 相对更高级，画图更快捷，但 api 有限，其返回也是 figure。官方文档 [Plotly Express in Python](https://plotly.com/python/plotly-express/)

绘制:

- `plotly.graph_objects` 初始化时通过 *data* 直接传入坐标轴对象；
- `figure.add_trace`  传入坐标轴对象。

