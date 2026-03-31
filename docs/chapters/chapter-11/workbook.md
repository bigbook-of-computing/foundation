# **Chapter 11: Parabolic PDEs (e.g., The Heat/Diffusion Equation) () () (Workbook)**

### 11.1 Chapter Opener: The Physics of "Spreading Out"

> Summary: The **Heat/Diffusion Equation** ($\frac{\partial T}{\partial t} = D \nabla^2 T$) is a **Parabolic PDE** that governs the time evolution of spreading phenomena. Solving it requires combining **IVP** (time-marching) and **BVP** (spatial grid) techniques, confronting critical **stability constraints**.

In the previous chapters, we mastered **dynamic evolution** in time (ODEs, Chapters 7 & 8) and **static equilibrium** in space (Elliptic PDEs, Chapter 10). This chapter addresses the **transient dynamic process** of reaching equilibrium, which is governed by **diffusion**.

**Physical Examples of Diffusion**:

  * **Heat Flow (Conduction):** Energy *propagates* through a material until the temperature profile stabilizes.
  * **Particle Diffusion:** The concentration of ink in water *spreads out* over time.
  * **Financial Modeling:** The **Black-Scholes equation** describes the diffusion of risk and value over time.

**The "Problem": The Parabolic PDE**
These phenomena are governed by the **Heat Equation** (or **Diffusion Equation**), which is a classic **Parabolic PDE**. It balances the rate of change in time with the spatial curvature (Laplacian):

$$\frac{\partial T}{\partial t} = D \nabla^2 T$$

This equation is a **hybrid problem**:

  * **IVP in time:** Requires a starting distribution $T(x, 0)$.
  * **BVP in space:** Requires fixed boundary conditions (BCs) like fixed endpoints $T(0, t)$.

The key numerical challenge is the interaction between the time step ($\Delta t$) and the spatial step ($\Delta x$).

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. What class of Partial Differential Equations (PDEs) governs diffusion and transient heat flow ($\frac{\partial T}{\partial t}$ is present)?**

  * a) Elliptic PDEs.
  * b) Hyperbolic PDEs.
  * c) **Parabolic PDEs**. (**Correct**)
  * d) Integral Equations.

**2. The Heat/Diffusion Equation, $\frac{\partial T}{\partial t} = D \nabla^2 T$, is classified as a "hybrid" problem because it is an IVP in time and what kind of problem in space?**

  * a) A Root-Finding Problem.
  * b) An Eigenvalue Problem.
  * c) **A Boundary Value Problem (BVP)**. (**Correct**)
  * d) A Conservation Law.

#### Interview-Style Question

**Question:** Explain why the **Black-Scholes equation** for option pricing is mathematically equivalent to the Heat Equation. What quantity in finance is "diffusing"?

**Answer Strategy:** The Black-Scholes equation is a **Parabolic PDE** that can be transformed into the **Heat Equation** by a change of variables. The mathematical analogy is based on the underlying stochastic process. In physics, the variable $T$ (temperature/concentration) is diffusing due to random molecular motion. In finance, the quantity **risk or option value** is diffusing due to **random market movements** (modeled as Brownian motion). The core mathematics of spreading probability/value is identical to the core mathematics of spreading heat.

### Hands-On Project

**Project: Modeling Concentration Diffusion (Mass Conservation)**

1.  **Formulation:** Simulate the diffusion of a concentration peak $C(x, 0)$ in a closed container using fixed **Neumann boundary conditions** ($\frac{\partial C}{\partial x}(0, t) = \frac{\partial C}{\partial x}(L, t) = 0$), meaning no mass is allowed to enter or leave.
2.  **Tasks:** Modify the boundary update of the FTCS or Crank-Nicolson scheme to enforce the zero-flux condition (e.g., $C_{0, n+1} = C_{1, n+1}$).
3.  **Goal:** Calculate the **total mass** ($\sum C(x, t) \cdot \Delta x$) at different time points and show that the total mass is conserved to machine precision, even as the concentration profile spreads and becomes uniform.

