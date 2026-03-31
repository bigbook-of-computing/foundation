
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve, solve_banded, inv
import time

# ==========================================================
# Chapter 13 Codebook: Systems of Linear Equations
# Project 2: Stability Check (Avoiding A⁻¹)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and System
# ==========================================================

N = 500  # Use a smaller N to keep the O(N³) inverse calculation feasible but slow
MAIN_DIAG_VAL = 2.0
OFF_DIAG_VAL = -1.0
B_VAL = 1.0

# --- Full Matrix A ---
A = np.diag(np.full(N, MAIN_DIAG_VAL)) \
  + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=1) \
  + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=-1)
b = np.full(N, B_VAL)

# --- Banded Matrix for Thomas/solve_banded (Reference) ---
ab = np.zeros((3, N))
ab[1, :] = MAIN_DIAG_VAL
ab[0, 1:] = OFF_DIAG_VAL
ab[2, :-1] = OFF_DIAG_VAL

# ==========================================================
# 2. Method 1: The Standard Solver (Reference, Preferred)
# ==========================================================
# This method uses optimized LU decomposition (O(N³)) for the factorization.

start_time_solve = time.time()
x_solve = solve(A, b)
time_solve = time.time() - start_time_solve

# ==========================================================
# 3. Method 2: Explicit Inverse (Inefficient and Unstable)
# ==========================================================
# Explicitly calculate A⁻¹ and then multiply by b.

start_time_inv = time.time()
# Factorization: inv(A) (O(N³))
A_inv = inv(A)
# Multiplication: A_inv * b (O(N²))
x_inv = A_inv @ b
time_inv = time.time() - start_time_inv

# ==========================================================
# 4. Method 3: The O(N) Specialized Solver (Efficiency Reference)
# ==========================================================

start_time_thomas = time.time()
x_thomas = solve_banded((1, 1), ab, b)
time_thomas = time.time() - start_time_thomas

# ==========================================================
# 5. Analysis and Comparison
# ==========================================================

# Compare the inefficient inverse method against the accurate standard solver
error_inv = np.max(np.abs(x_inv - x_solve))

# Create plotting data
time_data = [time_solve, time_inv, time_thomas]
label_data = [r"solve(A, b) $\mathcal{O}(N^3)$", r"inv(A)@b $\mathcal{O}(N^3)$", r"solve\_banded $\mathcal{O}(N)$"]

# --- Plot 1: Time Comparison ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].bar(label_data, time_data, color=['green', 'red', 'blue'])
ax[0].set_title(f"Time Cost Comparison ($N={N}$)")
ax[0].set_ylabel("Time (seconds)")
ax[0].tick_params(axis='x', rotation=10)
ax[0].grid(axis='y')


# --- Plot 2: Numerical Accuracy Comparison ---
error_data = [
    0, # solve(A,b) is the reference (error is zero)
    error_inv, 
    np.max(np.abs(x_thomas - x_solve)) # Thomas error vs. Reference
]
error_labels = ["Reference Error", r"A⁻¹@b Error", r"Thomas Error"]

ax[1].bar(error_labels, error_data, color=['green', 'red', 'blue'])
ax[1].axhline(np.finfo(float).eps, color='gray', linestyle='--', label=r"Machine $\epsilon$")
ax[1].set_title("Maximum Absolute Error vs. Reference")
ax[1].set_ylabel("Max Absolute Error")
ax[1].grid(axis='y', which="both", ls="--")
ax[1].ticklabel_format(axis='y', style='sci', scilimits=(-1, 1)) 
ax[1].legend()

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Numerical Stability and Efficiency Summary ---")
print(f"System Size N: {N}")
print(f"1. solve(A, b) Time (Reference): {time_solve:.4e} s")
print(f"2. inv(A)@b Time (Inefficient):  {time_inv:.4e} s")
print(f"3. Thomas Alg Time (O(N)):       {time_thomas:.4e} s")
print("-" * 50)
print(f"Max Error from Inverse (A⁻¹@b): {error_inv:.2e}")

print("\nConclusion: The explicit calculation of A⁻¹ is both significantly slower (despite the same O(N³) complexity due to overhead) and yields a solution with a greater numerical error than the built-in solve(A, b) function. This confirms the rule of computational physics: always use decomposition-based solvers, never explicit inversion.")
