import time
import threading
import matplotlib.pyplot as plt


def close(tim):
    time.sleep(tim)
    plt.close()


thread1 = threading.Thread(target=close, args=(3,))

thread1.start()
plt.plot(range(10))
plt.show()
