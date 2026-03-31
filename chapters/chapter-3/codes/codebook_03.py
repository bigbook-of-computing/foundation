from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-3/codes")
codes_dir.mkdir(parents=True, exist_ok=True)


def f(x):
    return np.cos(x) - x

x = np.linspace(-1.0, 2.0, 600)
y = f(x)

fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.axhline(0.0, color="black", linewidth=1.0)
ax.plot(x, y, color="tab:purple", linewidth=2.0, label="f(x)=cos(x)-x")

# Show example bracket used by bisection
ax.axvline(0.0, linestyle="--", color="tab:gray", alpha=0.7)
ax.axvline(1.0, linestyle="--", color="tab:gray", alpha=0.7)
ax.scatter([0.0, 1.0], [f(0.0), f(1.0)], color="tab:red", zorder=3, label="bracket endpoints")

ax.set_title("Chapter 3: Residual Landscape and Root Bracket")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.grid(True, alpha=0.3)
ax.legend()

out_file = codes_dir / "ch3_residual_landscape.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
