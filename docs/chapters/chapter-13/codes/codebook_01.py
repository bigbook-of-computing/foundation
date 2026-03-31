
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded, lu_factor, lu_solve
import time

# ==========================================================
# Chapter 13 Codebook: Systems of Linear Equations
# Project 1: Tridiagonal System Solver (Thomas Algorithm)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and System (A*x = b)
# ==========================================================

N = 1000  # System size N x N (1000 unknowns)
# This size makes the O(N³) cost significant, highlighting the O(N) advantage.

# --- Matrix A: Tridiagonal (from FDM stencil for y'' = 0) ---
# Main diagonal: 2.0
# Upper/Lower diagonals: -1.0
MAIN_DIAG_VAL = 2.0
OFF_DIAG_VAL = -1.0

# --- Vector b (Source/RHS) ---
# We use a simple constant source term for b.
B_VAL = 1.0
b = np.full(N, B_VAL)

# ==========================================================
# 2. Method 1: The Thomas Algorithm (O(N) - Specialized)
# ==========================================================
# The Thomas Algorithm is implemented via solve_banded (banded matrix solver).

# Create the banded matrix storage (3 rows: upper, main, lower)
ab = np.zeros((3, N))

# Row 1: Main diagonal (N elements)
ab[1, :] = MAIN_DIAG_VAL

# Row 0: Upper diagonal (N-1 elements, shifted right by 1)
ab[0, 1:] = OFF_DIAG_VAL

# Row 2: Lower diagonal (N-1 elements, shifted left by 1)
ab[2, :-1] = OFF_DIAG_VAL

start_time_thomas = time.time()
# Solve the system: x_thomas = A⁻¹ * b
x_thomas = solve_banded((1, 1), ab, b)
time_thomas = time.time() - start_time_thomas

# ==========================================================
# 3. Method 2: General LU Decomposition (O(N³) Factor, O(N²) Solve)
# ==========================================================
# We use this as the benchmark for a general solver.

# Create the full, dense matrix A for the general solver
A_full = np.diag(np.full(N, MAIN_DIAG_VAL)) \
       + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=1) \
       + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=-1)

start_time_lu = time.time()
# Factorization: LU_factor (O(N³) step)
lu, piv = lu_factor(A_full)
# Substitution: lu_solve (O(N²) step)
x_lu = lu_solve((lu, piv), b)
time_lu = time.time() - start_time_lu

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

# --- Plot 1: Solution Vector ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(np.arange(N), x_thomas, 'b-', label="Solution Vector $x$")
ax[0].set_title(r"Solution of Tridiagonal System $\mathbf{A}\mathbf{x} = \mathbf{b}$ ($N=1000$)")
ax[0].set_xlabel("Node Index $i$")
ax[0].set_ylabel("Solution Value $x_i$")
ax[0].grid(True)
ax[0].legend()


# --- Plot 2: Efficiency Comparison ---
# Use the slower time (LU Decomposition) as the normalization point
comparison_data = {
    "Method": ["Thomas (O(N))", "General LU (O(N³))"],
    "Time": [time_thomas, time_lu]
}

ax[1].bar(comparison_data["Method"], comparison_data["Time"], color=['green', 'red'])
ax[1].set_title(f"Computation Time Comparison (N={N})")
ax[1].set_ylabel("Time (seconds)")
ax[1].grid(axis='y')
ax[1].text(0, time_thomas / 2, f"{time_thomas:.3e} s", ha='center', color='black', fontweight='bold')
ax[1].text(1, time_lu / 2, f"{time_lu:.3e} s", ha='center', color='black', fontweight='bold')


plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================

# Check accuracy (should be near machine epsilon)
max_error_check = np.max(np.abs(x_thomas - x_lu))

print("\n--- Linear System Solver Analysis ---")
print(f"System Size N: {N}")
print(f"Thomas (Specialized O(N)) Time: {time_thomas:.4e} s")
print(f"General LU (O(N³)) Time:       {time_lu:.4e} s")
print("-" * 40)
print(f"Max Absolute Error (|x_thomas - x_lu|): {max_error_check:.2e}")
print(f"Time Speedup (LU/Thomas): {time_lu / time_thomas:.2f}x")

print("\nConclusion: The Thomas Algorithm (solve_banded) is significantly faster than general \nLU Decomposition for tridiagonal systems, confirming the efficiency gain of \nexploiting the sparse matrix structure (O(N) vs. O(N³)).")
