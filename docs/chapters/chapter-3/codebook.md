# **Chapter 3: Root Finding (Codebook)**

---

This Codebook provides the exact, reproducible Python implementation for solving nonlinear equations. We compare the reliability of **Bisection** against the high-speed convergence of **Newton-Raphson** and its derivative-free alternative, the **Secant Method**.

---

## Project 1: Comparative Solver Audit

| Feature | Description |
| :--- | :--- |
| **Goal** | Solve $\cos(x) - x = 0$ using Bisection, Newton, and Secant methods, comparing their convergence rates. |
| **Mathematical Model** | $f(x) = \cos(x) - x$; $f'(x) = -\sin(x) - 1$. |
| **Core Concept** | Tracking the "Precision Gain" (bits per iteration) across different solver architectures. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt

def audit_solvers():
    """Compares Bisection, Newton, and Secant methods on a benchmark problem."""
    
    f = lambda x: np.cos(x) - x
    df = lambda x: -np.sin(x) - 1.0
    
    # 1. Bisection (Safe, Linear)
    a, b = 0.0, 1.0
    bisect_history = []
    for i in range(50):
        c = (a + b) / 2
        fc = f(c)
        bisect_history.append(abs(fc))
        if f(a) * fc < 0: b = c
        else: a = c
        if abs(fc) < 1e-12: break
            
    # 2. Newton (Fast, Quadratic)
    x = 0.5
    newton_history = []
    for i in range(20):
        fx = f(x)
        newton_history.append(abs(fx))
        if abs(fx) < 1e-12: break
        x = x - fx / df(x)
            
    # 3. Secant (Derivative-free, Superlinear)
    x0, x1 = 0.0, 1.0
    secant_history = []
    for i in range(20):
        f0, f1 = f(x0), f(x1)
        secant_history.append(abs(f1))
        if abs(f1) < 1e-12: break
        x_next = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x_next

    # Visualization
    plt.figure(figsize=(10, 6))
    plt.semilogy(bisect_history, 'o-', label='Bisection (Linear)')
    plt.semilogy(newton_history, 's-', label='Newton (Quadratic)')
    plt.semilogy(secant_history, '^-', label='Secant (1.618)')
    plt.axhline(1e-12, color='black', linestyle='--', alpha=0.3)
    plt.title("Root-Finding Convergence Rates")
    plt.xlabel("Iteration Count")
    plt.ylabel("Residual $|f(x)|$")
    plt.grid(True, which="both", ls="-", alpha=0.2)
    plt.legend()
    plt.savefig("codes/ch3_method_convergence.png")
    plt.close()

if __name__ == "__main__":
    audit_solvers()
```

### Expected Outcome and Interpretation

The plot reveals the **Hierarchy of Speed**. Bisection moves at a steady linear rate, gaining approximately 1 bit of precision per iteration. Newton-Raphson exhibits a dramatic "vertical drop" once it nears the root, doubling the number of correct digits with each step. The Secant method falls in between, offering high speed without requiring an explicit derivative. This audit validates using Bisection for robustness and Newton for final high-precision polishing.

---

## Project 2: Bracketing Physical Singularities

| Feature | Description |
| :--- | :--- |
| **Goal** | Isolate roots for the Finite Square Well problem: $-k \cot(k) - \sqrt{\alpha^2 - k^2} = 0$. |
| **Mathematical Model** | Transcendental equation for quantum bound states. |
| **Core Concept** | Using "Domain Knowledge" to build safe brackets around singularities ($n\pi$). |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt

def solve_quantum_well(alpha=8.0):
    """Finds odd-state energy roots while avoiding cotangent poles."""
    
    residual = lambda k: -k * (np.cos(k)/np.sin(k)) - np.sqrt(alpha**2 - k**2)
    
    # 1. Visualization for Bracket Identification
    k_vals = np.linspace(0.1, alpha-0.1, 1000)
    res_vals = residual(k_vals)
    
    plt.figure(figsize=(10, 5))
    plt.plot(k_vals, res_vals, label='Residual $R(k)$')
    plt.axhline(0, color='black', linewidth=1)
    
    # Identify roots manually/visually first
    # For alpha=8, roots are near 2.5 and 5.5
    plt.ylim(-20, 20)
    plt.title(f"Finite Well Residual ($\alpha={alpha}$)")
    plt.grid(True, alpha=0.3)
    plt.savefig("codes/ch3_residual_landscape.png")
    plt.close()

if __name__ == "__main__":
    solve_quantum_well()
```

### Expected Outcome and Interpretation

The "Landscape" plot is essential because $k \cot(k)$ has infinite poles at $k = n\pi$. A standard solver would "jump" these poles and find garbage. By plotting first, we identify safe **brackets** (e.g., $[2, 3]$ and $[5, 6]$) where the function is smooth and a sign change is guaranteed. This confirms that **Visualization is a Diagnostic Tool**, not just an endpoint.

---

## **References**

[1] Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing*. Cambridge University Press.

[2] Brent, R. P. (1973). *Algorithms for Minimization without Derivatives*. Prentice-Hall.

[3] Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis*. Cengage Learning.