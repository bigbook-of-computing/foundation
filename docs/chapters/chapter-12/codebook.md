# **Chapter 12: Hyperbolic PDEs (Codebook)**

---

This Codebook implements the numerical solutions for wave propagation. We demonstrate the **CFL stability boundary** for hyperbolic systems and provide the **plucked string** simulation, highlighting the **two-stage initialization** required for second-order time derivatives.

---

## Project 1: CFL Stability Crisis (Wave Equation)

| Component | Description |
| :--- | :--- |
| **Objective** | Demonstrate the conditional stability of the Wave Equation ($C = v\Delta t / \Delta x$). |
| **Mathematical Concept** | Explicit time-marching using the Central-Time Central-Space (CTCS) stencil. |
| **Experiment Setup** | 1D string with stationary Gaussian pulse; $C = 0.9$ (stable) vs $C = 1.1$ (unstable). |
| **Expected Behavior** | Stable propagation for $C \le 1$; catastrophic explosion for $C > 1$. |
| **Verification Goal** | Confirm the "Information Speed Limit" of the numerical grid. |

---

### Complete Python Code

```python

import numpy as np
import matplotlib.pyplot as plt

## ==========================================================

# **Chapter 12: Hyperbolic PDEs () () (Codebook)**

## Project 1: CFL Stability Crisis (Wave Equation)

## ==========================================================

## ==========================================================

## 1. Setup Initial Conditions (A Gaussian Pulse)

## ==========================================================

L = 1.0          # Length of the string (m)
Nx = 100         # Number of spatial grid points
v = 1.0          # Wave speed (m/s)
T_FINAL = 5.0    # Total simulation time (s)

h_x = L / (Nx + 1) # Spatial step size (Δx)
N_total = Nx + 2   # Grid size including boundaries

x_grid = np.linspace(0, L, N_total)
## Initial condition: A small Gaussian pulse near the center, released from rest.

def initial_gaussian(x):
    """Gaussian pulse, max amplitude 0.05, centered at L/4."""
    return 0.05 * np.exp(-((x - L / 4) / 0.05)**2)

## Initial velocity is zero (released from rest)

V_INITIAL = 0.0

## ==========================================================

## 2. FTCS Wave Solver Function

## ==========================================================

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

## ==========================================================

## 3. Run Comparison Cases

## ==========================================================

## A. Stable Case (C = 0.9, obeys C <= 1)

C_STABLE = 0.9
max_y_stable, N_steps_stable = ftcs_wave_solve(C_STABLE, T_FINAL, initial_gaussian, V_INITIAL, h_x, v)

## B. Unstable Case (C = 1.1, violates C <= 1)

C_UNSTABLE = 1.1
max_y_unstable, N_steps_unstable = ftcs_wave_solve(C_UNSTABLE, T_FINAL, initial_gaussian, V_INITIAL, h_x, v)

## Create a common time grid for plotting

time_stable = np.linspace(0, T_FINAL, len(max_y_stable))
time_unstable = np.linspace(0, T_FINAL, len(max_y_unstable))

## ==========================================================

## 4. Visualization and Analysis

## ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

## Plot the stability history

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

## Final Analysis

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

```
**Sample Output:**
```python
--- Stability Analysis Summary ---
Spatial Step (h_x): 9.9010e-03

---

Case A: Stable (C=0.9)
  Final Max Amplitude: 4.739e-02
  Result: Amplitude remains bounded (oscillates).

---

Case B: Unstable (C=1.1)
  Final Max Amplitude: 1.072e+01
  Steps before Explosion: 41 / 459
  Result: Exponential growth (explosion) due to CFL violation.
```




![png](codes/output_1_0.png)




```
--- Stability Analysis Summary ---
Spatial Step (h_x): 9.9010e-03
--------------------------------------------------
Case A: Stable (C=0.9)
  Final Max Amplitude: 4.739e-02
  Result: Amplitude remains bounded (oscillates).
--------------------------------------------------
Case B: Unstable (C=1.1)
  Final Max Amplitude: 1.072e+01
  Steps before Explosion: 41 / 459
  Result: Exponential growth (explosion) due to CFL violation.



```
## Project 2: Plucked String Simulation (Verlet and First Step)

| Component | Description |
| :--- | :--- |
| **Objective** | Simulate a fundamental **Plucked String** (Dirichlet BCs). |
| **Mathematical Concept** | Solving $\partial_t^2 y = v^2 \partial_x^2 y$ with a two-step initialization for $y(x, t=1)$. |
| **Experiment Setup** | Triangular initial profile; released from rest ($v_{init}=0$). |
| **Expected Behavior** | Separation into two counter-propagating waves; stable reflection at boundaries. |
| **Verification Goal** | Visualize harmonic motion and standing wave formation. |

---

### Complete Python Code