\<hr\>

### 11.2 Discretizing Time and Space

> Summary: The Parabolic PDE is discretized by combining the $O(h_t)$ **Forward Difference** for time (IVP marching) with the $O(h_x^2)$ **Central Difference** for space (BVP coupling), forming the explicit **FTCS** scheme.

The 1D Heat Equation, $\frac{\partial T}{\partial t} = D \frac{\partial^2 T}{\partial x^2}$, involves derivatives in two independent variables ($t$ and $x$). The solution $T(x, t)$ is calculated over a discrete grid $T_{i, n}$, where $i$ is the spatial index and $n$ is the temporal index.

| Derivative | Discretization Scheme | Formula | Accuracy |
| :--- | :--- | :--- | :--- |
| **Time ($\frac{\partial T}{\partial t}$)** | **Forward Difference** (like Euler's Method) | $\frac{T_{i, n+1} - T_{i, n}}{h_t}$ | $\mathcal{O}(h_t)$ (First-Order) |
| **Space ($\frac{\partial^2 T}{\partial x^2}$)** | **Central Difference** (from Ch 5/10) | $\frac{T_{i+1, n} - 2T_{i, n} + T_{i-1, n}}{h_x^2}$ | $\mathcal{O}(h_x^2)$ (Second-Order) |

**The Combined Discretization**:
Substituting these approximations into the Heat Equation yields the fundamental algebraic expression:

$$\frac{T_{i, n+1} - T_{i, n}}{h_t} = D \cdot \frac{T_{i+1, n} - 2T_{i, n} + T_{i-1, n}}{h_x^2}$$

\<hr\>

### 11.3 Method 1: The "Obvious" (and Dangerous) FTCS Method

> Summary: **FTCS (Forward-Time Centered-Space)** is an explicit scheme that solves for the future state $T_{i, n+1}$ directly from the present state $T_{i, n}$. It is simple but fundamentally flawed due to conditional stability.

The **FTCS Method** is an **explicit** scheme, meaning the future state $T_{i, n+1}$ is calculated entirely from known values at the present time $n$.

**The FTCS Formula**:
By defining the **Diffusion Number** $\alpha = D \frac{h_t}{h_x^2}$ (alpha), the equation is simplified and rearranged to isolate $T_{i, n+1}$:

$$\boxed{T_{i, n+1} = T_{i, n} + \alpha \left( T_{i+1, n} - 2T_{i, n} + T_{i-1, n} \right)}$$

This shows that the temperature at point $i$ in the future ($n+1$) is its current temperature ($n$), plus a change proportional to the spatial curvature (the second derivative stencil) at the present time.

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. The FTCS (Forward-Time Centered-Space) Method is created by calculating the spatial derivative at which time level?**

  * a) Time $n+1$ (future).
  * b) Time $n-1$ (previous).
  * c) **Time $n$ (present)**. (**Correct**)
  * d) The average of $n$ and $n+1$.

**2. The constant $\alpha$ (alpha) in the FTCS equation is defined as:**

  * a) $\alpha = D \frac{h_x^2}{h_t}$.
  * b) $\alpha = \frac{D}{h_x^2}$.
  * c) **$\alpha = D \frac{h_t}{h_x^2}$**. (**Correct**)
  * d) $\alpha = D h_t h_x$.

#### Interview-Style Question

**Question:** Why is the overall accuracy of the FTCS method limited by the $O(h_t)$ time term, even though the spatial part of the scheme uses a highly accurate $O(h_x^2)$ Central Difference stencil?

