from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

codes_dir = Path("docs/chapters/chapter-3/codes")
codes_dir.mkdir(parents=True, exist_ok=True)


def bisection(f, a, b, tol_x=1e-12, tol_f=1e-12, max_iter=200):
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("Bisection requires a sign-change bracket.")

    hist = []
    x_old = None
    for i in range(max_iter):
        x = 0.5 * (a + b)
        fx = f(x)
        dx = np.nan if x_old is None else abs(x - x_old)
        hist.append((i, x, fx, dx))

        if abs(fx) < tol_f:
            return x, hist, "residual"
        if x_old is not None and abs(x - x_old) < tol_x:
            return x, hist, "step"

        if fa * fx < 0:
            b, fb = x, fx
        else:
            a, fa = x, fx

        x_old = x

    return x, hist, "max_iter"


def newton(f, df, x0, tol_x=1e-12, tol_f=1e-12, max_iter=100):
    hist = []
    x = x0
    x_old = None

    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)
        dx = np.nan if x_old is None else abs(x - x_old)
        hist.append((i, x, fx, dx))

        if abs(fx) < tol_f:
            return x, hist, "residual"
        if x_old is not None and abs(x - x_old) < tol_x:
            return x, hist, "step"

        if abs(dfx) < 1e-14:
            return x, hist, "derivative_floor"

        x_old = x
        x = x - fx / dfx

    return x, hist, "max_iter"


def secant(f, x0, x1, tol_x=1e-12, tol_f=1e-12, max_iter=100):
    f0, f1 = f(x0), f(x1)
    hist = [(0, x0, f0, np.nan), (1, x1, f1, abs(x1 - x0))]

    for i in range(2, max_iter + 1):
        denom = (f1 - f0)
        if abs(denom) < 1e-16:
            return x1, hist, "secant_breakdown"

        x2 = x1 - f1 * (x1 - x0) / denom
        f2 = f(x2)
        hist.append((i, x2, f2, abs(x2 - x1)))

        if abs(f2) < tol_f:
            return x2, hist, "residual"
        if abs(x2 - x1) < tol_x:
            return x2, hist, "step"

        x0, f0 = x1, f1
        x1, f1 = x2, f2

    return x1, hist, "max_iter"


def f(x):
    return np.cos(x) - x


def df(x):
    return -np.sin(x) - 1.0

r_b, h_b, t_b = bisection(f, 0.0, 1.0)
r_n, h_n, t_n = newton(f, df, 0.5)
r_s, h_s, t_s = secant(f, 0.0, 1.0)

print("Bisection root:", r_b, "termination:", t_b, "iters:", len(h_b))
print("Newton root:", r_n, "termination:", t_n, "iters:", len(h_n))
print("Secant root:", r_s, "termination:", t_s, "iters:", len(h_s))

fig, ax = plt.subplots(figsize=(8.2, 4.8))

for name, hist, color in [
    ("Bisection", h_b, "tab:blue"),
    ("Newton", h_n, "tab:orange"),
    ("Secant", h_s, "tab:green"),
]:
    k = np.array([row[0] for row in hist], dtype=float)
    r = np.array([abs(row[2]) for row in hist], dtype=float)
    r = np.maximum(r, 1e-18)
    ax.semilogy(k, r, marker="o", linewidth=1.5, markersize=3, label=name, color=color)

ax.set_title("Chapter 3: Convergence of Root-Finding Methods")
ax.set_xlabel("iteration")
ax.set_ylabel("|f(x_k)|")
ax.grid(True, which="both", alpha=0.3)
ax.legend()

out_file = codes_dir / "ch3_method_convergence.png"
fig.savefig(out_file, dpi=160, bbox_inches="tight")
plt.close(fig)

print(f"Saved figure to: {out_file}")
