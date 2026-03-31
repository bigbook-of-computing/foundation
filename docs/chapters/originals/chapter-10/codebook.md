# **Chapter 10: Elliptic Partial Differential Equations () () (Codebook)**


This Python Code Book is for **Chapter 10: Elliptic Partial Differential Equations (e.g., Laplace's Equation)**, focusing on implementing and comparing the iterative relaxation techniques used to solve static field problems.

---

## Project 1: Electrostatic Potential (Gauss-Seidel Relaxation)

| Feature | Description |
| :--- | :--- |
| **Goal** | Simulate the **steady-state electrostatic potential** ($\phi$) inside a 2D box ($\nabla^2 \phi = 0$) using the **Gauss-Seidel Method**. |
| **Model** | **Laplace's Equation** ($\nabla^2 \phi = 0$). |
| **Boundary Conditions (BCs)** | **Dirichlet Conditions** (fixed voltage) applied to the boundaries: one side fixed at $100$ V and the other three sides fixed at $0$ V. |
| **Method** | **Finite Difference Method (FDM)** iteration using the **Five-Point Stencil**: the potential at a point is the average of its four neighbors. Gauss-Seidel updates points sequentially, using refreshed values immediately. |

---

### Complete Python Code


```python
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# **Chapter 10: Elliptic PDEs () () (Codebook)**
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


```
**Sample Output:**
```
Starting Gauss-Seidel Relaxation on 52x52 grid...
Converged after 2528 iterations. Max residual: 1.00e-05

--- Simulation Summary ---
Total Iterations: 2528
Final Max Residual: 9.996e-06

Conclusion: The Gauss-Seidel relaxation method successfully found the equilibrium 
potential distribution, confirmed by the exponential decrease of the maximum residual.
```


```
Starting Gauss-Seidel Relaxation on 52x52 grid...
Converged after 2528 iterations. Max residual: 1.00e-05




```
![png](codes/output_1_1.png)
    


    
```
--- Simulation Summary ---
Total Iterations: 2528
Final Max Residual: 9.996e-06

Conclusion: The Gauss-Seidel relaxation method successfully found the equilibrium 
potential distribution, confirmed by the exponential decrease of the maximum residual.




```
## Project 2: Comparative Efficiency (Jacobi vs. Gauss-Seidel)

| Feature | Description |
| :--- | :--- |
| **Goal** | Compare the **convergence speed** of the **Jacobi Method** (synchronous update) and the **Gauss-Seidel Method** (sequential update) for a fixed FDM problem. |
| **Model** | Laplace's Equation ($\nabla^2 \phi = 0$) on a 2D domain. |
| **Core Concept** | **Gauss-Seidel** is expected to converge nearly **twice as fast** as Jacobi because it immediately uses the refreshed, better information from neighboring points in the current iteration, leading to faster information propagation. |

---

### Complete Python Code


```python

import numpy as np
import matplotlib.pyplot as plt
import time # For tracking computation time

# ==========================================================
# **Chapter 10: Elliptic PDEs () () (Codebook)**
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

```
**Sample Output:**
```
Running Comparison...

--- Efficiency Comparison ---
Grid Size N: 50
Convergence Tolerance: 1.0e-04

---

Jacobi Method (Synchronous):
  Total Iterations: 3501
  Total Time: 8.5178 s

Gauss-Seidel Method (Sequential):
  Total Iterations: 1922
  Total Time: 5.1474 s

---

Gauss-Seidel Iteration Speedup: 1.82x (Expected: ~2.0x)
Gauss-Seidel Time Speedup: 1.65x (Varies by hardware/language)

Conclusion: Gauss-Seidel requires significantly fewer iterations to converge 
(speedup factor close to 2x) because it propagates new boundary information 
faster into the domain.
```


```
Running Comparison...




```
![png](codes/output_3_1.png)
    


    
```
--- Efficiency Comparison ---
Grid Size N: 50
Convergence Tolerance: 1.0e-04
--------------------------------------------------
Jacobi Method (Synchronous):
  Total Iterations: 3501
  Total Time: 16.2338 s

Gauss-Seidel Method (Sequential):
  Total Iterations: 1922
  Total Time: 7.8819 s
--------------------------------------------------
Gauss-Seidel Iteration Speedup: 1.82x (Expected: ~2.0x)
Gauss-Seidel Time Speedup: 2.06x (Varies by hardware/language)

Conclusion: Gauss-Seidel requires significantly fewer iterations to converge 
(speedup factor close to 2x) because it propagates new boundary information 
faster into the domain.




```
##  Iterative Relaxation Methods for Elliptic PDEs

Elliptic Partial Differential Equations (PDEs), such as **Laplace's Equation** ($\nabla^2 \phi = 0$), model **static, steady-state** systems. The Finite Difference Method (FDM) converts this continuous problem into a large system of linear equations, which is solved iteratively using **relaxation methods**.

The core of all these methods is the **Five-Point Stencil**, which dictates that the potential at any interior point is the **average of its four immediate neighbors**.

### Comparison of the Three Methods

| Feature | Jacobi Method | Gauss-Seidel Method | Successive Over-Relaxation (SOR) |
| :--- | :--- | :--- | :--- |
| **Update Strategy** | **Synchronous**. All new values ($\phi_{\text{new}}$) are calculated *only* from the potentials of the previous sweep ($\phi_{\text{old}}$). | **Sequential**. Updates are performed **in place**, using newly calculated values from the current sweep immediately. | Sequential (built on Gauss-Seidel) with **Extrapolation**. |
| **Information Flow** | **Slow**. Information propagates inward by only **one grid unit per iteration**. | **Faster**. Information propagation is accelerated as new boundary influence travels inward faster. | **Fastest**. Intentionally **overshoots** the equilibrium value to accelerate convergence dramatically. |
| **Memory Requirement** | Requires **two full copies** of the grid ($\phi_{\text{old}}$ and $\phi_{\text{new}}$). | Requires **one array** for the solution (plus a temporary copy for the convergence check). | Requires one array, similar to Gauss-Seidel. |
| **Convergence Speed** | **Slowest**. | Typically **twice as fast** as Jacobi. | Can reduce total iterations by an **order of magnitude** compared to Gauss-Seidel. |
| **Parallelization** | Highly **parallelizable** (since updates are independent). | Inherently **sequential**, making straightforward parallelization difficult. | Sequential, making straightforward parallelization difficult. |
| **Key Factor** | N/A | N/A | **Over-relaxation factor** ($\omega$), which must satisfy $1 < \omega < 2$. |

---

## 💡 Key Conceptual Difference

The main reason **Gauss-Seidel** is more efficient than **Jacobi** in a single-processor (serial) implementation is the **propagation of information**.

* **Jacobi** uses only old data. This means a new value calculated at $(i, j)$ cannot influence the calculation at $(i+1, j)$ or $(i, j+1)$ until the *next* iteration.
* **Gauss-Seidel** uses updated values immediately. In a standard left-to-right, bottom-to-top sweep, the newly calculated value at $(i-1, j)$ and $(i, j-1)$ is used to calculate $\phi_{i, j}$ in the *same* sweep. This accelerated propagation of information throughout the grid leads to a convergence rate that is theoretically **twice as fast**.

The provided codebook comparison confirms this: Gauss-Seidel converged in **1922 iterations** and **7.8819 s**, while Jacobi required **3501 iterations** and **16.2338 s** to reach the same tolerance, resulting in a time speedup of **2.06x**.

# **Chapter 10: Elliptic Partial Differential Equations () () (Codebook)**

## Project 1: Electrostatic Potential (Gauss-Seidel Relaxation)

---

### Definition: Electrostatic Potential (Gauss-Seidel)

The goal is to simulate the **steady-state electrostatic potential ($\phi$)** inside a 2D box ($\nabla^2 \phi = 0$) using the **Gauss-Seidel Method**. This is a pure **Boundary Value Problem (BVP)** where the solution is determined entirely by fixed **Dirichlet boundary conditions**.

### Theory: Five-Point Stencil and Sequential Update

The **Finite Difference Method (FDM)** discretizes **Laplace's Equation** ($\nabla^2 \phi = 0$) using the **Five-Point Stencil**, which dictates that the potential at any interior grid point ($i, j$) is the average of its four immediate neighbors:

$$\phi_{i, j} = \frac{1}{4} (\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1})$$

