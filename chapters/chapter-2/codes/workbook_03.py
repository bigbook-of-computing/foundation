import numpy as np

x = np.float64(1e8)
deltas = np.logspace(-2, -12, 11)

for d in deltas:
    computed = (x + d) - x
    rel_err = abs(computed - d) / d
    print(f"delta={d:.1e} computed={computed:.1e} rel_err={rel_err:.2e}")
