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
