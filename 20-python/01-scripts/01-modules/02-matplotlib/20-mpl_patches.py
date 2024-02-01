import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches


ax = plt.axes()

for ii in range(3, 11):
    if ii == 4:
        ax.add_patch(patches.CirclePolygon((6, 10), 2.5))
    else:
        ax.add_patch(patches.RegularPolygon((ii * 2, ii * 2), ii, 1))

plt.xlim([0, 30]); plt.ylim([0, 30]);
plt.show()
