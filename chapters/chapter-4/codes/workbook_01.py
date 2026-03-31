import numpy as np
from scipy.interpolate import CubicSpline

rng = np.random.default_rng(42)
x = np.linspace(0, 6, 20)
y_true = np.sin(x)
y_noisy = y_true + 0.12 * rng.standard_normal(len(x))

# Interpolation through noisy points
spline = CubicSpline(x, y_noisy)

# Quadratic trend fit
coef = np.polyfit(x, y_noisy, deg=2)
