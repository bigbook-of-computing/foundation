
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 5 Codebook: Numerical Differentiation
# Project 1: The Great Error Showdown (V-Plot Analysis)
# ==========================================================

# ==========================================================
# 1. Setup Functions and Parameters
# ==========================================================

def f(x):
    """The function to differentiate."""
    return np.sin(x)

def f_prime_analytic(x):
    """The exact analytic derivative: f'(x) = cos(x)."""
    return np.cos(x)

def central_difference(f_func, x, h):
    """
    Computes the first derivative using the O(h²) Central Difference stencil.
    f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
    """
    return (f_func(x + h) - f_func(x - h)) / (2.0 * h)

# Test point and True value
X_TEST = 1.0 
TRUE_DERIV = f_prime_analytic(X_TEST)

# Range of step sizes h (logarithmically spaced)
# We test from h=1e-1 down to h=1e-16 to see the full V-plot transition.
h_values = np.logspace(-1, -16, 100)

# ==========================================================
# 2. Compute Errors Across All h
# ==========================================================

numerical_derivs = central_difference(f, X_TEST, h_values)
absolute_errors = np.abs(numerical_derivs - TRUE_DERIV)

# ==========================================================
# 3. Visualization (The V-Plot)
# ==========================================================

# Find the optimal h (where the error is minimized)
h_optimal = h_values[np.argmin(absolute_errors)]
min_error = np.min(absolute_errors)

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the log-log V-curve
ax.loglog(h_values, absolute_errors, 'b-', linewidth=2, label="Total Absolute Error")

# Highlight the optimal point (the 'sweet spot')
ax.loglog(h_optimal, min_error, 'ro', markersize=8, label=f"Optimal $h$ ($\sim$ {h_optimal:.2e})")

# Add slope guides for analysis:
# Truncation error: O(h²) → slope = 2
ax.loglog([1e-1, 1e-5], [1e-4, 1e-12], 'k--', alpha=0.5, label=r"Truncation Error Slope ($\propto h^2$)")
# Round-off error: O(1/h) → slope = -1
ax.loglog([1e-10, 1e-16], [1e-5, 1e-11], 'g--', alpha=0.5, label=r"Round-off Error Slope ($\propto 1/h$)")

ax.set_title(r"V-Plot: Truncation vs. Round-off Error for $f'(x)$")
ax.set_xlabel(r"Step Size $h$ ($\log_{10}$ scale)")
ax.set_ylabel(r"Absolute Error $|\text{Error}|$ ($\log_{10}$ scale)")
ax.grid(True, which="both", ls="--")
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================

print("\n--- V-Plot Analysis ---")
print(f"Test Function: f(x) = sin(x) at x = {X_TEST}")
print(f"True Derivative: {TRUE_DERIV:.16f}")
print(f"Minimum Error Achieved: {min_error:.3e}")
print(f"Optimal Step Size (h_opt): {h_optimal:.2e}")
print("\nConclusion: The total error is minimized at h_opt ≈ 10⁻⁶, illustrating where the \ntruncation error (decreasing) is balanced by the round-off error (increasing).")
