from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-2/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

x = np.logspace(0, 16, 60)
next_x = np.nextafter(x, np.inf)
abs_gap = next_x - x
rel_gap = abs_gap / x

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.loglog(x, abs_gap, label="absolute gap")
ax.loglog(x, rel_gap, label="relative gap")
ax.set_title("Chapter 2: Float Spacing vs Magnitude")
ax.set_xlabel("x")
ax.set_ylabel("gap")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

out_file = codes_dir / "ch2_gap_scaling.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
print("Median relative gap:", float(np.median(rel_gap)))