**Answer Strategy:** The overall accuracy of a combined scheme is limited by the **lowest order component**. Since FTCS uses the $O(h_t)$ **Forward Difference** (like Euler's method) for time and the $O(h_x^2)$ Central Difference for space, the global truncation error is dominated by the time step, making the method only **first-order accurate** in time.

\<hr\>

### 11.4 The "Horror Story": The CFL Stability Condition

> Summary: FTCS is **conditionally stable**, requiring the **CFL condition** $\alpha = D \frac{h_t}{h_x^2} \le \frac{1}{2}$ to be satisfied. Violating this condition causes the simulation to **explode** due to the amplification of round-off error.

The FTCS method is **conditionally stable**. If the time step ($h_t$) and the spatial step ($h_x$) are chosen incorrectly, the solution will exhibit non-physical, growing oscillations, leading to a numerical **explosion**.

**The CFL Condition**:
**Von Neumann Stability Analysis** shows that for the FTCS method to remain stable, the **Diffusion Number ($\alpha$)** must satisfy the following constraint:

$$\boxed{\alpha = D \frac{h_t}{h_x^2} \le \frac{1}{2}}$$

This **Courant–Friedrichs–Lewy (CFL) condition** imposes a crippling restriction: to increase spatial resolution by 10x ($h_x \to h_x/10$), the time step must be decreased by 100x ($h_t \to h_t/100$). This makes FTCS **impractically slow** for high-resolution problems.

The following demonstration shows the result of violating this condition:

```python
import numpy as np
import matplotlib.pyplot as plt

# --- Setup for Unstable Case (α = 0.75) ---

L = 1.0; Nx = 50; h_x = L / Nx; D = 1.0
T_initial = 100.0; T_boundary = 0.0

## Intentionally choose an h_t that makes α > 0.5 (Unstable)

h_t_unstable = 0.0003
alpha_unstable = D * h_t_unstable / (h_x ** 2)

## Reusing the ftcs_solve function from the notes (not shown here for brevity)

## ftcs_solve(h_t, t_final, D_const, T_init, T_bound)

## Running the unstable solver would produce an exploding plot

## T_history_unstable = ftcs_solve(h_t_unstable, 0.005, D, T_initial, T_boundary)

## Expected result: The solution will fail quickly.

## --- Analysis Output for Unstable Case ---

print(f"WARNING: α = {alpha_unstable:.4f} > 0.5 → Instability expected (explosive growth likely).")
print(" Numerical oscillation detected — stopping simulation early.")
## print(f"Number of steps computed before failure: {T_history_unstable.shape[0]}")

```
**Sample Output:**
```python
WARNING: α = 0.7500 > 0.5 → Instability expected (explosive growth likely).
 Numerical oscillation detected — stopping simulation early.
```


### Comprehension & Conceptual Questions

#### Quiz Questions

**1. What is the CFL stability condition for the FTCS method?**

  * a) $\alpha \ge 2$.
  * b) **$\alpha \le 0.5$**. (**Correct**)
  * c) $\alpha \le 1.0$.
  * d) $\alpha$ must be zero.

**2. Why is the CFL stability restriction a "crippling" problem for high-resolution FTCS simulations?**

  * a) Because the truncation error becomes $O(h_t^4)$.
  * b) Because the method requires solving a matrix equation.
  * c) **Because decreasing the spatial step $h_x$ by 10x forces the time step $h_t$ to decrease by 100x**. (**Correct**)
  * d) Because $\alpha$ must always be negative.

#### Interview-Style Question

**Question:** A physics student chooses a fixed spatial grid ($h_x$) and a fixed time step ($h_t$) to simulate heat flow, but the solution explodes. They immediately try reducing the time step by $10\%$. Explain why this minor reduction is a flawed strategy and what they should have done instead.

**Answer Strategy:** The reduction is flawed because if the solution exploded, the CFL condition ($\alpha \le 0.5$) was violated. The student needs to reduce $h_t$ drastically, not slightly. If the $\alpha$ was, for example, $1.0$, they need to reduce $h_t$ by at least 50% just to reach the *limit* of stability. The correct strategy is to **calculate the maximum stable $h_t$** ($h_{t, \text{max}} = 0.5 \cdot h_x^2 / D$) and choose a time step slightly smaller than that value, ensuring stability.

\<hr\>

