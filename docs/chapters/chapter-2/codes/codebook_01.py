import numpy as np

print("=== Chapter 2 Baseline ===")
print("float64 epsilon:", np.finfo(np.float64).eps)
print("0.1 as stored:", format(np.float64(0.1), ".55f"))
print("0.1 + 0.2:", np.float64(0.1) + np.float64(0.2))
print("0.3:", np.float64(0.3))
print("equality check:", (np.float64(0.1) + np.float64(0.2)) == np.float64(0.3))
