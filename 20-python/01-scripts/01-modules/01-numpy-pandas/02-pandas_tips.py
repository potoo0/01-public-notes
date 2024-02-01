import numpy as np
import pandas as pd
from datetime import datetime

# 0. 设置
# #0.1 绘图
# pd.options.plotting.backend = 'matplotlib'  # matplotlib
# pd.options.plotting.backend = "plotly"  # plotly


# 1. 生成 df
row = 5
df_org = pd.DataFrame({
    'ts': pd.date_range(end='2020-11-30', periods=row, freq='D'),
    'data': np.linspace(1, 10, row)
})

print(f'\n原始:\n{df_org}')


# 2. 索引与普通列转换
# #索引变成普通列，并设置新索引为 RangeIndex
df = df_org.copy()
df.reset_index(inplace=True)
# #普通列变索引
df.set_index('ts', inplace=True)

print(f'\n索引-列转换:\n{df}')


# 3. 更改列名
# # 3.1 普通列
# rename 可以传字典, 函数
df = df_org.copy()
df.rename(columns={'data': 'data_y'}, inplace=True)
df.rename(columns=str.title, inplace=True)
# df.columns = [xxxx, xxx, ...]  # 更改所有列名
# # 3.2 索引列
# df.index.name 属性只能在单一索引是使用
df.index.name = 'Idx'
df.rename_axis('a', inplace=True)
# df.rename_axis(('a', 'b'), inplace=True)
print(f'\n索引列和普通列改名:\n{df}')


# 4. 列筛选
# cols = df.columns
df = df_org.copy()
cols = ['data']
X = df.drop(cols, axis=1)  # axis=1: 操作整列
y = df.filter(cols, axis=1)  # axis=1: 操作整列

print(f'\n列筛选:\n{X=}\n{y=}')


# 5. 行去重
'''
>>> %timeit df3[~df3.index.duplicated(keep='first')]
1000 loops, best of 3: 307 µs per loop

>>> %timeit df3.groupby(df3.index).first()
1000 loops, best of 3: 580 µs per loop

>>> %timeit df3.reset_index().drop_duplicates(subset='index', keep='first').set_index('index')
1000 loops, best of 3: 1.54 ms per loop
'''

# 6. 整列/行操作
'''
           DataFrame    Series
apply         Y            Y
map           -            Y
applymap      Y            -

apply 支持指定 axis，但是不支持 Index 列的操作
    axis=1: 每次取一行
    axis=0: 每次取一列
Index 只可用 map
'''
df = df_org.copy()
df.set_index('ts', inplace=True)
print('org:\n', df)
print('apply axis=1 sum:\n', df.apply(lambda row: row.sum(), axis=1))
print('map demo:\n', df['data'].map(lambda x: x * 10))
print('applymap:\n', df.applymap(np.square))
# apply and convert to list by row: List[Tuple]
print('apply and convert to list by row')
rowList1 = df.apply(lambda row: (row['data'] * 10, row['data']), axis=1, result_type='reduce').to_list()
print('List[Tuple]', rowList1)
# apply and convert to list by row: List[Dict]
rowList2 = df.to_dict(orient='records')
print('List[Dict]', rowList2)

# iter
# `itertuples` 快于 `iterrows`, 但前者返回值是 namedtuple 故只能通过 `.` 来访问值(_asdict() 可转为 dict)。
# 二者都是原 df 的拷贝，修改值可通过 `df.at[row.Index, 'col'] = val`。`at` 快于 `loc`。
for idx, row in df.iterrows(): ...
for row in df.itertuples(): ...
for name, group in df.groupby('data'): ...

# 6. read csv
'''
原数据有列名:
- header=0,  # head 信息所在的行号
- parse_dates=[0],  # 要转换为 datetime 对象的列号
- infer_datetime_format=True,  # parse_dates 启用时，此参数启用后会加速转换 datetime
- index_col=[0],  # index 所在列号
- 列分隔(下面三个参数只可指定一个):
    - sep: 可以写正则，如 '\s+', 匹配任意空白字符;
    - delimiter: 等效于 sep;
    - delim_whitespace=True: 相当于 sep='\s+'

原数据无列名:
df = pd.read_csv(
    fullpath,
    header=None,
    names=columnNames
)
'''


# 7. 列类型转换
df_coltype = pd.DataFrame(
    data={'a': map(str, range(1, 10))},
    index=map(str, range(1, 10))
)
# 查看类型: df_coltype.dtypes
print(f'原类型:\n{df_coltype.dtypes}')
# 转化为 int, 方法一: astype 对某列，即 Series
df_coltype['a'] = df_coltype['a'].astype('int32')
# 方法一: astype 方法也可以对 df 操作
#     传入指定列对某列否则对整个 df (不会操作 index)
df_coltype = df_coltype.astype({'a': 'int16'})
print(f'修改后类型:\n{df_coltype.dtypes}')

