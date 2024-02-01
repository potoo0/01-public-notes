import numpy as np
import matplotlib.pyplot as plt

# generate some data
data = np.random.normal(size=100)

# define the plot
fig, ax = plt.subplots()

# plot the data as a histogram
ax.hist(data, orientation=u'horizontal')

# invert the order of x-axis values
ax.set_xlim(ax.get_xlim()[::-1])

# move ticks to the right
ax.yaxis.tick_right()

plt.show()
