import numpy as np

# 1. ravel vs flatten:
# 功能: 将多维数组降位一维
# 区别: flatten 返回拷贝，修改不会影响原数据
#       ravel 返回的是视图，修改会影响原数据

# 2. where
X = np.arange(1, 10).reshape(-1, 1)  # n x 1
# where 用法 1: 取满足条件的数据的索引
# condi = np.where(X < 5)
condi = np.where((X > 2) & (X < 5))
print(X[condi[0], condi[1]])

print(np.c_[condi[0], condi[1]])

# where 用法 2: 替换条件之外的值
res = np.arange(-5, 10)
feature_range = (0, 1)
res = np.where(res >= feature_range[0], res, feature_range[0])
print(res)

# 3. 矩阵合并
# np.c_[a, b]: 合并 a, b
# np.r_[a, b]:
# np.vstack(): 等于 np.c_
# np.hstack(): 等于 np.r_
# np.concatenate():

a = np.array([1, 2])
b = np.array([3, 4])
print(np.c_[a, b])
print(np.r_[a, b])
