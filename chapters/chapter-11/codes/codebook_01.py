import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 11 Codebook: Parabolic PDEs
# Project 1: CFL Stability Crisis (FTCS vs. Explosion)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and FTCS Solver Function
# ==========================================================
# Physical parameters
L = 1.0          # Length of the rod (m)
Nx = 50          # Number of interior spatial grid points
h_x = L / (Nx + 1) # Spatial step size (Δx)
D = 1.0          # Thermal diffusivity (m²/s)

# Thermal conditions
T_initial = 100.0  # Initial temperature of the rod's interior (°C)
T_boundary = 0.0   # Fixed boundary temperature at both ends (Dirichlet BCs)

def ftcs_solve(h_t, t_final, D_const, T_init, T_bound, h_x_local):
    """
    Solves the 1D transient heat equation using the Explicit FTCS method.
    """
    N_total = Nx + 2 # Grid size including boundaries
    
    # Compute diffusion number (stability parameter)
    alpha = D_const * h_t / (h_x_local ** 2)

    # Initialize temperature field (including boundaries)
    T_present = np.full(N_total, T_init)
    T_present[0] = T_present[N_total - 1] = T_bound

    # Store the temporal evolution
    T_history = [T_present.copy()]
    time = 0.0

    # --- Stability check ---
    is_stable = alpha <= 0.5
    print(f"  Diffusion Number α: {alpha:.4f}. Stable: {is_stable}")

    # ==========================================================
    # Time integration loop
    # ==========================================================
    while time < t_final:
        T_future = T_present.copy()
        
        # Apply FTCS update for all interior points (1 ≤ i ≤ Nx)
        for i in range(1, N_total - 1):
            # T_n+1 = T_n + alpha * (T_i+1,n - 2T_i,n + T_i-1,n)
            T_future[i] = T_present[i] + alpha * (
                T_present[i + 1] - 2 * T_present[i] + T_present[i - 1]
            )

        # Reapply boundary conditions (Dirichlet)
        T_future[0] = T_future[N_total - 1] = T_bound

        # Advance to next time step
        T_present = T_future
        time += h_t
        T_history.append(T_present.copy())
        
        # Check for numerical explosion
        if np.max(np.abs(T_present)) > 1000 and not is_stable:
             print("  --- EXPLOSION DETECTED (Max T > 1000) ---")
             break

    return np.array(T_history)

# ==========================================================
# 2. Run Simulation Cases
# ==========================================================
# A. Stable Case (α = 0.5)
h_t_stable = 0.5 * (h_x**2) / D
T_history_stable = ftcs_solve(h_t_stable, 0.1, D, T_initial, T_boundary, h_x)

# B. Unstable Case (α = 0.75, which is > 0.5)
h_t_unstable = 0.75 * (h_x**2) / D
T_history_unstable = ftcs_solve(h_t_unstable, 0.1, D, T_initial, T_boundary, h_x)

# ==========================================================
# 3. Visualization and Analysis
# ==========================================================
x_grid = np.linspace(0, L, Nx + 2)

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Stable Case (α = 0.5) ---
ax[0].plot(x_grid, T_history_stable[0], label="t = 0 (Initial)", color='blue')
# Plot an intermediate time step
mid_idx_stable = T_history_stable.shape[0] // 3
ax[0].plot(x_grid, T_history_stable[mid_idx_stable], label=f"t = {mid_idx_stable * h_t_stable:.3f}", color='red')
ax[0].plot(x_grid, T_history_stable[-1], label="t = Final (Smooth)", color='black')

ax[0].set_title(r"Stable FTCS Solution ($\alpha = 0.5$)")
ax[0].set_xlabel("Position $x$")
ax[0].set_ylabel("Temperature $T$ (°C)")
ax[0].grid(True)
ax[0].legend()
ax[0].set_ylim(0, T_initial * 1.1)

# --- Plot 2: Unstable Case (α = 0.75) ---
# Plot only the first few steps before explosion
N_plot_unstable = min(T_history_unstable.shape[0], 10) 
for i in range(N_plot_unstable):
    ax[1].plot(x_grid, T_history_unstable[i], alpha=(i+1)/N_plot_unstable, color='orange')
    
ax[1].plot(x_grid, T_history_unstable[N_plot_unstable - 1], 'r-', linewidth=2, label="Final Exploding Step")
ax[1].set_title(r"Unstable FTCS Solution ($\alpha = 0.75 > 0.5$)")
ax[1].set_xlabel("Position $x$")
ax[1].set_ylabel("Temperature $T$ (°C)")
ax[1].grid(True)
ax[1].legend()
ax[1].set_ylim(-T_initial * 2, T_initial * 2) # Limit Y-axis for visible oscillations

plt.tight_layout()
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================
alpha_stable = D * h_t_stable / (h_x ** 2)
alpha_unstable = D * h_t_unstable / (h_x ** 2)

print("\n--- Stability Crisis Analysis ---")
print(f"Spatial step Δx: {h_x:.4e}")
print("-" * 50)
print(f"Case A: Stable (α = {alpha_stable:.4f})")
print(f"  Time step Δt: {h_t_stable:.4e}")
print(f"  Result: Smooth, physically correct cooling.")
print("-" * 50)
print(f"Case B: Unstable (α = {alpha_unstable:.4f})")
print(f"  Time step Δt: {h_t_unstable:.4e}")
print(f"  Result: Immediate growth of non-physical oscillations (numerical explosion).")
