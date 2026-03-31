
import numpy as np
import matplotlib.pyplot as plt

# Set a seed for reproducibility
np.random.seed(42)

# ==========================================================
# Chapter 17 Codebook: Randomness in Physics
# Project 2: Monte Carlo Integration (Area Under a Curve)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Test Function
# ==========================================================
I_ANALYTIC = 1.0 / 3.0  # True integral of x² from 0 to 1
DOMAIN_VOLUME = 1.0     # Volume of the integration domain (1 - 0 = 1)

def f(x):
    """The function to integrate: f(x) = x²."""
    return x**2

# Test a range of increasing sample sizes (N) to show convergence
N_SAMPLES_RANGE = np.logspace(1, 6, 20, dtype=int)

# ==========================================================
# 2. Perform Monte Carlo Integration
# ==========================================================

monte_carlo_estimates = []
absolute_errors = []

for N in N_SAMPLES_RANGE:
    # 1. Generate random sample points (Uniform distribution in [0, 1])
    x_samples = np.random.rand(N)
    
    # 2. Evaluate the function at the random points
    f_samples = f(x_samples)
    
    # 3. Calculate the average function value
    f_average = np.mean(f_samples)
    
    # 4. Monte Carlo Estimate: I ≈ Volume * <f>
    I_mc = DOMAIN_VOLUME * f_average
    
    monte_carlo_estimates.append(I_mc)
    absolute_errors.append(np.abs(I_mc - I_ANALYTIC))

# ==========================================================
# 3. Visualization and Analysis (Verifying the 1/sqrt(N) law)
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Convergence of Estimate ---
ax[0].semilogx(N_SAMPLES_RANGE, monte_carlo_estimates, 'b-o', markersize=4)
ax[0].axhline(I_ANALYTIC, color='r', linestyle='--', label=f"Analytic Value ({I_ANALYTIC:.4f})")

ax[0].set_title("Monte Carlo Estimate Convergence")
ax[0].set_xlabel("Number of Samples $N$ ($\log_{10}$ scale)")
ax[0].set_ylabel("Integral Estimate $I_{\text{MC}}$")
ax[0].grid(True, which="both", ls="--")
ax[0].legend()

# --- Plot 2: Error Analysis (Verifying 1/sqrt(N)) ---
# The error plot confirms the scaling rate.
ax[1].loglog(N_SAMPLES_RANGE, absolute_errors, 'b-o', markersize=4, label="Observed Absolute Error")

# Plot the theoretical guide: Error ∝ 1/sqrt(N) → slope = -0.5
# We use the first point to scale the theoretical guide line
E0 = absolute_errors[0]
N0 = N_SAMPLES_RANGE[0]
theoretical_error_guide = E0 * np.sqrt(N0) / np.sqrt(N_SAMPLES_RANGE)

ax[1].loglog(N_SAMPLES_RANGE, theoretical_error_guide, 'r--', label=r"Theoretical Slope ($\propto 1/\sqrt{N}$)")

ax[1].set_title("Monte Carlo Error Scaling")
ax[1].set_xlabel("Number of Samples $N$ ($\log_{10}$ scale)")
ax[1].set_ylabel("Absolute Error ($\log_{10}$ scale)")
ax[1].grid(True, which="both", ls="--")
ax[1].legend()

plt.tight_layout()
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================
final_N = N_SAMPLES_RANGE[-1]
final_I_mc = monte_carlo_estimates[-1]
final_error = absolute_errors[-1]

print("\n--- Monte Carlo Integration Summary ---")
print(f"Analytic Value (I_true): {I_ANALYTIC:.6f}")
print(f"Final Samples (N): {final_N}")
print("-" * 50)
print(f"Final Monte Carlo Estimate: {final_I_mc:.6f}")
print(f"Final Absolute Error: {final_error:.2e}")

print("\nConclusion: The estimate converges to the true value, and the error plot confirms the \ncharacteristic $1/\sqrt{N}$ scaling. This proves the feasibility of Monte Carlo methods for high-dimensional integration.")