```python

import numpy as np
import matplotlib.pyplot as plt

## ==========================================================

# **Chapter 12: Hyperbolic PDEs () () (Codebook)**

## Project 2: Plucked String Simulation (Verlet and First Step)

## ==========================================================

## ==========================================================

## 1. Setup Parameters and Initial Conditions

## ==========================================================

L = 1.0           # Length of the string (m)
Nx = 100          # Number of interior spatial points
v = 1.0           # Wave speed (m/s)

h_x = L / (Nx + 1)  # Spatial step size (Δx)
C = 1.0             # Courant Number (C=1 for fastest stable simulation, C <= 1)
h_t = C * h_x / v   # Time step size (Δt)
C_sq = C**2

T_FINAL = 2.0     # Total simulation time (s) (One full period: 2L/v)
N_steps = int(T_FINAL / h_t)
N_total = Nx + 2

x_grid = np.linspace(0, L, N_total)

## Initial condition: A triangular plucked shape

PLUCK_HEIGHT = 0.05
PLUCK_POS = 0.2  # Pluck point (e.g., L/5)

def initial_plucked_shape(x):
    """Creates a triangular displacement profile."""
    return np.where(x <= PLUCK_POS,
                    PLUCK_HEIGHT * x / PLUCK_POS,
                    PLUCK_HEIGHT * (L - x) / (L - PLUCK_POS))

## Initial state: Plucked and released from rest (v_initial = 0)

y_past = initial_plucked_shape(x_grid) # y(n=0)
y_present = np.zeros_like(y_past)
V_INITIAL = 0.0 # Initial velocity is zero everywhere

## Store history for visualization

y_history = []

## ==========================================================

## 2. Initialization: The Special First Step (n=0 to n=1)

## ==========================================================

## Formula for v_i,0 = 0: y_i,1 = y_i,0 + (C^2 / 2) * [Laplacian]

print(f"Starting simulation with C={C:.2f} (Verlet/FTCS).")

for i in range(1, N_total - 1):
    laplacian_term = y_past[i+1] - 2 * y_past[i] + y_past[i-1]

    # Special formula for v_initial = 0
    y_present[i] = y_past[i] + 0.5 * C_sq * laplacian_term

## Boundary conditions y(0)=y(L)=0 are preserved

y_past[0] = y_past[-1] = 0.0
y_present[0] = y_present[-1] = 0.0

y_history.append(y_past.copy())
y_history.append(y_present.copy())

## ==========================================================

## 3. The Main Time March (FTCS / Verlet Loop, n >= 1)

## ==========================================================

for n in range(1, N_steps):
    y_future = np.zeros_like(y_past)

    for i in range(1, N_total - 1):
        laplacian_term = y_present[i+1] - 2 * y_present[i] + y_present[i-1]

        # FTCS (Verlet) Update Rule: y_n+1 = 2y_n - y_n-1 + C^2 * [Laplacian]
        y_future[i] = 2 * y_present[i] - y_past[i] + C_sq * laplacian_term

    # Advance the time levels
    y_past = y_present.copy()
    y_present = y_future.copy()
    y_history.append(y_present.copy())

## ==========================================================

## 4. Visualization and Analysis

## ==========================================================

## Select indices for plotting key moments in the wave cycle (e.g., reflection stages)

time_points = [0, N_steps // 4, N_steps // 2, N_steps - 1]
time_points_labels = [f"t = {idx * h_t:.2f} s" for idx in time_points]

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title(r"1D Wave Equation: Plucked String Simulation ($C = 1.0$)")
ax.set_xlabel("Position $x$")
ax.set_ylabel("Displacement $y$")
ax.set_ylim(-PLUCK_HEIGHT * 1.1, PLUCK_HEIGHT * 1.1)

## Plot the key stages of propagation and reflection

for idx, label in zip(time_points, time_points_labels):
    ax.plot(x_grid, y_history[idx], label=label)

ax.axhline(0, color='gray', linestyle='-')
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

## Final Analysis

print("\n--- Plucked String Simulation Summary ---")
print(f"Analytic Wave Period (2L/v): {2 * L / v:.2f} s")
print(f"Total Time Simulated: {T_FINAL:.2f} s")
print(f"Courant Number C: {C:.2f}")
print("\nConclusion: The string successfully simulated propagation and reflection over a full period \nwithout dissipation or explosion, validating the use of the explicit (Verlet-like) FTCS scheme \nunder the CFL constraint.")

```
**Sample Output:**
```python
Starting simulation with C=1.00 (Verlet/FTCS).

--- Plucked String Simulation Summary ---
Analytic Wave Period (2L/v): 2.00 s
Total Time Simulated: 2.00 s
Courant Number C: 1.00

Conclusion: The string successfully simulated propagation and reflection over a full period
without dissipation or explosion, validating the use of the explicit (Verlet-like) FTCS scheme
under the CFL constraint.
```


```
Starting simulation with C=1.00 (Verlet/FTCS).




```
![png](codes/output_3_1.png)




```
--- Plucked String Simulation Summary ---
Analytic Wave Period (2L/v): 2.00 s
Total Time Simulated: 2.00 s
Courant Number C: 1.00

Conclusion: The string successfully simulated propagation and reflection over a full period
without dissipation or explosion, validating the use of the explicit (Verlet-like) FTCS scheme
under the CFL constraint.
```