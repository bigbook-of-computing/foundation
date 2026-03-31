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
