# **Chapter 4: Interpolation, Fitting, and Residual Judgment (Codebook)**

---

This Codebook provides the technical implementation for modeling datasets. We explore the two fundamental strategies: **Interpolation** (treating data as exact constraints) and **Least-Squares Fitting** (treating data as noisy observations). We also demonstrate the dangerous instability of high-degree polynomials known as **Runge's Phenomenon**.

---

## Project 1: Splines vs. Global Polynomials

| Feature | Description |
| :--- | :--- |
| **Goal** | Interpolate a sparse set of 10 points using both a 9th-degree Lagrange polynomial and a Piecewise Cubic Spline. |
| **Mathematical Model** | Runge's test function: $f(x) = 1 / (1 + 25x^2)$. |
| **Core Concept** | Identifying the **boundary oscillations** characteristic of high-degree global interpolation. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import BarycentricInterpolator, CubicSpline

def compare_interpolation_methods():
    """Demonstrates Runge's Phenomenon and the stability of Cubic Splines."""
    
    # 1. Target function (Runge's function)
    f = lambda x: 1.0 / (1.0 + 25.0 * x**2)
    
    # 2. Sparse interpolation nodes (Uniform)
    x_nodes = np.linspace(-1, 1, 11)
    y_nodes = f(x_nodes)
    
    # 3. Interpolants
    poly = BarycentricInterpolator(x_nodes, y_nodes)
    spline = CubicSpline(x_nodes, y_nodes)
    
    # 4. Evaluation grid
    x_dense = np.linspace(-1, 1, 500)
    
    # Visualization
    plt.figure(figsize=(10, 6), dpi=150)
    plt.plot(x_dense, f(x_dense), 'k--', alpha=0.5, label='True Function')
    plt.plot(x_dense, poly(x_dense), 'r-', label='9th-Degree Polynomial')
    plt.plot(x_dense, spline(x_dense), 'b-', label='Cubic Spline')
    plt.scatter(x_nodes, y_nodes, color='black', s=20, zorder=3)
    
    plt.ylim(-0.5, 1.5)
    plt.title("Runge's Phenomenon: The Danger of Global Interpolation")
    plt.legend()
    plt.grid(True, alpha=0.2)
    plt.savefig("codes/ch4_interpolation_comparison.png")
    plt.close()

if __name__ == "__main__":
    compare_interpolation_methods()
```

### Expected Outcome and Interpretation

The output clearly shows the **Runge Ripple**. While the global polynomial is exact at the 11 nodes, it oscillates wildly between the nodes near the edges ($\pm 1$). The Cubic Spline, being piecewise, remains perfectly stable and follows the true function much more faithfully. This validates a core principle: **Global degree $N$ is almost never the answer for large $N$.**

---

## Project 2: Noisy Data & Residual Analysis

| Feature | Description |
| :--- | :--- |
| **Goal** | Fit a linear model to noisy synthetic data and analyze the distribution of errors (residuals). |
| **Mathematical Model** | $y_i = a x_i + b + \epsilon$; Least-Squares Regression. |
| **Core Concept** | Using **Residual Plots** to verify model adequacy and detect hidden bias. |

### Complete Python Code

```python
import numpy as np
import matplotlib.pyplot as plt

def audit_linear_fit():
    """Fits noisy linear data and analyzes the residuals."""
    
    # 1. Generate data
    np.random.seed(42)
    x = np.linspace(0, 10, 50)
    y_true = 2.5 * x + 5.0
    noise = np.random.normal(0, 2.0, size=x.shape)
    y_obs = y_true + noise
    
    # 2. Least-Squares Fit
    slope, intercept = np.polyfit(x, y_obs, deg=1)
    y_fit = slope * x + intercept
    residuals = y_obs - y_fit
    
    # 3. Create Multi-Panel Diagnostic Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Panel A: The Fit
    ax1.scatter(x, y_obs, color='gray', alpha=0.6, label='Observations')
    ax1.plot(x, y_fit, 'r-', linewidth=2, label=f'Fit: {slope:.2f}x + {intercept:.2f}')
    ax1.set_title("Linear Least-Squares Fit")
    ax1.legend()
    
    # Panel B: Residuals
    ax2.scatter(x, residuals, color='purple', alpha=0.7)
    ax2.axhline(0, color='black', linestyle='--')
    ax2.set_title("Residual Distribution (Noise Analysis)")
    ax2.set_ylabel("Error ($y_{obs} - y_{fit}$)")
    
    plt.savefig("codes/ch4_fit_residuals.png")
    plt.close()

if __name__ == "__main__":
    audit_linear_fit()
```

### Expected Outcome and Interpretation

The residual plot (Panel B) shows points randomly scattered around zero with no visible trend (no "smile" or "frown"). This confirms that the **Linear Model is adequate** for this data. If the residuals showed a curved pattern, it would be a signal that our data is actually non-linear (e.g., quadratic) and that we are **Underfitting** the physics.

---

## **References**

[1] de Boor, C. (1978). *A Practical Guide to Splines*. Springer-Verlag.

[2] Trefethen, L. N. (2012). *Approximation Theory and Approximation Practice*. SIAM.

[3] Draper, N. R., & Smith, H. (1998). *Applied Regression Analysis*. Wiley-Interscience.