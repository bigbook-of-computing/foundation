from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-3/codes")
codes_dir.mkdir(parents=True, exist_ok=True)

ALPHA = 8.0


def residual(k):
    return -k * (np.cos(k) / np.sin(k)) - np.sqrt(np.maximum(ALPHA ** 2 - k ** 2, 0.0))


def bisection_local(f, a, b, tol=1e-12, max_iter=200):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("Invalid bracket")
    for _ in range(max_iter):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or abs(b - a) < tol:
            return m
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)

# Build candidate brackets away from singular points n*pi
eps = 1e-3
candidates = [
    (0.5 * np.pi + eps, np.pi - eps),
    (1.5 * np.pi + eps, 2.0 * np.pi - eps),
]

roots = []
for a, b in candidates:
    if b >= ALPHA:
        continue
    fa, fb = residual(a), residual(b)
    if np.isfinite(fa) and np.isfinite(fb) and fa * fb < 0:
        roots.append(bisection_local(residual, a, b))

print("Odd-state k roots:", roots)

x = np.linspace(0.2, ALPHA - 1e-3, 1500)
y = residual(x)

fig, ax = plt.subplots(figsize=(8.2, 4.8))
ax.plot(x, y, color="tab:blue", linewidth=1.5, label="residual(k)")
ax.axhline(0.0, color="black", linewidth=1.0)

for r in roots:
    ax.axvline(r, linestyle="--", color="tab:red", alpha=0.8)
    ax.scatter([r], [0.0], color="tab:red", zorder=3)

ax.set_ylim(-15, 15)
ax.set_title("Chapter 3: Finite Well Odd-State Root Locations")
ax.set_xlabel("k")
ax.set_ylabel("residual(k)")
ax.grid(True, alpha=0.3)
ax.legend()

out_file = codes_dir / "ch3_finite_well_roots.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
