import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 6 Codebook: Numerical Integration (Quadrature)
# Project 1: Quadrature Showdown (Trapezoidal vs. Simpson's Rule)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Test Function
# ==========================================================

# Define the integration limits and analytic solution
A = 0.0
B = np.pi
I_TRUE = 2.0  # Analytic solution for integral of sin(x) from 0 to pi

def f(x):
    """The function to integrate: f(x) = sin(x)."""
    return np.sin(x)

# ==========================================================
# 2. Quadrature Methods Implementation
# ==========================================================

def extended_trapezoidal(f_func, a, b, N):
    """Computes integral using the O(h²) Trapezoidal Rule with N intervals."""
    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    y = f_func(x)
    
    # Formula: I ≈ h * [ (1/2)y₀ + y₁ + ... + y_{N-1} + (1/2)yₙ ]
    integral = (h / 2.0) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
    return integral

def extended_simpson(f_func, a, b, N):
    """
    Computes integral using the O(h⁴) Simpson's Rule.
    Requires an even number of intervals (N must be even).
    """
    if N % 2 != 0:
        raise ValueError("Simpson's Rule requires an even number of intervals (N).")
        
    h = (b - a) / N
    x = np.linspace(a, b, N + 1)
    y = f_func(x)
    
    # Formula: I ≈ (h/3) * [ y₀ + 4y₁ + 2y₂ + 4y₃ + ... + 4y_{N-1} + yₙ ]
    # Sum of odd-indexed terms (weights=4) and even-indexed terms (weights=2)
    integral = (h / 3.0) * (y[0] + np.sum(4 * y[1:-1:2]) + np.sum(2 * y[2:-1:2]) + y[-1])
    return integral

# ==========================================================
# 3. Convergence Analysis
# ==========================================================

# Test with a range of interval numbers N (powers of 2 for easy comparison)
N_values = np.array([4, 8, 16, 32, 64, 128, 256, 512, 1024])

errors_trap = []
errors_simp = []

for N in N_values:
    # Calculate error for Trapezoidal
    I_trap = extended_trapezoidal(f, A, B, N)
    errors_trap.append(np.abs(I_trap - I_TRUE))
    
    # Calculate error for Simpson's (N is always even here)
    I_simp = extended_simpson(f, A, B, N)
    errors_simp.append(np.abs(I_simp - I_TRUE))

h_values = (B - A) / N_values # h = (b-a) / N

# ==========================================================
# 4. Visualization (Log-Log Plot)
# ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot Trapezoidal Error (Expected slope ≈ 2)
ax.loglog(h_values, errors_trap, 'b-o', label=r"Trapezoidal Error ($\mathcal{O}(h^2)$)")

# Plot Simpson's Error (Expected slope ≈ 4)
ax.loglog(h_values, errors_simp, 'r-s', label=r"Simpson's Error ($\mathcal{O}(h^4)$)")

# Add slope guides for visual confirmation
# Guide for O(h²)
ax.loglog([h_values[0], h_values[-1]], 
          [errors_trap[0], errors_trap[0] * (h_values[-1] / h_values[0])**2], 
          'k--', alpha=0.5, label=r"Guide Slope $m=2$")

# Guide for O(h⁴)
ax.loglog([h_values[0], h_values[-1]], 
          [errors_simp[0], errors_simp[0] * (h_values[-1] / h_values[0])**4], 
          'g--', alpha=0.5, label=r"Guide Slope $m=4$")

ax.set_title("Numerical Integration Convergence Rates")
ax.set_xlabel(r"Step Size $h$ ($\log_{10}$ scale)")
ax.set_ylabel(r"Absolute Error $|\text{Error}|$ ($\log_{10}$ scale)")
ax.grid(True, which="both", ls="--")
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================
print("\n--- Convergence Analysis ---")
print("N intervals (log2):", np.log2(N_values))
print("Log10(h) values:", np.log10(h_values))
print("Log10(Error) Trapezoidal:", np.log10(errors_trap))
print("Log10(Error) Simpson's:", np.log10(errors_simp))
print("\nConclusion: The slopes of the log-log plot confirm the predicted convergence orders: \nTrapezoidal method error decreases quadratically (slope ~2), while Simpson's \nmethod error decreases quartically (slope ~4), making Simpson's method vastly more efficient.")