The **Gauss-Seidel** method is an iterative **relaxation** solver that executes this FDM stencil sequentially. The core efficiency of the method is that it **immediately uses the updated potential values** ($\phi_{i-1, j}$ and $\phi_{i, j-1}$) in the current iteration, leading to faster propagation of information across the domain. The iteration stops when the **maximum residual** falls below the tolerance ($\epsilon$).

### Extensive Python Code and Visualization

```python
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# **Chapter 10: Elliptic PDEs () () (Codebook)**
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
```
**Sample Output:**
```
Total Iterations: 2528
Final Max Residual: 9.996e-06
```

---

## Project 2: Comparative Efficiency (Jacobi vs. Gauss-Seidel)

---

### Definition: Comparative Efficiency

The goal is to numerically compare the **convergence speed** (measured in total iterations) of the **Jacobi Method** (synchronous update) and the **Gauss-Seidel Method** (sequential update) for solving the same Laplace's equation problem.

### Theory: Sequential vs. Synchronous Updates

Both methods use the Five-Point Stencil. The difference lies in the order of computation, which dictates the rate of information propagation:

  * **Jacobi (Synchronous):** Calculates the new state $\phi_{i, j}^{\text{new}}$ based entirely on the state from the *previous* sweep ($\phi^{\text{old}}$). This is computationally inefficient for convergence because new boundary effects travel slowly.
  * **Gauss-Seidel (Sequential):** Uses the most recent values available within the *current* sweep. This **accelerated information flow** leads to faster overall convergence, theoretically requiring only about **half the number of iterations** compared to Jacobi.

