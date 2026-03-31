from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import CubicSpline

codes_dir = Path("docs/chapters/chapter-4/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(123)
x = np.linspace(0.0, 6.0, 25)
y_true = np.sin(x)
y_noisy = y_true + 0.12 * rng.standard_normal(len(x))

x_dense = np.linspace(x.min(), x.max(), 500)

# Interpolation through all noisy points
spline = CubicSpline(x, y_noisy)
y_spline = spline(x_dense)

# Quadratic least-squares trend
coef2 = np.polyfit(x, y_noisy, deg=2)
y_fit2 = np.polyval(coef2, x_dense)

fig, ax = plt.subplots(figsize=(8.4, 5.0))
ax.plot(x_dense, np.sin(x_dense), linestyle="--", color="black", linewidth=1.5, label="true sin(x)")
ax.scatter(x, y_noisy, color="tab:blue", s=20, alpha=0.75, label="noisy samples")
ax.plot(x_dense, y_spline, color="tab:orange", linewidth=2.0, label="cubic spline interpolation")
ax.plot(x_dense, y_fit2, color="tab:green", linewidth=2.0, label="quadratic least-squares fit")

ax.set_title("Chapter 4: Interpolation vs Trend Fitting")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.grid(True, alpha=0.3)
ax.legend()

out_file = codes_dir / "ch4_interpolation_comparison.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
