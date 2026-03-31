
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 12 Codebook: Hyperbolic PDEs
# Project 1: CFL Stability Crisis (Wave Equation)
# ==========================================================

# ==========================================================
# 1. Setup Initial Conditions (A Gaussian Pulse)
# ==========================================================

L = 1.0          # Length of the string (m)
Nx = 100         # Number of spatial grid points
v = 1.0          # Wave speed (m/s)
T_FINAL = 5.0    # Total simulation time (s)

h_x = L / (Nx + 1) # Spatial step size (Δx)
N_total = Nx + 2   # Grid size including boundaries

x_grid = np.linspace(0, L, N_total)
# Initial condition: A small Gaussian pulse near the center, released from rest.
def initial_gaussian(x):
    """Gaussian pulse, max amplitude 0.05, centered at L/4."""
    return 0.05 * np.exp(-((x - L / 4) / 0.05)**2)

# Initial velocity is zero (released from rest)
V_INITIAL = 0.0 

# ==========================================================
# 2. FTCS Wave Solver Function
# ==========================================================

def ftcs_wave_solve(C_target, t_final, initial_shape, v_initial, h_x_local, v_wave):
    """
    Explicit FTCS solver for the 1D Wave Equation, demonstrating stability
    based on the Courant Number C.
    """
    # Calculate time step based on target C
    h_t = C_target * h_x_local / v_wave 
    C_sq = C_target**2
    
    # Calculate total steps and ensure grid size is consistent
    N_steps = int(t_final / h_t)
    
    # Initialize the grids
    y_past = initial_shape(x_grid) # y(n=0)
    y_present = np.zeros_like(y_past)
    
    # ------------------------------------------------------------------
    # Step 1: Special First Step (n=0 to n=1)
    # y_i,1 = y_i,0 + h_t*v_i,0 + (C^2/2) * [Laplacian]
    # ------------------------------------------------------------------
    # Since initial velocity v_i,0 = 0, the term h_t*v_i,0 vanishes.
    
    for i in range(1, N_total - 1):
        laplacian_term = y_past[i+1] - 2 * y_past[i] + y_past[i-1]
        y_present[i] = y_past[i] + 0.5 * C_sq * laplacian_term
        
    # Boundary conditions y(0)=y(L)=0 are inherently applied
    y_present[0] = y_present[-1] = 0.0

    # ------------------------------------------------------------------
    # Step 2: Main Time March (n >= 1)
    # y_n+1 = 2y_n - y_n-1 + C^2 * [Laplacian]
    # ------------------------------------------------------------------
    
    # Store history (only final state for stability check)
    max_displacement = [np.max(np.abs(y_past))] 
    
    for n in range(1, N_steps):
        y_future = np.zeros_like(y_past)

        for i in range(1, N_total - 1):
            laplacian_term = y_present[i+1] - 2 * y_present[i] + y_present[i-1]
            
            # FTCS (Verlet) Update Rule
            y_future[i] = 2 * y_present[i] - y_past[i] + C_sq * laplacian_term
        
        # Advance time levels
        y_past = y_present
        y_present = y_future
        
        # Check for explosion
        current_max_y = np.max(np.abs(y_present))
        max_displacement.append(current_max_y)
        if current_max_y > 10.0: # Arbitrary threshold for explosion
            break

    return np.array(max_displacement), N_steps

# ==========================================================
# 3. Run Comparison Cases
# ==========================================================

# A. Stable Case (C = 0.9, obeys C <= 1)
C_STABLE = 0.9
max_y_stable, N_steps_stable = ftcs_wave_solve(C_STABLE, T_FINAL, initial_gaussian, V_INITIAL, h_x, v)

# B. Unstable Case (C = 1.1, violates C <= 1)
C_UNSTABLE = 1.1
max_y_unstable, N_steps_unstable = ftcs_wave_solve(C_UNSTABLE, T_FINAL, initial_gaussian, V_INITIAL, h_x, v)

# Create a common time grid for plotting
time_stable = np.linspace(0, T_FINAL, len(max_y_stable))
time_unstable = np.linspace(0, T_FINAL, len(max_y_unstable))

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the stability history
ax.plot(time_stable, max_y_stable, 'b-', label=f"Stable Case ($C = {C_STABLE}$)")
ax.plot(time_unstable, max_y_unstable, 'r-', label=f"Unstable Case ($C = {C_UNSTABLE}$)")

ax.axhline(0.05, color='gray', linestyle=':', label="Initial Max Amplitude")

ax.set_title(r"CFL Stability Check for Explicit Wave Equation Solver")
ax.set_xlabel("Time (s)")
ax.set_ylabel("Max Displacement (Absolute Amplitude)")
ax.set_yscale('log') # Use log scale to clearly show exponential growth/boundedness
ax.grid(True, which="both", ls="--")
ax.legend()
plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Stability Analysis Summary ---")
print(f"Spatial Step (h_x): {h_x:.4e}")
print("-" * 50)
print(f"Case A: Stable (C={C_STABLE})")
print(f"  Final Max Amplitude: {max_y_stable[-1]:.3e}")
print(f"  Result: Amplitude remains bounded (oscillates).")
print("-" * 50)
print(f"Case B: Unstable (C={C_UNSTABLE})")
print(f"  Final Max Amplitude: {max_y_unstable[-1]:.3e}")
print(f"  Steps before Explosion: {len(max_y_unstable)} / {N_steps_unstable}")
print(f"  Result: Exponential growth (explosion) due to CFL violation.")