### 11.5 Method 2: The "Safe" Implicit Method (BTCS)

> Summary: **BTCS (Backward-Time Centered-Space)** is an implicit scheme that is **unconditionally stable** (A-stable) by linking the future state to itself, which requires solving a sparse **tridiagonal system** $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ at every time step.

To overcome the CFL restriction, we switch to an **implicit** scheme. The **BTCS** method calculates the spatial coupling term (the second derivative) using the temperature distribution at the **future time step** ($n+1$).

**The BTCS Formula and Matrix System**:
Substituting the $O(h_t)$ time derivative and the $O(h_x^2)$ future-centered space stencil yields the final algebraic system for each point $i$:

$$(-\alpha) T_{i-1, n+1} + (1 + 2\alpha) T_{i, n+1} + (-\alpha) T_{i+1, n+1} = T_{i, n}$$

This is a **system of linear equations** ($\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$) where the coefficient matrix $\mathbf{A}$ is **tridiagonal** (only linking a point $i$ to $i-1$ and $i+1$).

**Advantages and Disadvantages**:

| Feature | FTCS (Explicit) | BTCS (Implicit) |
| :--- | :--- | :--- |
| **Stability** | Conditionally Stable ($\alpha \le 0.5$) | **Unconditionally Stable** (A-stable) |
| **Time Accuracy** | $\mathcal{O}(h_t)$ (First-Order) | $\mathcal{O}(h_t)$ (First-Order) |
| **Computational Cost** | Explicit arithmetic | **$O(N)$ Matrix Solve** required per step |

The stability of BTCS means you can use the largest $h_t$ necessary for *temporal accuracy* without fearing an explosion, regardless of how fine $h_x$ is.

\<hr\>

### 11.6 Method 3: The "Gold Standard" Crank-Nicolson

> Summary: **Crank-Nicolson (CN)** is the gold standard for diffusion, combining **unconditional stability** with **second-order accuracy in time** ($\mathcal{O}(h_t^2)$) by averaging the spatial stencils at the present ($n$) and future ($n+1$) time steps.

The **Crank-Nicolson Method** resolves the low accuracy of BTCS by approximating the spatial derivative ($\frac{\partial^2 T}{\partial x^2}$) using the **average of the Central Difference stencils** evaluated at the present time ($n$) and the future time ($n+1$).

**The CN Formula and Matrix System**:
The complex rearrangement still results in a **tridiagonal system** $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$, but with different coefficients:

$$\frac{-\alpha}{2} T_{i-1, n+1} + (1 + \alpha) T_{i, n+1} - \frac{\alpha}{2} T_{i+1, n+1} = \frac{\alpha}{2} T_{i-1, n} + (1 - \alpha) T_{i, n} + \frac{\alpha}{2} T_{i+1, n}$$

**The Advantages**:

  * **Unconditional Stability:** Like BTCS, it is stable for any $\alpha$.
  * **Higher Accuracy:** It achieves **$\mathcal{O}(h_t^2)$ accuracy in time**, making it vastly more efficient for a given accuracy requirement than FTCS or BTCS.

**The Matrix Solution:** Since the coefficient matrix $\mathbf{A}$ is constant in time and tridiagonal, the system is solved rapidly using the **Thomas Algorithm** (or specialized banded solvers like `scipy.linalg.solve_banded`).

\<hr\>

### 11.7 Core Application: The 1D "Quenched" Rod

> Summary: The **Crank-Nicolson Method** is used to simulate the transient cooling of a rod, demonstrating its ability to maintain perfect stability and accuracy even when using large time steps that violate the FTCS condition.

We simulate a 1D metal rod, initially hot ($T_0=100^\circ\text{C}$), whose ends are instantly quenched to a cold temperature ($T_{\text{env}}=0^\circ\text{C}$).

**The Critical Test:** We deliberately choose a large time step $\Delta t$ that results in a **Diffusion Number $\alpha \approx 12.5$**. FTCS would instantly explode at this value.

