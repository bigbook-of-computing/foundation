from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-2/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

x = np.float64(1e8)
delta = np.logspace(-2, -14, 50)
recovered = (x + delta) - x
rel_err = np.abs(recovered - delta) / delta

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.loglog(delta, rel_err, color="tab:red")
ax.set_title("Chapter 2: Relative Error from Cancellation")
ax.set_xlabel("true delta")
ax.set_ylabel("relative error")
ax.grid(True, which="both", alpha=0.3)

out_file = codes_dir / "ch2_cancellation_error.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
print("Worst relative error:", float(np.max(rel_err)))
