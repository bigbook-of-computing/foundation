import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 10 Codebook: Elliptic PDEs
# Project 1: Electrostatic Potential (Gauss-Seidel Relaxation)
# ==========================================================

# Numerical Parameters
N = 50                 # Grid size N x N (number of interior points)
MAX_ITER = 10000       # Maximum iterations for safety
TOLERANCE = 1e-5       # Convergence tolerance for max residual

# Boundary Conditions (Voltage in Volts)
V_SOURCE = 100.0       # Voltage of the fixed source side (Top)
V_GROUND = 0.0         # Voltage of the other three sides

# Initialize the potential grid (N+2 x N+2, including boundaries)
phi = np.full((N + 2, N + 2), V_GROUND, dtype=np.float64)

# Apply Boundary Conditions (Dirichlet)
# Top boundary (row 0) is the fixed source
phi[0, :] = V_SOURCE

# Gauss-Seidel Iterative Solver
iterations = 0
max_residual_history = []

for iteration in range(MAX_ITER):
    iterations += 1
    phi_old = phi.copy() 
    max_residual = 0.0

    for i in range(1, N + 1):
        for j in range(1, N + 1):
            
            # Gauss-Seidel: Use the already updated values for (i-1, j) and (i, j-1)
            phi_new = 0.25 * (
                phi_old[i + 1, j] + phi[i - 1, j] +  
                phi_old[i, j + 1] + phi[i, j - 1]
            )
            
            residual = np.abs(phi_new - phi_old[i, j])
            
            phi[i, j] = phi_new # Update the potential grid immediately
            
            max_residual = max(max_residual, residual)
    
    max_residual_history.append(max_residual)

    if max_residual < TOLERANCE:
        break

# --- Plot 1: Potential Field (Heatmap) ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

im = ax[0].imshow(phi, cmap='viridis', origin='lower')
fig.colorbar(im, ax=ax[0], label="Potential (Volts)")
ax[0].set_title("Steady-State Electrostatic Potential ($\\nabla^2 \\phi = 0$)")
ax[0].set_xlabel("x-index")
ax[0].set_ylabel("y-index")

# Add contour lines (Equipotential lines)
contours = ax[0].contour(phi, colors='white', alpha=0.6, levels=np.linspace(V_GROUND, V_SOURCE, 10))
ax[0].clabel(contours, inline=True, fontsize=8, fmt='%1.0f')


# --- Plot 2: Convergence History ---
ax[1].plot(max_residual_history, 'r-', linewidth=2)
ax[1].set_title("Convergence of Gauss-Seidel Method")
ax[1].set_xlabel("Iteration Number")
ax[1].set_ylabel("Maximum Residual (log scale)")
ax[1].set_yscale('log')
ax[1].grid(True)

plt.tight_layout()
plt.show()

# Final Analysis
print(f"Total Iterations: {iterations}")
print(f"Final Max Residual: {max_residual_history[-1]:.3e}")
