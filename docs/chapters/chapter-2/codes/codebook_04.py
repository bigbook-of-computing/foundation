from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-2/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

n = np.arange(0, 40)
true_y = (1.0 / 3.0) ** n

# Unstable recurrence: y_n = (10/3) y_{n-1} - y_{n-2}
unstable = np.zeros_like(true_y)
unstable[0] = 1.0
unstable[1] = 1.0 / 3.0
for k in range(2, len(n)):
    unstable[k] = (10.0 / 3.0) * unstable[k - 1] - unstable[k - 2]

fig, ax = plt.subplots(figsize=(8, 4.8))
ax.semilogy(n, np.abs(true_y), label="true |(1/3)^n|", linewidth=2)
ax.semilogy(n, np.abs(unstable), label="unstable recurrence", linewidth=2)
ax.set_title("Chapter 2: Stability vs Mathematical Correctness")
ax.set_xlabel("n")
ax.set_ylabel("absolute value (log scale)")
ax.grid(True, alpha=0.3)
ax.legend()

out_file = codes_dir / "ch2_stability_recurrence.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
print("Final true value:", float(true_y[-1]))
print("Final unstable value:", float(unstable[-1]))