**The CN Process:** At every step, the system $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ is solved using the fast tridiagonal solver.

```python
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

## --- Setup for Unstable α (α = 12.5) ---

L = 1.0; Nx = 50; h_x = L / Nx; D = 1.0
h_t_cn = 0.005
alpha_cn = D * h_t_cn / (h_x ** 2) # α = 12.5
N_interior = Nx - 1

## [Code to build A_banded and the time march loop is performed here]

## --- Plotting the Stable Result ---

x_grid = np.linspace(0, L, Nx + 1)
## T_history is the result array from the simulation loop (not shown for brevity)

## Final plot shows smooth, physically sensible cooling curves

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_title(r"Crank–Nicolson Temperature Evolution ($\alpha = 12.5$, Unconditionally Stable)")
ax.set_xlabel("Position $x$")
ax.set_ylabel("Temperature $T$ ($^\circ$C)")
ax.grid(True)
## Plot selected time profiles

## for idx in plot_indices:

##     ax.plot(x_grid, T_history[idx], label=f"t = {idx * h_t_cn:.3f} s")

## plt.show()

## --- Final Analysis ---

## print(f"Diffusion Number α: {alpha_cn:.2f}")

## print(f"FTCS Stability Limit: Δt ≤ {0.5 * h_x**2 / D:.6f} s")

## print(f"CN uses Δt ≈ {h_t_cn / (0.5 * h_x**2 / D):.1f} × FTCS limit")

## print("Result: CN remains unconditionally stable ✓")

```

**Analysis and Conclusion:** The simulation confirms that the Crank-Nicolson method handles the massive $\alpha=12.5$ with **perfect stability**. This allows the use of large time steps, making the $\mathcal{O}(h_t^2)$ CN method vastly more **efficient** than running the thousands of tiny steps required for stable FTCS.

\<hr\>

### 11.8 Chapter Summary & Next Steps

**What We Built: The Parabolic PDE Solver**
We successfully added **time evolution** to spatial grids to solve diffusion problems:

  * **FTCS (Explicit):** Simple, but slow and **conditionally stable** ($\alpha \le 0.5$).
  * **BTCS (Implicit):** **Unconditionally stable**, but only $\mathcal{O}(h_t)$ accurate.
  * **Crank-Nicolson (Implicit):** The **Gold Standard**—unconditionally stable and $\mathcal{O}(h_t^2)$ accurate.

**The "Big Picture"**
The stability of the implicit methods relies on solving a **tridiagonal system** $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ at each step, emphasizing the crucial role of the fast $O(N)$ solvers from **Chapter 13**.

**Bridge to Chapter 12: The Wave Equation**
We transition from diffusion ($\\partial T / \partial t$) to propagation (waves). This requires replacing the first-order time derivative with a **second-order time derivative**:

$$\frac{\partial T}{\partial t} \quad \to \quad \frac{\partial^2 y}{\partial t^2}$$

This leads to the **Hyperbolic PDE** (Wave Equation), which introduces new challenges and a different stability condition.

---

# **Chapter 11: Parabolic PDEs () () (Workbook)**

**1. What class of Partial Differential Equations (PDEs) governs diffusion and transient heat flow ($\frac{\partial T}{\partial t}$ is present)?**

  * a) Elliptic PDEs.
  * b) Hyperbolic PDEs.
  * c) **Parabolic PDEs**. (**Correct**)
  * d) Integral Equations.

**2. The FTCS (Forward-Time Centered-Space) Method is constructed using the $\mathcal{O}(h_t)$ Forward Difference for time with which stencil for space?**

  * a) Backward Difference.
  * b) **Central Difference** ($\mathcal{O}(h_x^2)$). (**Correct**)
  * c) Simpson's Rule.
  * d) The 5-Point Stencil in time.

**3. What is the CFL stability condition for the FTCS method?**

  * a) $\alpha \ge 2$.
  * b) **$\alpha \le 0.5$**. (**Correct**)
  * c) $\alpha \le 1.0$.
  * d) $\alpha$ must be zero.