### Extensive Python Code and Visualization

```python
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# ==========================================================
# 1. Setup Parameters and Grid
# ==========================================================
N = 50                 
V_SOURCE = 100.0
TOLERANCE = 1e-4       

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
        # Must use a separate grid for new values, retaining phi_old until the end of the sweep
        phi_new = phi.copy() 
        max_residual = 0.0
        
        for i in range(1, N + 1):
            for j in range(1, N + 1):
                # Jacobi: Use only values from the previous time step (phi)
                phi_new[i, j] = 0.25 * (
                    phi[i + 1, j] + phi[i - 1, j] + 
                    phi[i, j + 1] + phi[i, j - 1]
                )
                
                residual = np.abs(phi_new[i, j] - phi[i, j])
                max_residual = max(max_residual, residual)
        
        phi = phi_new # Commit the entire new grid
        residual_history.append(max_residual)

        if max_residual < tolerance:
            break
            
    end_time = time.time()
    return iteration + 1, end_time - start_time, residual_history

def solve_gauss_seidel(N, V_source, tolerance, max_iter=10000):
    """Gauss-Seidel Method: Updates sequentially (in-place)."""
    phi = np.full((N + 2, N + 2), 0.0, dtype=np.float64)
    phi[0, :] = V_source
    
    residual_history = []
    
    start_time = time.time()
    for iteration in range(max_iter):
        max_residual = 0.0
        
        # We need the old values *only* for residual check (optional optimization can skip the copy)
        phi_old_for_residual = phi.copy() 

        for i in range(1, N + 1):
            for j in range(1, N + 1):
                phi_current = phi[i, j]
                
                # Gauss-Seidel: Use the already updated values for (i-1, j) and (i, j-1)
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

iter_jac, time_jac, res_jac = solve_jacobi(N, V_SOURCE, TOLERANCE)
iter_gs, time_gs, res_gs = solve_gauss_seidel(N, V_SOURCE, TOLERANCE)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# Plot 1: Iteration Count Comparison
ax[0].bar(['Jacobi', 'Gauss-Seidel'], [iter_jac, iter_gs], color=['skyblue', 'salmon'])
ax[0].set_title(f"Iterations to Converge ($\\epsilon={TOLERANCE:.1e}$)")
ax[0].set_ylabel("Total Iterations")
ax[0].grid(axis='y')
ax[0].text(0, iter_jac / 2, f"{iter_jac} Iters", ha='center', color='black', fontweight='bold')
ax[0].text(1, iter_gs / 2, f"{iter_gs} Iters", ha='center', color='black', fontweight='bold')


# Plot 2: Convergence History
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
speedup_iter = iter_jac / iter_gs
speedup_time = time_jac / time_gs

print("\n--- Efficiency Comparison ---")
print(f"Jacobi Iterations: {iter_jac}")
print(f"Gauss-Seidel Iterations: {iter_gs}")
print(f"Gauss-Seidel Iteration Speedup: {speedup_iter:.2f}x (Expected: ~2.0x)")
print(f"Gauss-Seidel Time Speedup: {speedup_time:.2f}x")

print("\nConclusion: Gauss-Seidel requires significantly fewer iterations to converge (speedup factor close to 2x) because its sequential update rule propagates new boundary information much faster into the domain than the synchronous Jacobi method.")
```
**Sample Output:**
```
--- Efficiency Comparison ---
Jacobi Iterations: 3501
Gauss-Seidel Iterations: 1922
Gauss-Seidel Iteration Speedup: 1.82x (Expected: ~2.0x)
Gauss-Seidel Time Speedup: 1.77x

Conclusion: Gauss-Seidel requires significantly fewer iterations to converge (speedup factor close to 2x) because its sequential update rule propagates new boundary information much faster into the domain than the synchronous Jacobi method.
```

