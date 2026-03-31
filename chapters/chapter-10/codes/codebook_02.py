
import numpy as np
import matplotlib.pyplot as plt
import time # For tracking computation time

# ==========================================================
# Chapter 10 Codebook: Elliptic PDEs
# Project 2: Comparative Efficiency (Jacobi vs. Gauss-Seidel)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Grid
# ==========================================================
N = 50                 # Grid size
V_SOURCE = 100.0
TOLERANCE = 1e-4       # Increased tolerance for faster comparison

# ==========================================================
# 2. Solver Functions
# ==========================================================

def solve_jacobi(N, V_source, tolerance, max_iter=10000):
    """Jacobi Method: Updates synchronously (requires two arrays)."""
    phi = np.full((N + 2, N + 2), 0.0, dtype=np.float64)
    phi[0, :] = V_source
    
    residual_history = []
    
    start_time = time.time()
    for iteration in range(max_iter):
        phi_new = phi.copy()
        max_residual = 0.0
        
        # Iterate over interior points
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Jacobi: Use only values from the previous time step (phi)
                phi_new[i, j] = 0.25 * (
                    phi[i + 1, j] + phi[i - 1, j] + 
                    phi[i, j + 1] + phi[i, j - 1]
                )
                
                residual = np.abs(phi_new[i, j] - phi[i, j])
                max_residual = max(max_residual, residual)
        
        phi = phi_new # Update the entire grid at once
        residual_history.append(max_residual)

        if max_residual < tolerance:
            break
            
    end_time = time.time()
    return iteration + 1, end_time - start_time, residual_history

def solve_gauss_seidel(N, V_source, tolerance, max_iter=10000):
    """Gauss-Seidel Method: Updates sequentially (requires one array)."""
    phi = np.full((N + 2, N + 2), 0.0, dtype=np.float64)
    phi[0, :] = V_source
    
    residual_history = []
    
    start_time = time.time()
    for iteration in range(max_iter):
        max_residual = 0.0
        
        # Store a copy of the previous state for residual check *only*
        phi_old_for_residual = phi.copy() 

        for i in range(1, N + 1):
            for j in range(1, N + 1):
                phi_current = phi[i, j]
                
                # Gauss-Seidel: Use refreshed values (i-1, j) and (i, j-1)
                phi[i, j] = 0.25 * (
                    phi[i + 1, j] + phi[i - 1, j] + 
                    phi[i, j + 1] + phi[i, j - 1]
                )
                
                residual = np.abs(phi[i, j] - phi_current)
                max_residual = max(max_residual, residual)
        
        residual_history.append(max_residual)
        
        if max_residual < tolerance:
            break
            
    end_time = time.time()
    return iteration + 1, end_time - start_time, residual_history

# ==========================================================
# 3. Run Comparison
# ==========================================================

print("Running Comparison...")
iter_jac, time_jac, res_jac = solve_jacobi(N, V_SOURCE, TOLERANCE)
iter_gs, time_gs, res_gs = solve_gauss_seidel(N, V_SOURCE, TOLERANCE)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Iteration Count Comparison ---
ax[0].bar(['Jacobi', 'Gauss-Seidel'], [iter_jac, iter_gs], color=['skyblue', 'salmon'])
ax[0].set_title(f"Iterations to Converge ($\epsilon={TOLERANCE}$)")
ax[0].set_ylabel("Total Iterations")
ax[0].grid(axis='y')
ax[0].text(0, iter_jac / 2, f"{iter_jac} Iters", ha='center', color='black', fontweight='bold')
ax[0].text(1, iter_gs / 2, f"{iter_gs} Iters", ha='center', color='black', fontweight='bold')


# --- Plot 2: Convergence History ---
# Plot up to the maximum number of shared iterations for clear comparison
max_plot_iter = min(len(res_jac), len(res_gs)) 
ax[1].plot(range(1, max_plot_iter + 1), res_jac[:max_plot_iter], 'b--', label="Jacobi")
ax[1].plot(range(1, max_plot_iter + 1), res_gs[:max_plot_iter], 'r-', label="Gauss-Seidel")
ax[1].axhline(TOLERANCE, color='k', linestyle=':', label="Tolerance")

ax[1].set_title("Convergence Rate Comparison (Log Scale)")
ax[1].set_xlabel("Iteration Number")
ax[1].set_ylabel("Maximum Residual")
ax[1].set_yscale('log')
ax[1].legend()
ax[1].grid(True, which="both", ls="--")

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Efficiency Comparison ---")
print(f"Grid Size N: {N}")
print(f"Convergence Tolerance: {TOLERANCE:.1e}")
print("-" * 50)
print("Jacobi Method (Synchronous):")
print(f"  Total Iterations: {iter_jac}")
print(f"  Total Time: {time_jac:.4f} s")

print("\nGauss-Seidel Method (Sequential):")
print(f"  Total Iterations: {iter_gs}")
print(f"  Total Time: {time_gs:.4f} s")
print("-" * 50)

# Quantify the speedup
speedup_iter = iter_jac / iter_gs
speedup_time = time_jac / time_gs

print(f"Gauss-Seidel Iteration Speedup: {speedup_iter:.2f}x (Expected: ~2.0x)")
print(f"Gauss-Seidel Time Speedup: {speedup_time:.2f}x (Varies by hardware/language)")

print("\nConclusion: Gauss-Seidel requires significantly fewer iterations to converge \n(speedup factor close to 2x) because it propagates new boundary information \nfaster into the domain.")
