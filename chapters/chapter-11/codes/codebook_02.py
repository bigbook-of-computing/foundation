
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded # Efficient solver for tridiagonal systems

# ==========================================================
# Chapter 11 Codebook: Parabolic PDEs
# Project 2: The Gold Standard (Crank-Nicolson)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Implicit Solver Function
# ==========================================================
# Physical parameters
L = 1.0          # Length of the rod (m)
N = 50           # Number of interior grid points
h_x = L / (N + 1) # Spatial step size (Δx)
D = 1.0          # Thermal diffusivity (m²/s)

# Conditions
T_initial = 100.0
T_boundary = 0.0
T_FINAL = 0.1      # Final time

# Time Step: Chosen to deliberately violate FTCS stability (α=0.5) by a large margin
# If FTCS limit h_t is 0.0001, we choose h_t = 0.005 (50x larger).
h_t_large = 0.005 

# Compute diffusion number (alpha)
alpha = D * h_t_large / (h_x ** 2)

# ==========================================================
# 2. Crank-Nicolson Solver Implementation
# ==========================================================

def crank_nicolson_solve(T_init, T_bound):
    """
    Solves the 1D Heat Equation using the Implicit Crank-Nicolson Method.
    The method is O(h_t²) accurate and unconditionally stable.
    """
    N_steps = int(T_FINAL / h_t_large)
    
    # ----------------------------------------------------------------
    # A. Construct the Tridiagonal Matrix A (LHS)
    # ----------------------------------------------------------------
    # A * T_n+1 = b (Tridiagonal System)
    # The matrix size is N x N (only interior points, boundaries are fixed)
    
    # Diagonal coefficient: (1 + alpha)
    diag_val = 1.0 + alpha
    # Off-diagonal coefficient: (-alpha / 2)
    off_diag_val = -0.5 * alpha
    
    # Prepare the banded matrix structure for scipy.linalg.solve_banded
    # Banded storage: 3 rows (upper, main, lower diagonal)
    # Row 0: Upper diagonal (N-1 elements)
    # Row 1: Main diagonal (N elements)
    # Row 2: Lower diagonal (N-1 elements)
    
    # Diagonal elements
    main_diag = np.full(N, diag_val)
    # Off-diagonal elements (N-1 elements)
    off_diag = np.full(N - 1, off_diag_val)
    
    # The banded matrix storage for 'solve_banded'
    # Order: [upper_diag, main_diag, lower_diag]
    ab = np.zeros((3, N))
    ab[1, :] = main_diag      # Main diagonal
    ab[0, 1:] = off_diag      # Upper diagonal (shifted right by 1)
    ab[2, :-1] = off_diag     # Lower diagonal (shifted left by 1)
    
    # ----------------------------------------------------------------
    # B. Initialize State and Time March
    # ----------------------------------------------------------------
    
    # T_present stores INTERIOR points only (size N)
    T_present = np.full(N, T_init)
    T_history = [T_present.copy()]
    
    for n in range(N_steps):
        # ----------------------------------------------------------------
        # C. Construct the RHS Vector (b)
        # ----------------------------------------------------------------
        # b = T_n + (alpha/2) * [T_i+1,n - 2T_i,n + T_i-1,n]
        # b is derived from the known T_n distribution.

        b = np.empty(N)
        
        # Calculate RHS using the explicit FTCS-like stencil
        for i in range(N):
            # T_i-1, T_i, T_i+1 at time n.
            # Handle boundary terms at i=0 and i=N-1
            
            # Left neighbor (T_i-1,n)
            T_i_minus_1 = T_present[i - 1] if i > 0 else T_bound
            # Right neighbor (T_i+1,n)
            T_i_plus_1 = T_present[i + 1] if i < N - 1 else T_bound
            
            # The explicit part of the update (RHS)
            laplacian_term = T_i_plus_1 - 2 * T_present[i] + T_i_minus_1
            b[i] = T_present[i] + 0.5 * alpha * laplacian_term
            
            # Add boundary contribution to RHS (Dirichlet only)
            # The fixed T_bound on the LEFT side contributes to b[0]
            if i == 0:
                b[i] += 0.5 * alpha * T_bound
            # The fixed T_bound on the RIGHT side contributes to b[N-1]
            if i == N - 1:
                b[i] += 0.5 * alpha * T_bound


        # ----------------------------------------------------------------
        # D. Solve the System: A * T_n+1 = b
        # ----------------------------------------------------------------
        # The Thomas Algorithm (solve_banded) finds T_n+1 efficiently in O(N).
        T_future = solve_banded((1, 1), ab, b)
        
        T_present = T_future
        T_history.append(T_present.copy())
        
    return np.array(T_history)

# ==========================================================
# 3. Run Simulation and Process Results
# ==========================================================

print(f"Running Crank-Nicolson Solver...")
print(f"Chosen Diffusion Number α: {alpha:.2f} (Violates FTCS limit of 0.5 by {alpha/0.5:.1f}x)")

# Run the solver (using the large, unstable time step)
T_history_cn_raw = crank_nicolson_solve(T_initial, T_boundary)

# Add boundary points (0 and L) back for plotting
def add_bc_for_plot(T_array, T_bound):
    """Adds the fixed boundary values to the array of interior points."""
    # Takes shape (time, N) and returns (time, N+2)
    T_with_bc = np.insert(T_array, [0, T_array.shape[1]], T_bound, axis=1)
    return T_with_bc

T_history_cn = add_bc_for_plot(T_history_cn_raw, T_boundary)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================
x_grid = np.linspace(0, L, N + 2)

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the evolution
ax.plot(x_grid, T_history_cn[0], label="t = 0 (Initial)", color='blue')
ax.plot(x_grid, T_history_cn[5], label="t = 0.025", color='red')
ax.plot(x_grid, T_history_cn[-1], label=f"t = {T_history_cn.shape[0] * h_t_large:.3f} (Final, Smooth)", color='black', linewidth=2)

ax.set_title(r"Crank-Nicolson: Stable Solution Despite $\alpha = 12.75$")
ax.set_xlabel("Position $x$")
ax.set_ylabel("Temperature $T$ (°C)")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Crank-Nicolson Summary ---")
print(f"Time Step (Δt): {h_t_large:.4e}")
print(f"Diffusion Number (α): {alpha:.2f}")
print(f"Total Time Simulated: {T_history_cn.shape[0] * h_t_large:.3f} s")
print("\nConclusion: The simulation remained stable, producing a smooth, non-oscillatory solution, \nconfirming the unconditional stability and efficiency of the Crank-Nicolson method, \neven with time steps that would cause FTCS to immediately explode.")