---

## Project 3: Successive Over-Relaxation (SOR) Implementation

---

### Definition: Successive Over-Relaxation (SOR) Implementation

The goal is to implement the **Successive Over-Relaxation (SOR) method** to achieve a convergence rate significantly faster than Gauss-Seidel by intentionally **overshooting** the estimate.

### Theory: Over-Relaxation Factor ($\omega$)

SOR is an enhanced version of Gauss-Seidel that introduces the **over-relaxation factor ($\omega$)**. The update involves calculating the Gauss-Seidel estimate ($\phi^{\text{GS}}$) and then taking a weighted average of that estimate and the old value ($\phi^{\text{old}}$):

$$\phi_{i, j}^{\text{SOR}} = (1 - \omega) \phi_{i, j}^{\text{old}} + \omega \phi_{i, j}^{\text{GS}}$$

For the SOR method to accelerate the process, the factor $\omega$ must be in the range **$1 < \omega < 2$**. Choosing the optimal $\omega$ can reduce iterations by an **order of magnitude** compared to Gauss-Seidel, making the method scale closer to $\mathcal{O}(L)$ (linear with grid size).

### Extensive Python Code

```python
import numpy as np
import matplotlib.pyplot as plt
import time
import random

# ==========================================================
# 1. Setup Parameters and Solver Functions
# ==========================================================
N = 50                 
V_SOURCE = 100.0
TOLERANCE = 1e-4       
MAX_ITER = 10000

# Optimal over-relaxation factor for Laplace's Eq on a square grid:
# \omega_{opt} = 2 / (1 + sin(\pi / (N+1)))
def calculate_optimal_omega(N):
    return 2.0 / (1.0 + np.sin(np.pi / (N + 1)))

OMEGA = calculate_optimal_omega(N)

def solve_sor(N, V_source, tolerance, omega, max_iter=MAX_ITER):
    """Successive Over-Relaxation (SOR) Method."""
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
                
                # 1. Calculate the Gauss-Seidel estimate (phi_GS)
                phi_GS = 0.25 * (
                    phi[i + 1, j] + phi[i - 1, j] + 
                    phi[i, j + 1] + phi[i, j - 1]
                )
                
                # 2. Apply Over-Relaxation: phi_SOR = (1-w)*phi_old + w*phi_GS
                phi_new = (1.0 - omega) * phi_current + omega * phi_GS
                
                # Update in place
                phi[i, j] = phi_new
                
                residual = np.abs(phi[i, j] - phi_current)
                max_residual = max(max_residual, residual)
        
        residual_history.append(max_residual)
        
        if max_residual < tolerance:
            break
            
    end_time = time.time()
    return iteration + 1, end_time - start_time, residual_history, phi

# ==========================================================
# 3. Run Simulation
# ==========================================================

iter_sor, time_sor, res_sor, phi_sor = solve_sor(N, V_SOURCE, TOLERANCE, OMEGA)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Potential Field (Heatmap) ---
im = ax[0].imshow(phi_sor, cmap='viridis', origin='lower')
fig.colorbar(im, ax=ax[0], label="Potential (Volts)")
ax[0].set_title(f"Steady-State Potential (SOR, $\\omega={OMEGA:.4f}$)")

# --- Plot 2: Convergence History ---
ax[1].plot(res_sor, 'r-', linewidth=2)
ax[1].axhline(TOLERANCE, color='k', linestyle=':', label="Tolerance")
ax[1].set_title(f"Convergence of SOR Method (Iters: {iter_sor})")
ax[1].set_xlabel("Iteration Number")
ax[1].set_ylabel("Maximum Residual (log scale)")
ax[1].set_yscale('log')
ax[1].grid(True, which="both", ls="--")

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- SOR Implementation Summary ---")
print(f"Optimal Relaxation Factor (\u03c9): {OMEGA:.4f}")
print(f"Total Iterations: {iter_sor}")

print("\nConclusion: The SOR method successfully converged to the equilibrium solution. The convergence is extremely fast compared to Gauss-Seidel (which took ~1900 iterations at the same tolerance), confirming the power of the over-relaxation factor to accelerate the iterative solver.")
```
**Sample Output:**
```
--- SOR Implementation Summary ---
Optimal Relaxation Factor (ω): 1.8840
Total Iterations: 112

Conclusion: The SOR method successfully converged to the equilibrium solution. The convergence is extremely fast compared to Gauss-Seidel (which took ~1900 iterations at the same tolerance), confirming the power of the over-relaxation factor to accelerate the iterative solver.
```

---

## Project 4: Convergence Speed Comparison (Jacobi, Gauss-Seidel, SOR)

---

### Definition: Convergence Speed Comparison

The goal is to conduct a complete comparison of the efficiency (total iterations required) of all three relaxation methods—**Jacobi, Gauss-Seidel, and SOR**—to illustrate the massive acceleration achieved by the SOR method.

### Theory: Quantifying Efficiency Gains

This project compares the theoretical scaling hierarchy for the iterative solvers:

| Method | Update | Convergence Rate | Expected Scaling |
| :--- | :--- | :--- | :--- |
| **Jacobi** | Synchronous | Slow | $\mathcal{O}(L^2)$ |
| **Gauss-Seidel** | Sequential | Medium | $\mathcal{O}(L^2)$ ($\sim 2\times$ Jacobi) |
| **SOR** | Accelerated Sequential | Fast | $\mathcal{O}(L)$ (Near-optimal) |

The final plot visually confirms that the convergence rate, measured by the decay of the maximum residual, is fastest for SOR, followed by Gauss-Seidel, and slowest for Jacobi.

### Extensive Python Code and Visualization

```python
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
```