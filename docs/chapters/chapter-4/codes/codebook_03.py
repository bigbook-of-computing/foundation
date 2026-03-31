from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-4/codes")
codes_dir.mkdir(parents=True, exist_ok=True)


def runge(x):
    return 1.0 / (1.0 + 25.0 * x * x)

x_dense = np.linspace(-1.0, 1.0, 1200)
y_dense = runge(x_dense)

# Uniform-node interpolation (high-degree)
n = 16
x_uni = np.linspace(-1.0, 1.0, n)
y_uni = runge(x_uni)
coef_uni = np.polyfit(x_uni, y_uni, deg=n - 1)
y_uni_interp = np.polyval(coef_uni, x_dense)

# Chebyshev-like nodes
k = np.arange(n)
x_cheb = np.cos((2 * k + 1) * np.pi / (2 * n))
x_cheb = np.sort(x_cheb)
y_cheb = runge(x_cheb)
coef_cheb = np.polyfit(x_cheb, y_cheb, deg=n - 1)
y_cheb_interp = np.polyval(coef_cheb, x_dense)

fig, ax = plt.subplots(figsize=(8.4, 5.0))
ax.plot(x_dense, y_dense, color="black", linewidth=2.0, label="true Runge function")
ax.plot(x_dense, y_uni_interp, color="tab:red", linewidth=1.7, label="uniform-node interpolation")
ax.plot(x_dense, y_cheb_interp, color="tab:blue", linewidth=1.7, label="chebyshev-node interpolation")
ax.scatter(x_uni, y_uni, color="tab:red", s=16, alpha=0.6)
ax.scatter(x_cheb, y_cheb, color="tab:blue", s=16, alpha=0.6)

ax.set_ylim(-0.6, 1.4)
ax.set_title("Chapter 4: Runge Phenomenon and Node Choice")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.grid(True, alpha=0.3)
ax.legend(loc="upper center")

out_file = codes_dir / "ch4_runge_phenomenon.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

max_err_uni = float(np.max(np.abs(y_uni_interp - y_dense)))
max_err_cheb = float(np.max(np.abs(y_cheb_interp - y_dense)))

print(f"Saved figure to: {out_file}")
print("max error (uniform nodes):", max_err_uni)
print("max error (chebyshev nodes):", max_err_cheb)
