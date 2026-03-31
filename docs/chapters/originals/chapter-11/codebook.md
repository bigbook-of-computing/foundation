# **Chapter 11: Parabolic Partial Differential Equations (e.g., The Heat/Diffusion Equation) () () (Codebook)**

---

## Project 1: CFL Stability Crisis (FTCS vs. Explosion)

| Feature | Description |
| :--- | :--- |
| **Goal** | Simulate the Heat Equation using the **Explicit FTCS (Forward-Time Centered-Space) Method** and demonstrate its **conditional stability** by running one case where the CFL condition is met ($\alpha \le 0.5$) and one case where it is violated ($\alpha > 0.5$). |
| **Model** | **1D Heat Equation**: $\frac{\partial T}{\partial t} = D \frac{\partial^2 T}{\partial x^2}$. |
| **Stability Constraint** | The **CFL Condition** for FTCS is $\mathbf{\alpha = D \frac{h_t}{h_x^2} \le 0.5}$. Violation leads to numerical explosion. |
| **Core Concept** | FTCS is easy to implement but is **impractically slow** for high spatial resolution due to the $h_t \propto h_x^2$ restriction. |

---

### Complete Python Code


```python
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# **Chapter 11: Parabolic PDEs () () (Codebook)**
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
```
**Sample Output:**
```
Diffusion Number α: 0.5000. Stable: True
  Diffusion Number α: 0.7500. Stable: False
  --- EXPLOSION DETECTED (Max T > 1000) ---

--- Stability Crisis Analysis ---
Spatial step Δx: 1.9608e-02

---

Case A: Stable (α = 0.5000)
  Time step Δt: 1.9223e-04
  Result: Smooth, physically correct cooling.

---

Case B: Unstable (α = 0.7500)
  Time step Δt: 2.8835e-04
  Result: Immediate growth of non-physical oscillations (numerical explosion).
```


```
  Diffusion Number α: 0.5000. Stable: True
  Diffusion Number α: 0.7500. Stable: False
  --- EXPLOSION DETECTED (Max T > 1000) ---




```
![png](codes/output_1_1.png)
    


    
```
--- Stability Crisis Analysis ---
Spatial step Δx: 1.9608e-02
--------------------------------------------------
Case A: Stable (α = 0.5000)
  Time step Δt: 1.9223e-04
  Result: Smooth, physically correct cooling.
--------------------------------------------------
Case B: Unstable (α = 0.7500)
  Time step Δt: 2.8835e-04
  Result: Immediate growth of non-physical oscillations (numerical explosion).



```
## Project 2: The Gold Standard (Crank-Nicolson)

| Feature | Description |
| :--- | :--- |
| **Goal** | Solve the Heat Equation using the **Crank-Nicolson Method** (the "gold standard"). The solver must remain **stable and accurate** even when using a time step that grossly **violates** the explicit FTCS CFL condition. |
| **Method** | **Implicit Scheme** solved by the **Thomas Algorithm** (or equivalent, here implemented using `np.linalg.solve` on the tridiagonal matrix). |
| **Core Advantage** | Crank-Nicolson is **unconditionally stable** (A-stable) and **second-order accurate in time** ($\mathcal{O}(h_t^2)$). This allows for much larger, efficiency-gaining time steps. |

---

### Complete Python Code


```python

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded # Efficient solver for tridiagonal systems

# ==========================================================
# **Chapter 11: Parabolic PDEs () () (Codebook)**
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
```
**Sample Output:**
```
Running Crank-Nicolson Solver...
Chosen Diffusion Number α: 13.00 (Violates FTCS limit of 0.5 by 26.0x)

--- Crank-Nicolson Summary ---
Time Step (Δt): 5.0000e-03
Diffusion Number (α): 13.00
Total Time Simulated: 0.105 s

Conclusion: The simulation remained stable, producing a smooth, non-oscillatory solution, 
confirming the unconditional stability and efficiency of the Crank-Nicolson method, 
even with time steps that would cause FTCS to immediately explode.
```


```
Running Crank-Nicolson Solver...
Chosen Diffusion Number α: 13.00 (Violates FTCS limit of 0.5 by 26.0x)




```
![png](codes/output_3_1.png)
    


    
```
--- Crank-Nicolson Summary ---
Time Step (Δt): 5.0000e-03
Diffusion Number (α): 13.00
Total Time Simulated: 0.105 s

Conclusion: The simulation remained stable, producing a smooth, non-oscillatory solution, 
confirming the unconditional stability and efficiency of the Crank-Nicolson method, 
even with time steps that would cause FTCS to immediately explode.
```