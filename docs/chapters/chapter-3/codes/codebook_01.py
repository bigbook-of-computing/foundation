import numpy as np


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
