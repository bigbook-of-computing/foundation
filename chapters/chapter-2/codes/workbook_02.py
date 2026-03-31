import numpy as np

values = [1.0, 1e3, 1e8, 1e12, 1e16]
for x in values:
    next_x = np.nextafter(x, np.inf)
    abs_gap = next_x - x
    rel_gap = abs_gap / x
    print(f"x={x:>10.1e} abs_gap={abs_gap:>10.3e} rel_gap={rel_gap:>10.3e}")
