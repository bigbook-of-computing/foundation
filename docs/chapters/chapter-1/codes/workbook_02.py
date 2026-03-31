import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi, 200)
y = np.sin(x)

plt.figure(figsize=(8, 4))
plt.plot(x, y, linewidth=2)
plt.title("Chapter 1 Lab: sin(x)")
plt.xlabel("x (radians)")
plt.ylabel("sin(x)")
plt.grid(True)
plt.show()
