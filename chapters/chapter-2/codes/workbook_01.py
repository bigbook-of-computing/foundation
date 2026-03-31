import numpy as np

eps = np.finfo(np.float64).eps
print("Machine epsilon:", eps)
print("1 + eps > 1 ?", (1.0 + eps) > 1.0)
print("1 + eps/2 > 1 ?", (1.0 + eps / 2.0) > 1.0)
print("0.1 stored as:", format(np.float64(0.1), ".55f"))
