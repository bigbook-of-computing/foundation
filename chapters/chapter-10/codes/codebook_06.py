import numpy as np
import matplotlib.pyplot as plt
import time
import random

# ==========================================================
# 1. Setup Parameters and Re-declare Solvers
# ==========================================================
N = 50                 
V_SOURCE = 100.0
TOLERANCE = 1e-4       
MAX_ITER = 10000

# Optimal omega for SOR
OMEGA = calculate_optimal_omega(N) # Using the optimal omega from Project 3

# We reuse the functions defined in Projects 2 and 3: 
# solve_jacobi, solve_gauss_seidel, solve_sor, calculate_optimal_omega

# The solver definitions must be available in the execution environment
# (They are assumed to be loaded from the previous projects).

# ==========================================================
# 2. Run All Three Comparisons
# ==========================================================

# Jacobi Run (T_low)
iter_jac, time_jac, res_jac = solve_jacobi(N, V_SOURCE, TOLERANCE)

# Gauss-Seidel Run (T_med)
iter_gs, time_gs, res_gs = solve_gauss_seidel(N, V_SOURCE, TOLERANCE)

# SOR Run (T_fast)
iter_sor, time_sor, res_sor, _ = solve_sor(N, V_SOURCE, TOLERANCE, OMEGA)

# ==========================================================
# 3. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Convergence History (Log Scale) ---
max_plot_iter = min(len(res_jac), len(res_gs), len(res_sor))

ax[0].plot(range(1, iter_jac + 1), res_jac, 'b--', label="Jacobi")
ax[0].plot(range(1, iter_gs + 1), res_gs, 'r-', label="Gauss-Seidel")
ax[0].plot(range(1, iter_sor + 1), res_sor, 'g-', label=f"SOR (\\omega={OMEGA:.3f})")

ax[0].axhline(TOLERANCE, color='k', linestyle=':', label="Tolerance")
ax[0].set_title("Comparative Convergence Rates (Log Scale)")
ax[0].set_xlabel("Iteration Number")
ax[0].set_ylabel("Maximum Residual")
ax[0].set_yscale('log')
ax[0].legend()
ax[0].grid(True, which="both", ls="--")

# --- Plot 2: Iteration Count Comparison (Bar Chart) ---
iter_values = [iter_jac, iter_gs, iter_sor]
labels = ['Jacobi', 'Gauss-Seidel', 'SOR']

ax[1].bar(labels, iter_values, color=['skyblue', 'salmon', 'darkgreen'])
ax[1].set_title(f"Total Iterations Required (L={N}, $\\epsilon={TOLERANCE:.1e}$)")
ax[1].set_ylabel("Total Iterations")
ax[1].grid(axis='y')

# Annotate values
for i, val in enumerate(iter_values):
    ax[1].text(i, val + 50, f"{val} Iters", ha='center', color='k', fontweight='bold')

plt.tight_layout()
plt.show()

# Final Analysis
gs_speedup = iter_jac / iter_gs
sor_speedup_gs = iter_gs / iter_sor
sor_speedup_jac = iter_jac / iter_sor

print("\n--- Full Convergence Comparison Summary ---")
print(f"Jacobi Iterations: {iter_jac}")
print(f"Gauss-Seidel Iterations: {iter_gs}")
print(f"SOR Iterations: {iter_sor}")
print("-" * 50)
print(f"GS Speedup (vs. Jacobi): {gs_speedup:.2f}x")
print(f"SOR Speedup (vs. Gauss-Seidel): {sor_speedup_gs:.2f}x")
print(f"SOR Speedup (vs. Jacobi): {sor_speedup_jac:.2f}x")

print("\nConclusion: SOR provides a massive acceleration, requiring only a fraction of the iterations needed by the other methods. This confirms the power of the over-relaxation factor (\u03c9) in iterative solvers, making it the most efficient method for solving static Elliptic PDEs.")
