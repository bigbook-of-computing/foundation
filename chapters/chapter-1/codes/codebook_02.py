from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

# Resolve output location relative to the chapter directory
codes_dir = Path("docs/chapters/chapter-1/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

# 1. Generate data
x = np.linspace(0.0, 2.0 * np.pi, 400)
y = np.sin(x)

# 2. Plot with scientific labeling
fig, ax = plt.subplots(figsize=(8, 4.5))
ax.plot(x, y, color="tab:blue", linewidth=2.0, label="sin(x)")
ax.set_title("Chapter 1: First Reproducible Plot")
ax.set_xlabel("x (radians)")
ax.set_ylabel("Amplitude")
ax.grid(True, alpha=0.35)
ax.legend()

# 3. Save artifact for docs and reports
out_file = codes_dir / "ch1_sin_plot.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
