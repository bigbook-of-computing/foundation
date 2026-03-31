import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 10 Codebook: Elliptic PDEs
# Project 1: Electrostatic Potential (Gauss-Seidel Relaxation)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Initial Grid
# ==========================================================

# Numerical Parameters
N = 50                 # Grid size N x N (number of interior points)
MAX_ITER = 10000       # Maximum iterations for safety
TOLERANCE = 1e-5       # Convergence tolerance for max residual

# Boundary Conditions (Voltage in Volts)
V_SOURCE = 100.0       # Voltage of the fixed source side (Top)
V_GROUND = 0.0         # Voltage of the other three sides

# Initialize the potential grid (including boundaries, so N+2 x N+2)
# The interior is initially set to 0.0 (or V_SOURCE for a better guess)
phi = np.full((N + 2, N + 2), V_GROUND, dtype=np.float64)

# Apply Boundary Conditions (Dirichlet)
# Top boundary (row 0) is the fixed source
phi[0, :] = V_SOURCE
# Other boundaries are already set to V_GROUND = 0.0

# ==========================================================
# 2. Gauss-Seidel Iterative Solver
# ==========================================================

print(f"Starting Gauss-Seidel Relaxation on {N+2}x{N+2} grid...")

iterations = 0
max_residual_history = []

for iteration in range(MAX_ITER):
    iterations += 1
    phi_old = phi.copy() # Store a copy of the old state to check convergence (residual)
    max_residual = 0.0

    # Iterate over all interior points (from 1 to N)
    for i in range(1, N + 1):
        for j in range(1, N + 1):
            
            # --- Five-Point Stencil (The FDM core) ---
            # phi[i,j] = 1/4 * (phi[i+1, j] + phi[i-1, j] + phi[i, j+1] + phi[i, j-1])
            
            # Gauss-Seidel: Use the already updated values in the current sweep (phi[i-1, j] and phi[i, j-1])
            phi_new = 0.25 * (
                phi_old[i + 1, j] + phi[i - 1, j] +  # Note: phi[i-1, j] is new
                phi_old[i, j + 1] + phi[i, j - 1]    # Note: phi[i, j-1] is new
            )
            
            # The core Gauss-Seidel update uses the new values for i-1 and j-1
            # while still referring to old values for i+1 and j+1.
            
            # Recalculate using the standard stencil (just for numerical check here)
            phi_update_check = 0.25 * (
                phi_old[i + 1, j] + phi[i - 1, j] +
                phi[i, j + 1] + phi[i, j - 1]
            )

            # Calculate the residual (change at this point)
            residual = np.abs(phi_new - phi_old[i, j])
            
            # Update the potential grid with the new value (Gauss-Seidel)
            phi[i, j] = phi_new
            
            # Track the maximum residual in this sweep
            max_residual = max(max_residual, residual)
    
    max_residual_history.append(max_residual)

    # Check for convergence
    if max_residual < TOLERANCE:
        print(f"Converged after {iterations} iterations. Max residual: {max_residual:.2e}")
        break

if iterations == MAX_ITER:
    print(f"Warning: Reached max iterations ({MAX_ITER}) without converging below tolerance.")

# ==========================================================
# 3. Visualization and Analysis
# ==========================================================

# --- Plot 1: Potential Field (Heatmap) ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot the 2D potential field (Heatmap)
im = ax[0].imshow(phi, cmap='viridis', origin='lower')
fig.colorbar(im, ax=ax[0], label="Potential (Volts)")
ax[0].set_title("Steady-State Electrostatic Potential ($\nabla^2 \phi = 0$)")
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
print("\n--- Simulation Summary ---")
print(f"Total Iterations: {iterations}")
print(f"Final Max Residual: {max_residual_history[-1]:.3e}")
print("\nConclusion: The Gauss-Seidel relaxation method successfully found the equilibrium \npotential distribution, confirmed by the exponential decrease of the maximum residual.")