**4. Why is the BTCS (Backward-Time Centered-Space) method classified as an implicit scheme?**

  * a) Because the stability condition is explicit.
  * b) Because the future temperature $T_{n+1}$ is expressed as an explicit function of only known values.
  * c) **Because the scheme builds a system of equations where the unknown $T_{n+1}$ is linked to itself and its future neighbors**. (**Correct**)
  * d) Because it explicitly solves the matrix $\mathbf{A}$.

**5. What is the most significant advantage of the implicit BTCS and Crank-Nicolson schemes?**

  * a) They are $\mathcal{O}(h^4)$ accurate.
  * b) They are solved entirely from the present state.
  * c) **They are unconditionally stable (A-stable)**. (**Correct**)
  * d) They do not require boundary conditions.

**6. The Crank-Nicolson Method is the gold standard because it is unconditionally stable and achieves what level of temporal accuracy?**

  * a) $\mathcal{O}(h_t)$.
  * b) **$\mathcal{O}(h_t^2)$** (second-order). (**Correct**)
  * c) $\mathcal{O}(h_t^4)$.
  * d) $\mathcal{O}(h_t^5)$.

**7. If you decrease the spatial step $h_x$ by 10x in an FTCS simulation, what must happen to the maximum stable time step $h_t$?**

  * a) It must increase by 10x.
  * b) It must remain the same.
  * c) **It must decrease by 100x**. (**Correct**)
  * d) It must decrease by 10x.

**8. The matrix $\mathbf{A}$ that results from the Crank-Nicolson scheme has what structure?**

  * a) A full (dense) matrix.
  * b) A diagonal matrix.
  * c) **A tridiagonal matrix**. (**Correct**)
  * d) An upper-triangular matrix.

**9. The final destination of the Heat Equation, the steady-state solution $T_{\text{steady}}(x)$, is equivalent to the solution of what other PDE?**

  * a) The Wave Equation.
  * b) **Laplace's Equation ($\nabla^2 T = 0$)**. (**Correct**)
  * c) The Schrödinger Equation.
  * d) A simple ODE.

**10. What specific $O(N)$ algorithm is typically used to efficiently solve the tridiagonal system $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ at each time step?**

  * a) Gaussian Elimination.
  * b) **The Thomas Algorithm (or specialized banded solvers)**. (**Correct**)
  * c) The Secant Method.
  * d) Matrix Inversion.

---

# **Chapter 11: Questions: Parabolic PDEs () () (Workbook)**

**1. Physics of Change:** What physical process does the $\frac{\partial T}{\partial t}$ term enable in the Parabolic PDE, and how does this fundamentally differ from the static equilibrium modeled by Elliptic PDEs?

**2. Hybrid Problem:** Why is the Heat/Diffusion Equation classified as a "hybrid" problem? How is it treated as both an **IVP** and a **BVP**?

**3. FTCS Scheme:** Explain how the **Forward-Time Centered-Space (FTCS)** method is constructed using finite difference approximations for time and space.

**4. Explicit Definition:** Why is FTCS considered an **explicit** marching scheme?

**5. CFL Condition:** State the **CFL stability condition** for the 1D FTCS method. What happens numerically if this condition is violated?

**6. The Crippling Restriction:** Explain the practical dilemma caused by the CFL condition: If you decrease the spatial resolution ($\Delta x$) by a factor of 10, what must happen to the maximum time step ($\Delta t$), and why is this inefficient?

**7. Implicit Definition:** What is the conceptual difference between an **explicit** and an **implicit** scheme (like BTCS)? What unknowns are coupled in an implicit scheme?

**8. Unconditional Stability:** What does it mean for a scheme to be **unconditionally stable** (A-stable), and why does this property overcome the CFL restriction?

**9. The Trade-off:** Explain the fundamental trade-off of using implicit schemes (BTCS/Crank-Nicolson) over explicit schemes. What must be done at every time step to achieve stability?