# 8. 数据选择
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#selecting-random-samples


# 9. 时间索引重采样 - asfreq/resample
# asfreq: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.asfreq.html
# resample: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.resample.html
# asfreq: 向上采样（时间刻度更精细），补充缺失值 pad 等；向上采样不支持求和等。
# resample: 向下采样（时间刻度更大）: sum 求和等；向上采样，补充缺失值 pad 等。
# 补充缺失值方法: ‘backfill’/’bfill’, ‘pad’/’ffill’
num = 30
index = pd.date_range('1/1/2020', periods=num, freq='H')
df = pd.DataFrame(
    data={'d': range(num)},
    index=index
)
df.asfreq('T', method='pad')
df.resample('D').sum()
df.resample('T').pad()


# 9. 添加多个列
df = pd.DataFrame({'d': range(10)})
ex_col = {
    'region': 'A',
    'netflow_directions': 'out',
    'op_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
}

df = df.assign(**ex_col)


# 10. groupby
x = [1, 1, 1, 2, 2, 3]
df = pd.DataFrame(
    data={'x': x, 'y': np.arange(len(x))}
)
df.groupby('x').apply(lambda inner: print(inner))
# groupby collect to set in new df
df.groupby(by='x').apply(lambda inner: set(inner.y.values)).to_frame()
# groupby caculate max to new df
#  按 c,d 分组, 然后求 a, b 的最大值的和
df = pd.DataFrame({"a": range(2, 5), "b": range(5, 8), "c": [1, 2, 1], "d": [1, 1, 1]})
dd = df.groupby(by=["c", "d"]).apply(lambda df: df.b.max() + df.a.max()).to_frame().reset_index()


# 11. multiIndex
# 11.1 column set to index
df = pd.DataFrame({
    'idx1': ['a', 'a', 'a'],
    'idx2': ['aa', 'ab', 'aa'],
    'val': [4, 5, 6]
})
df.set_index(['idx1', 'idx2'], inplace=True)

# 11.2 column name append to index
df = pd.DataFrame(
    data=np.arange(12).reshape(4, 3)
)
colname_multiidx = df.unstack().to_frame().sort_index(level=1)

# 12. multiindex - one column value append to index
# 此方法可以导出 (x_coor, y_coor, values) 点对
colval_multiidx = colname_multiidx.set_index(0, append=True)

# 12.1 multiindex operation
# 删除 0 level 的 index, level序号可通过查看 df.index 的顺序确定
colname_multiidx.droplevel(0)
# rename
# https://pandas-docs.github.io/pandas-docs-travis/user_guide/advanced.html#renaming-names-of-an-index-or-multiindex

# 13. 数据分组频次统计
df = pd.DataFrame(
    data={'y': np.random.randint(1, 20, size=10)}
)
group_step = np.arange(df['y'].min() - 1, df['y'].max() + 1, 5)
group = pd.cut(df['y'], group_step)  # 分组
group_freq = group.value_counts()

# 14. Nan 计数
df.isnull().sum().sum()

# 15. 合并 dataframe
# 1. join: 左右
#   - on: df 的列名, 此列名用来 join df2 的 index, 默认取 df 的 index
#   - how: {'left', 'right', 'outer', 'inner'}, default 'left'
#   - lsuffix/rsuffix: df/df2 列名前缀
# 2. merge: 左右
#   - how: {'left', 'right', 'outer', 'inner'}, default 'inner'
#   - on: 合并时基准字段名, 默认取两个 df 的交集字段
# 3. concat: 左右/上下
#   - axis: 0/index: 上下合并, 1/columns: 左右合并, 默认 0
#   - join: {'inner', 'outer'}, default 'outer'
#   - ignore_index: 忽略索引, 即合并后重建索引为 range(0, len)
#   - name: 合并时基准字段名
# 4. append: 上下
#   - ignore_index: 忽略索引, 即合并后重建索引为 range(0, len)

# x. 解决 concat, merge, join 数据类型的变化
joined = df.join(df2, how='outer').fillna(-1).astype(pd.concat([df.dtypes, df2.dtypes]))

# 16. SettingWithCopyWarning
# 在使用 loc，以及 iloc 后不推荐再链式修改某值
#   不推荐的操作:
df = pd.DataFrame(
    data={'a': [1, 2, 3], 'b': [4, 5, 6]},
)
# 不推荐
tmp = df.iloc[:, 1]
tmp[0] = 10
# ...
