# **Chapter 4: End-to-End Interpolation and Fitting Workflow () () (Codebook)**

---

## Project Scope

This codebook provides a complete modeling workflow from raw data behavior inspection to interpolation, fitting, and residual diagnostics.

Generated artifacts:

- `codes/ch4_interpolation_comparison.png`
- `codes/ch4_runge_phenomenon.png`
- `codes/ch4_fit_residuals.png`
- `codes/ch4_model_selection_metrics.png`

---

## Step 1: Synthetic Dataset Construction

```python
import numpy as np

rng = np.random.default_rng(123)

# Clean reference signal
x_clean = np.linspace(0.0, 6.0, 25)
y_clean = np.sin(x_clean)

# Noisy observation set
noise_sigma = 0.12
y_noisy = y_clean + noise_sigma * rng.standard_normal(len(x_clean))

print("N samples:", len(x_clean))
print("Noise sigma:", noise_sigma)
print("y mean:", float(np.mean(y_noisy)))
print("y std:", float(np.std(y_noisy)))
```
**Sample Output:**
```
N samples: 25
Noise sigma: 0.12
y mean: 0.020236479105575248
y std: 0.714938022076501
```

---

## Step 2: Interpolation vs Trend Fit Visualization

```python
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
```

![Interpolation vs fitting](codes/ch4_interpolation_comparison.png)

---

## Step 3: Runge Phenomenon Demonstration

```python
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
```

![Runge phenomenon](codes/ch4_runge_phenomenon.png)

---

## Step 4: Fit Residual Diagnostics (Linear, Quadratic, Cubic)

```python
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-4/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(321)
x = np.linspace(-2.0, 2.0, 80)
y_true = 0.4 * x ** 3 - 0.8 * x + 0.5
y = y_true + 0.35 * rng.standard_normal(len(x))

models = {}
for deg in [1, 2, 3]:
    coef = np.polyfit(x, y, deg=deg)
    y_hat = np.polyval(coef, x)
    resid = y - y_hat
    rmse = float(np.sqrt(np.mean(resid ** 2)))
    models[deg] = {"coef": coef, "y_hat": y_hat, "resid": resid, "rmse": rmse}

fig, axes = plt.subplots(2, 2, figsize=(10.2, 7.2), constrained_layout=True)
ax_fit = axes[0, 0]
ax_r1 = axes[0, 1]
ax_r2 = axes[1, 0]
ax_r3 = axes[1, 1]

x_dense = np.linspace(x.min(), x.max(), 500)
ax_fit.scatter(x, y, s=16, alpha=0.6, color="tab:gray", label="data")
for deg, color in [(1, "tab:red"), (2, "tab:blue"), (3, "tab:green")]:
    ax_fit.plot(x_dense, np.polyval(models[deg]["coef"], x_dense), color=color, linewidth=2.0, label=f"deg {deg}")
ax_fit.set_title("Model Fits")
ax_fit.set_xlabel("x")
ax_fit.set_ylabel("y")
ax_fit.grid(True, alpha=0.3)
ax_fit.legend()

for ax, deg, color in [(ax_r1, 1, "tab:red"), (ax_r2, 2, "tab:blue"), (ax_r3, 3, "tab:green")]:
    ax.scatter(x, models[deg]["resid"], s=14, alpha=0.65, color=color)
    ax.axhline(0.0, color="black", linewidth=1.0)
    ax.set_title(f"Residuals (deg {deg}), RMSE={models[deg]['rmse']:.3f}")
    ax.set_xlabel("x")
    ax.set_ylabel("residual")
    ax.grid(True, alpha=0.3)

out_file = codes_dir / "ch4_fit_residuals.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
for deg in [1, 2, 3]:
    print(f"degree {deg} RMSE: {models[deg]['rmse']:.5f}")
```

![Fit residuals](codes/ch4_fit_residuals.png)

---

## Step 5: Model Selection Summary Plot

```python
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-4/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(321)
x = np.linspace(-2.0, 2.0, 80)
y_true = 0.4 * x ** 3 - 0.8 * x + 0.5
y = y_true + 0.35 * rng.standard_normal(len(x))

rmse_vals = []
aic_vals = []

for deg in [1, 2, 3, 4, 5]:
    coef = np.polyfit(x, y, deg=deg)
    y_hat = np.polyval(coef, x)
    resid = y - y_hat
    rss = float(np.sum(resid ** 2))
    n = len(x)
    k = deg + 1
    rmse = float(np.sqrt(rss / n))
    aic = float(n * np.log(rss / n) + 2 * k)
    rmse_vals.append(rmse)
    aic_vals.append(aic)

deg_axis = np.array([1, 2, 3, 4, 5])

fig, ax1 = plt.subplots(figsize=(8.4, 5.0))
ax1.plot(deg_axis, rmse_vals, marker="o", color="tab:blue", linewidth=2.0, label="RMSE")
ax1.set_xlabel("polynomial degree")
ax1.set_ylabel("RMSE", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.plot(deg_axis, aic_vals, marker="s", color="tab:orange", linewidth=2.0, label="AIC")
ax2.set_ylabel("AIC", color="tab:orange")
ax2.tick_params(axis="y", labelcolor="tab:orange")

ax1.set_title("Chapter 4: Error-Complexity Tradeoff (RMSE vs AIC)")

out_file = codes_dir / "ch4_model_selection_metrics.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
print("RMSE values:", rmse_vals)
print("AIC values:", aic_vals)
```

![Model selection metrics](codes/ch4_model_selection_metrics.png)

---

## Step 6: Validation Checklist

1. State whether task is interpolation or fitting.
2. Use domain-safe evaluation range and flag extrapolation.
3. Pair scalar metrics with residual plots.
4. Report model complexity and uncertainty considerations.
5. Keep generated outputs chapter-local for reproducibility.

---

## Step 7: Git Snapshot

```bash
git add docs/chapters/chapter-4/essay.md
git add docs/chapters/chapter-4/workbook.md
git add docs/chapters/chapter-4/codebook.md
git add docs/chapters/chapter-4/codes/ch4_interpolation_comparison.png
git add docs/chapters/chapter-4/codes/ch4_runge_phenomenon.png
git add docs/chapters/chapter-4/codes/ch4_fit_residuals.png
git add docs/chapters/chapter-4/codes/ch4_model_selection_metrics.png
git commit -m "Chapter 4: full-depth pedagogical and codebook upgrade"
```

---

## Bridge

Chapter 4 formalized data-to-model decisions. Chapter 5 will use these approximations to compute derivatives and integrals from discrete samples while managing noise amplification and truncation behavior.