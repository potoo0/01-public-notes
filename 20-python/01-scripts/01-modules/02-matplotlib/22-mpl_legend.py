import numpy as np
import matplotlib.pyplot as plt
epochs = 2


def plot_history(his):
    handles = []
    x = np.arange(1, epochs + 1)
    fig, ax = plt.subplots()
    ax.set_xticks(x)
    handles.append(ax.plot(x, his['accuracy'], label='accuracy'))
    handles.append(ax.plot(x, his['loss'], label='loss'))
    handles.append(ax.plot(x, his['val_accuracy'], label='val_accuracy'))
    handles.append(ax.plot(x, his['val_loss'], label='val_loss'))
    fig.legend()
    plt.show()


history = {
    'accuracy': [0.13, 0.222],
    'loss': [2.7692117824554443, 2.366209884643555],
    'val_accuracy': [0.1694, 0.2568],
    'val_loss': [2.5003876701185974, 2.18240043483203]
}

plot_history(history)
