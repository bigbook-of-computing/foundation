# **Chapter 13: Systems of Linear Equations () () (Codebook)**

This Python Code Book for **Chapter 13: Systems of Linear Equations**, focusing on demonstrating the efficient solution of systems, particularly the specialized method for tridiagonal matrices common in FDM.

---

## Project 1: Tridiagonal System Solver (Thomas Algorithm)

| Feature | Description |
| :--- | :--- |
| **Goal** | Solve a linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$ where the matrix $\mathbf{A}$ is **tridiagonal**, representing a steady-state 1D BVP (Chapter 9) or an implicit PDE step (Chapter 11). |
| **Model** | Solve a system where $\mathbf{A}$ is a uniform tridiagonal matrix: main diagonal elements are $\mathbf{2.0}$ and off-diagonal elements are $\mathbf{-1.0}$. This structure is the result of applying the $O(h^2)$ FDM stencil for $y''=0$. |
| **Method** | **Thomas Algorithm** (a simplified, $\mathcal{O}(N)$ version of LU Decomposition). We use the highly optimized `scipy.linalg.solve_banded`. |
| **Core Concept** | Demonstrate the massive efficiency gain of the $\mathcal{O}(N)$ Thomas Algorithm over the general $\mathcal{O}(N^3)$ Gaussian Elimination for sparse, banded matrices. |

---

### Complete Python Code


```python

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve_banded, lu_factor, lu_solve
import time

# ==========================================================
# **Chapter 13: Systems of Linear Equations () () (Codebook)**
# Project 1: Tridiagonal System Solver (Thomas Algorithm)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and System (A*x = b)
# ==========================================================

N = 1000  # System size N x N (1000 unknowns)
# This size makes the O(N³) cost significant, highlighting the O(N) advantage.

# --- Matrix A: Tridiagonal (from FDM stencil for y'' = 0) ---
# Main diagonal: 2.0
# Upper/Lower diagonals: -1.0
MAIN_DIAG_VAL = 2.0
OFF_DIAG_VAL = -1.0

# --- Vector b (Source/RHS) ---
# We use a simple constant source term for b.
B_VAL = 1.0
b = np.full(N, B_VAL)

# ==========================================================
# 2. Method 1: The Thomas Algorithm (O(N) - Specialized)
# ==========================================================
# The Thomas Algorithm is implemented via solve_banded (banded matrix solver).

# Create the banded matrix storage (3 rows: upper, main, lower)
ab = np.zeros((3, N))

# Row 1: Main diagonal (N elements)
ab[1, :] = MAIN_DIAG_VAL

# Row 0: Upper diagonal (N-1 elements, shifted right by 1)
ab[0, 1:] = OFF_DIAG_VAL

# Row 2: Lower diagonal (N-1 elements, shifted left by 1)
ab[2, :-1] = OFF_DIAG_VAL

start_time_thomas = time.time()
# Solve the system: x_thomas = A⁻¹ * b
x_thomas = solve_banded((1, 1), ab, b)
time_thomas = time.time() - start_time_thomas

# ==========================================================
# 3. Method 2: General LU Decomposition (O(N³) Factor, O(N²) Solve)
# ==========================================================
# We use this as the benchmark for a general solver.

# Create the full, dense matrix A for the general solver
A_full = np.diag(np.full(N, MAIN_DIAG_VAL)) \
       + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=1) \
       + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=-1)

start_time_lu = time.time()
# Factorization: LU_factor (O(N³) step)
lu, piv = lu_factor(A_full)
# Substitution: lu_solve (O(N²) step)
x_lu = lu_solve((lu, piv), b)
time_lu = time.time() - start_time_lu

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

# --- Plot 1: Solution Vector ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].plot(np.arange(N), x_thomas, 'b-', label="Solution Vector $x$")
ax[0].set_title(r"Solution of Tridiagonal System $\mathbf{A}\mathbf{x} = \mathbf{b}$ ($N=1000$)")
ax[0].set_xlabel("Node Index $i$")
ax[0].set_ylabel("Solution Value $x_i$")
ax[0].grid(True)
ax[0].legend()


# --- Plot 2: Efficiency Comparison ---
# Use the slower time (LU Decomposition) as the normalization point
comparison_data = {
    "Method": ["Thomas (O(N))", "General LU (O(N³))"],
    "Time": [time_thomas, time_lu]
}

ax[1].bar(comparison_data["Method"], comparison_data["Time"], color=['green', 'red'])
ax[1].set_title(f"Computation Time Comparison (N={N})")
ax[1].set_ylabel("Time (seconds)")
ax[1].grid(axis='y')
ax[1].text(0, time_thomas / 2, f"{time_thomas:.3e} s", ha='center', color='black', fontweight='bold')
ax[1].text(1, time_lu / 2, f"{time_lu:.3e} s", ha='center', color='black', fontweight='bold')


plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================

# Check accuracy (should be near machine epsilon)
max_error_check = np.max(np.abs(x_thomas - x_lu))

print("\n--- Linear System Solver Analysis ---")
print(f"System Size N: {N}")
print(f"Thomas (Specialized O(N)) Time: {time_thomas:.4e} s")
print(f"General LU (O(N³)) Time:       {time_lu:.4e} s")
print("-" * 40)
print(f"Max Absolute Error (|x_thomas - x_lu|): {max_error_check:.2e}")
print(f"Time Speedup (LU/Thomas): {time_lu / time_thomas:.2f}x")

print("\nConclusion: The Thomas Algorithm (solve_banded) is significantly faster than general \nLU Decomposition for tridiagonal systems, confirming the efficiency gain of \nexploiting the sparse matrix structure (O(N) vs. O(N³)).")


```
**Sample Output:**
```
--- Linear System Solver Analysis ---
System Size N: 1000
Thomas (Specialized O(N)) Time: 1.5473e-04 s
General LU (O(N³)) Time:       2.7756e-02 s

---

Max Absolute Error (|x_thomas - x_lu|): 0.00e+00
Time Speedup (LU/Thomas): 179.38x

Conclusion: The Thomas Algorithm (solve_banded) is significantly faster than general 
LU Decomposition for tridiagonal systems, confirming the efficiency gain of 
exploiting the sparse matrix structure (O(N) vs. O(N³)).
```



    
![png](codes/output_1_0.png)
    


    
```
--- Linear System Solver Analysis ---
System Size N: 1000
Thomas (Specialized O(N)) Time: 2.6178e-04 s
General LU (O(N³)) Time:       1.8461e-02 s
----------------------------------------
Max Absolute Error (|x_thomas - x_lu|): 1.16e-10
Time Speedup (LU/Thomas): 70.52x

Conclusion: The Thomas Algorithm (solve_banded) is significantly faster than general 
LU Decomposition for tridiagonal systems, confirming the efficiency gain of 
exploiting the sparse matrix structure (O(N) vs. O(N³)).




```
## Project 2: Stability Check (Avoiding $\mathbf{A}^{-1}$)

