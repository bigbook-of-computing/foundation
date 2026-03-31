import numpy as np
import matplotlib.pyplot as plt

def plot_function(f, x_min, x_max):
    x = np.linspace(x_min, x_max, 1000)
    y = f(x)
    plt.plot(x, y)
    plt.grid(True)
    plt.show()
