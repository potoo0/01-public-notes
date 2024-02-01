import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# 分格绘图

# method3: easy to define structure.推荐
plt.figure(num=3)
f, ((ax11, ax12), (ax12, ax22)) = plt.subplots(2, 2, sharex=True, sharey=True)
ax11.scatter([1, 2], [1, 2])


# method 1: subplot2grid
plt.figure(num=1)
ax_p2g_1 = plt.subplot2grid((3, 3), (0, 0), colspan=3)
# parameter: (3, 3):分割成三行三列,(0, 0):ax_p2g_1的位置。rowspan/colspan:行/列跨度.默认是1
ax_p2g_1.plot([1, 2], [1, 2])
ax_p2g_1.set_title('ax1_title')
# ax_p2g_1.set_xlim()  # ax_p2g_1.set_xlabel()
ax_p2g_2 = plt.subplot2grid((3, 3), (1, 0), colspan=2)
ax_p2g_3 = plt.subplot2grid((3, 3), (1, 2), rowspan=2)
ax_p2g_4 = plt.subplot2grid((3, 3), (2, 0))
ax_p2g_5 = plt.subplot2grid((3, 3), (2, 1))
ax_p2g_5.plot([1, 2], [1, 2])
ax_p2g_5.set_title('ax5_title')


# method2: gridspec
plt.figure(num=2)
gs = gridspec.GridSpec(3, 3)
ax_gs_1 = plt.subplot(gs[0, :])  # 第1行开始到结束都是ax_gs_1
ax_gs_2 = plt.subplot(gs[1, :2])  # 第2行开始到第3列
ax_gs_3 = plt.subplot(gs[1:, 2])  # 第2行第3列开始到最后一行
ax_gs_4 = plt.subplot(gs[2, 0])  # 第3行第1列
ax_gs_5 = plt.subplot(gs[2, 1])  # 第3行第2列


plt.show()