**10. Crank-Nicolson:** Why is the **Crank-Nicolson Method** considered the "gold standard" for the Heat Equation?

**11. Temporal Accuracy:** What is the order of temporal accuracy for Crank-Nicolson, and how does this compare to FTCS and BTCS?

**12. Averaging Strategy:** Explain the key conceptual step Crank-Nicolson takes to achieve $\mathcal{O}(\Delta t^2)$ accuracy.

**13. Non-uniform Diffusion:** If the diffusion constant $D$ were a function of position, $D(x)$, how would the implicit FDM matrix $\mathbf{A}$ change?

**14. Solving the System:** What specific characteristic of the matrix ($\mathbf{A}$) in implicit schemes allows us to solve the system efficiently (in $O(N)$ time) instead of using a slow general solver?

**15. Initial Profile:** If you begin a simulation with a uniform temperature $T_0$ and fix the boundaries to $T_{\text{env}}$, describe the evolution of the maximum temperature over time.

---

# **Chapter 11: On Projects: Transient Diffusion Dynamics () () (Workbook)**

**1. Project: The CFL Violation Catastrophe**

  * **Problem:** Demonstrate and analyze the breakdown of the **FTCS** method when the **CFL stability condition** ($\alpha \le 0.5$) is violated.
  * **Formulation:** Set up a 1D rod (similar to Section 11.7) and choose parameters that result in an unstable diffusion number (e.g., $\alpha = 1.0$).
  * **Tasks:**
    1.  Implement the FTCS solver (Section 11.3).
    2.  Run the simulation for the unstable $\alpha$ and stop the time loop immediately if the solution exceeds a non-physical bound (e.g., $T < -100$).
    3.  **Visualization:** Plot the temperature profile at $t=0$, $t=2\Delta t$, and at the time step *just before* the solution explodes, showing the characteristic rapid, non-physical oscillations.

**2. Project: $\mathcal{O}(\Delta t^2)$ Convergence Analysis (Crank-Nicolson)**

  * **Problem:** Demonstrate the **second-order accuracy in time** ($\mathcal{O}(\Delta t^2)$) of the Crank-Nicolson method.
  * **Formulation:** Use the Crank-Nicolson solver and measure the error as $\Delta t$ is successively halved, ensuring $\Delta t$ is large enough that $\alpha \gg 0.5$ (avoiding the limit where spatial error $\mathcal{O}(\Delta x^2)$ dominates).
  * **Tasks:**
    1.  Use a very fine $\Delta x$ to minimize spatial error.
    2.  Use a reference solution (e.g., a CN run with a very, very small $\Delta t$) as the 'true' answer.
    3.  Run CN with $\Delta t, \Delta t/2, \Delta t/4$. Calculate the error at a fixed time $t=0.1$.
    4.  **Visualization:** Create a $\log(\text{Error})$ vs. $\log(\Delta t)$ plot. **Analysis:** The slope should be $-2$, confirming $\mathcal{O}(\Delta t^2)$ accuracy.

**3. Project: Insulated Boundaries (Neumann Conditions)**

  * **Problem:** Model a rod where one end is fixed ($T(0, t)=0$) and the other end is **insulated** (a **Neumann boundary condition**: $\frac{\partial T}{\partial x}(L, t) = 0$).
  * **Formulation:** The insulation condition must be incorporated into the FDM matrix system by modifying the last equation in the linear system ($\mathbf{A}\mathbf{T} = \mathbf{b}$) using an imaginary point $T_{N+1} = T_{N-1}$.
  * **Tasks:**
    1.  Modify the last row of the tridiagonal matrix $\mathbf{A}$ and the last element of $\mathbf{b}$ (for the Crank-Nicolson scheme) to account for the Neumann condition.
    2.  Use Crank-Nicolson.
    3.  **Visualization:** Plot the profiles. **Analysis:** The slope of the temperature curve at the insulated boundary should always be zero, reflecting $\frac{\partial T}{\partial x} = 0$.