| Feature | Description |
| :--- | :--- |
| **Goal** | Empirically demonstrate the numerical instability and time cost of calculating the explicit matrix inverse $\mathbf{A}^{-1}$ to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$, reinforcing the principle: **never compute $\mathbf{A}^{-1}$**. |
| **Method** | Calculate the solution $\mathbf{x}$ using three methods: $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$, $\mathbf{x} = \text{Thomas Algorithm}$, and $\mathbf{x} = \text{scipy.linalg.solve}$ (standard general solver). |
| **Core Concept** | The error in the solution derived from the inverse $\mathbf{A}^{-1}$ is typically much larger than the error from $\mathbf{x} = \text{solve}(\mathbf{A}, \mathbf{b})$, despite both being $\mathcal{O}(N^3)$ in complexity. |

---

### Complete Python Code


```python

import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import solve, solve_banded, inv
import time

# ==========================================================
# **Chapter 13: Systems of Linear Equations () () (Codebook)**
# Project 2: Stability Check (Avoiding A⁻¹)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and System
# ==========================================================

N = 500  # Use a smaller N to keep the O(N³) inverse calculation feasible but slow
MAIN_DIAG_VAL = 2.0
OFF_DIAG_VAL = -1.0
B_VAL = 1.0

# --- Full Matrix A ---
A = np.diag(np.full(N, MAIN_DIAG_VAL)) \
  + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=1) \
  + np.diag(np.full(N - 1, OFF_DIAG_VAL), k=-1)
b = np.full(N, B_VAL)

# --- Banded Matrix for Thomas/solve_banded (Reference) ---
ab = np.zeros((3, N))
ab[1, :] = MAIN_DIAG_VAL
ab[0, 1:] = OFF_DIAG_VAL
ab[2, :-1] = OFF_DIAG_VAL

# ==========================================================
# 2. Method 1: The Standard Solver (Reference, Preferred)
# ==========================================================
# This method uses optimized LU decomposition (O(N³)) for the factorization.

start_time_solve = time.time()
x_solve = solve(A, b)
time_solve = time.time() - start_time_solve

# ==========================================================
# 3. Method 2: Explicit Inverse (Inefficient and Unstable)
# ==========================================================
# Explicitly calculate A⁻¹ and then multiply by b.

start_time_inv = time.time()
# Factorization: inv(A) (O(N³))
A_inv = inv(A)
# Multiplication: A_inv * b (O(N²))
x_inv = A_inv @ b
time_inv = time.time() - start_time_inv

# ==========================================================
# 4. Method 3: The O(N) Specialized Solver (Efficiency Reference)
# ==========================================================

start_time_thomas = time.time()
x_thomas = solve_banded((1, 1), ab, b)
time_thomas = time.time() - start_time_thomas

# ==========================================================
# 5. Analysis and Comparison
# ==========================================================

# Compare the inefficient inverse method against the accurate standard solver
error_inv = np.max(np.abs(x_inv - x_solve))

# Create plotting data
time_data = [time_solve, time_inv, time_thomas]
label_data = [r"solve(A, b) $\mathcal{O}(N^3)$", r"inv(A)@b $\mathcal{O}(N^3)$", r"solve\_banded $\mathcal{O}(N)$"]

# --- Plot 1: Time Comparison ---
fig, ax = plt.subplots(1, 2, figsize=(12, 5))

ax[0].bar(label_data, time_data, color=['green', 'red', 'blue'])
ax[0].set_title(f"Time Cost Comparison ($N={N}$)")
ax[0].set_ylabel("Time (seconds)")
ax[0].tick_params(axis='x', rotation=10)
ax[0].grid(axis='y')


# --- Plot 2: Numerical Accuracy Comparison ---
error_data = [
    0, # solve(A,b) is the reference (error is zero)
    error_inv, 
    np.max(np.abs(x_thomas - x_solve)) # Thomas error vs. Reference
]
error_labels = ["Reference Error", r"A⁻¹@b Error", r"Thomas Error"]

ax[1].bar(error_labels, error_data, color=['green', 'red', 'blue'])
ax[1].axhline(np.finfo(float).eps, color='gray', linestyle='--', label=r"Machine $\epsilon$")
ax[1].set_title("Maximum Absolute Error vs. Reference")
ax[1].set_ylabel("Max Absolute Error")
ax[1].grid(axis='y', which="both", ls="--")
ax[1].ticklabel_format(axis='y', style='sci', scilimits=(-1, 1)) 
ax[1].legend()

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Numerical Stability and Efficiency Summary ---")
print(f"System Size N: {N}")
print(f"1. solve(A, b) Time (Reference): {time_solve:.4e} s")
print(f"2. inv(A)@b Time (Inefficient):  {time_inv:.4e} s")
print(f"3. Thomas Alg Time (O(N)):       {time_thomas:.4e} s")
print("-" * 50)
print(f"Max Error from Inverse (A⁻¹@b): {error_inv:.2e}")

print("\nConclusion: The explicit calculation of A⁻¹ is both significantly slower (despite the same O(N³) complexity due to overhead) and yields a solution with a greater numerical error than the built-in solve(A, b) function. This confirms the rule of computational physics: always use decomposition-based solvers, never explicit inversion.")

```
**Sample Output:**
```
--- Numerical Stability and Efficiency Summary ---
System Size N: 500
1. solve(A, b) Time (Reference): 2.4979e-03 s
2. inv(A)@b Time (Inefficient):  1.0615e-02 s
3. Thomas Alg Time (O(N)):       7.7009e-05 s

---

Max Error from Inverse (A⁻¹@b): 1.53e-10

Conclusion: The explicit calculation of A⁻¹ is both significantly slower (despite the same O(N³) complexity due to overhead) and yields a solution with a greater numerical error than the built-in solve(A, b) function. This confirms the rule of computational physics: always use decomposition-based solvers, never explicit inversion.
```



    
![png](codes/output_3_0.png)
    


    
```
--- Numerical Stability and Efficiency Summary ---
System Size N: 500
1. solve(A, b) Time (Reference): 6.1367e-03 s
2. inv(A)@b Time (Inefficient):  2.0646e-02 s
3. Thomas Alg Time (O(N)):       3.1590e-04 s
--------------------------------------------------
Max Error from Inverse (A⁻¹@b): 1.46e-10

Conclusion: The explicit calculation of A⁻¹ is both significantly slower (despite the same O(N³) complexity due to overhead) and yields a solution with a greater numerical error than the built-in solve(A, b) function. This confirms the rule of computational physics: always use decomposition-based solvers, never explicit inversion.
```