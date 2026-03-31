# **Introduction**

In Chapter 10, we solved **Elliptic Partial Differential Equations (PDEs)**, such as Laplace's Equation ($\nabla^2 \phi = 0$), to find the *final, static, steady-state* shape of a field (e.g., the equilibrium temperature profile). However, the reality of physics is the **transient dynamic process** of *reaching* that equilibrium. We must now answer the fundamental question: "How does the system evolve over time?".

This dynamic, spreading-out process is governed by **diffusion**. Whether it is heat propagating through a material, ink spreading in water, or risk diffusing in a financial market (governed by the Black-Scholes equation), the physics is described by the **Heat Equation** (or **Diffusion Equation**), which is the classic **Parabolic PDE**:

$$
\boxed{\frac{\partial T}{\partial t} = D \nabla^2 T}
$$

The equation is a **hybrid problem** that demands a combination of our previous techniques:

1.  It is an **Initial Value Problem (IVP)** in time, requiring a starting distribution $T(x, 0)$.
2.  It is a **Boundary Value Problem (BVP)** in space, requiring conditions like fixed endpoints $T(0, t) = A$.

To solve it, we must discretize **both** time ($\Delta t$) and space ($\Delta x$) and march the entire spatial grid forward one time step at a time.

# **Chapter 11: Outline**

| Sec. | Title | Core Ideas & Examples |
| :--- | :--- | :--- |
| **11.1** | Discretization: Time & Space | Forward-Time (FT) and Centered-Space (CS) stencils. |
| **11.2** | The Explicit FTCS Scheme | Explicit update rule, diffusion number $\alpha$. |
| **11.3** | Conditional Stability (CFL) | The $\alpha \le 0.5$ restriction, numerical explosion. |
| **11.4** | The Implicit BTCS Scheme | Unconditional stability, tridiagonal matrix system. |
| **11.5** | Crank-Nicolson Method | $\mathcal{O}(h_t^2)$ accuracy, unconditional stability, "Gold Standard". |
| **11.6** | Application: 1D "Quenched" Rod | Testing FTCS failure vs. Crank-Nicolson stability. |
| **11.7** | Summary & Bridge | From Parabolic (diffusion) to Hyperbolic (waves) PDEs. |

---

## **11.1 Discretization: The Time and Space Trade-off**

The Parabolic PDE involves derivatives in two independent variables: time ($t$) and space ($x$). The solution, $T(x, t)$, is calculated over a discrete grid indexed by time ($n$) and space ($i$), denoted $T_{i, n}$.

To convert the continuous PDE into a solvable algebraic system, we apply the Finite Difference Method (FDM) to each term:

| Derivative | Scheme | Formula | Accuracy |
| :--- | :--- | :--- | :--- |
| **Time ($\frac{\partial T}{\partial t}$)** | **Forward Difference** (like Euler's Method, Ch 7) | $\frac{T_{i, n+1} - T_{i, n}}{h_t}$ | $\mathcal{O}(h_t)$ (First-Order) |
| **Space ($\frac{\partial^2 T}{\partial x^2}$)** | **Central Difference** (like Laplacian, Ch 5/10) | $\frac{T_{i+1, n} - 2T_{i, n} + T_{i-1, n}}{h_x^2}$ | $\mathcal{O}(h_x^2)$ (Second-Order) |

Substituting these into the Heat Equation yields the core algebraic expression:

$$
\frac{T_{i, n+1} - T_{i, n}}{h_t} = D \cdot \frac{T_{i+1, n} - 2T_{i, n} + T_{i-1, n}}{h_x^2}
$$

??? question "Why use a low-accuracy time stencil?"
    We are using a highly accurate $\mathcal{O}(h_x^2)$ stencil for space but only a low-accuracy $\mathcal{O}(h_t)$ stencil for time. Why is this mismatch acceptable?
    
    **Hint:** Think about the FTCS stability constraint ($h_t \propto h_x^2$). The time step $h_t$ is *forced* to be so much smaller than $h_x$ that the error from the time-stepping (which scales with $h_t$) becomes negligible compared to the spatial error (which scales with $h_x^2$).
    
---

## **11.2 Method 1: The Explicit FTCS Scheme**

The **Forward-Time Centered-Space (FTCS) Method** is the most straightforward way to implement this combined discretization.

The scheme is **explicit**, meaning the future temperature $T_{i, n+1}$ is calculated directly from known values at the present time $n$.

The equation is rearranged by defining the dimensionless **Diffusion Number ($\alpha$)**:

$$
\alpha = D \frac{h_t}{h_x^2}
$$

The resulting FTCS update rule is:

$$
\boxed{T_{i, n+1} = T_{i, n} + \alpha \left( T_{i+1, n} - 2T_{i, n} + T_{i-1, n} \right)}
$$

This formula states that the change in temperature at a point is proportional to the **spatial curvature** at the present time.

```python
# Algorithm: Explicit FTCS for 1D Heat Equation

import numpy as np

def ftcs_heat_equation(T_present, D, h_x, h_t, N_steps):
    # Initialize: T_present[N], T_future[N] (with BCs)
    N = len(T_present)
    T_future = np.copy(T_present)
    alpha = D * h_t / (h_x * h_x)

    # Check stability *before* starting
    if alpha > 0.5:
        raise ValueError("Stability condition alpha <= 0.5 not met!")

    for n in range(N_steps):
        # Calculate all interior points for next timestep
        for i in range(1, N-1):
            T_future[i] = T_present[i] + alpha * (T_present[i+1] -
                                                2*T_present[i] +
                                                T_present[i-1])

        # Copy future to present for next iteration
        T_present = np.copy(T_future)

    return T_present
```

---

```python
```

---

## **11.3 The "Horror Story": Conditional Stability**

The simplicity of the FTCS method is deceptive, as it is plagued by **conditional stability**. If the time step $h_t$ is too large relative to the spatial step $h_x$, the inevitable round-off error (Chapter 2) introduced at each step is **amplified**, leading to non-physical, growing oscillations and a numerical **explosion**.

---

### **The CFL Condition**

**Von Neumann Stability Analysis** proves the stringent requirement for the FTCS scheme to remain stable [1, 2]:

$$
\boxed{\alpha = D \frac{h_t}{h_x^2} \le \frac{1}{2}}
$$

This is a specific case of the general **Courant–Friedrichs–Lewy (CFL) condition**, which imposes a numerical **"speed limit"** on the simulation.

---

### **The Crippling Restriction**

The CFL condition creates a practical dilemma for high-resolution modeling:

$$
h_t \le \frac{1}{2D} h_x^2
$$

Because $h_t$ is proportional to $h_x^2$, increasing the spatial resolution by a factor of $\mathbf{10}$ (i.e., decreasing $h_x$ by 10x) forces the time step $\mathbf{h_t}$ to decrease by a factor of $\mathbf{100}$. This renders the explicit FTCS method **impractically slow** for simulations requiring fine spatial grids.

!!! example "The Cost of Resolution"
    Imagine a 2D heat simulation ($h_t \propto h_x^2 + h_y^2$). You need to increase the spatial resolution by $10\times$ in both $x$ and $y$ to capture a fine detail.
    
    * **Workload:** The grid size increases by $100\times$.
    * **Stability:** The time step $h_t$ must shrink by $100\times$.
    * **Total Cost:** The simulation now takes $100 \times 100 = \mathbf{10,000}$ times longer to run. This is the "tyranny of $h^2$."
    
---

## **11.4 Method 2: The Implicit BTCS Scheme**

The solution to the CFL restriction is to switch from an **explicit** marching scheme to an **implicit** scheme.

The **Backward-Time Centered-Space (BTCS) Method** is the specific implicit scheme that solves this. It calculates the spatial coupling term ($\nabla^2 T$) using the temperature distribution at the **unknown future time step** ($n+1$).

---

### **The Matrix System**

This implicit linkage means that the future temperature $T_{i, n+1}$ is coupled to its future neighbors ($T_{i \pm 1, n+1}$). The rearrangement of the discretized equation results in a **system of linear equations**:

$$
(-\alpha) T_{i-1, n+1} + (1 + 2\alpha) T_{i, n+1} + (-\alpha) T_{i+1, n+1} = T_{i, n}
$$

This system is written in matrix form as $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$, where:

* $\mathbf{T}_{n+1}$ is the **unknown vector** of future temperatures.
* $\mathbf{b}$ is the **known vector** of present temperatures $T_{n}$ (plus boundary contributions).
* $\mathbf{A}$ is the coefficient matrix, which is **tridiagonal**.

---

### **Advantages and Trade-offs**

The most significant feature of BTCS is that it is **unconditionally stable** (A-stable) [2, 3]. The solution will never explode, regardless of the value of $\alpha$. The stability is achieved at the computational cost of having to solve the tridiagonal system $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ at every time step. Furthermore, BTCS is only **$\mathcal{O}(h_t)$ accurate** in time (like Euler's method).

---

## **11.5 Method 3: The "Gold Standard" Crank-Nicolson**

The **Crank-Nicolson Method** is the most widely used scheme for parabolic PDEs, as it is **unconditionally stable** and achieves **second-order accuracy in time** ($\mathcal{O}(h_t^2)$) [1, 4].

---

### **The Concept: Averaging the Derivatives**

Crank-Nicolson achieves its higher accuracy by approximating the spatial derivative ($\nabla^2 T$) using the **average of the Central Difference stencils** evaluated at the present time ($n$) and the future time ($n+1$):

$$
\frac{\partial T}{\partial t}\;\approx\;\frac{D}{2}\left[\left.\frac{\partial^2 T}{\partial x^2}\right|_{t=t_n}
+\left.\frac{\partial^2 T}{\partial x^2}\right|_{t=t_{n+1}}\right]
$$

---

### **The Algorithm and the Matrix System**

The complex substitution and rearrangement still result in a **tridiagonal system** of linear equations, $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$.

* **Matrix $\mathbf{A}$ (LHS):** Main Diagonal is $(1 + \alpha)$; Off-Diagonals are $(-\frac{\alpha}{2})$.
* **Vector $\mathbf{b}$ (RHS):** Must be **recalculated at every step** using the known $T_n$ profile.

!!! tip "Implicit Methods: Pay for Stability"
    Implicit methods (BTCS, Crank-Nicolson) are **computationally more expensive *per step*** because they require solving a matrix equation. However, they are **vastly more efficient *overall*** because their unconditional stability allows you to take enormous time steps ($h_t$) that would be impossible for an explicit method. You trade
    many cheap, unstable steps for a few expensive, stable steps.
    
---

### **The Gold Standard**

The Crank-Nicolson method is the gold standard because its combination of $\mathbf{\mathcal{O}(h_t^2)}$ accuracy and **unconditional stability** allows the user to choose the largest possible time step that satisfies the desired temporal *accuracy*, making it vastly more **efficient** than either FTCS or BTCS for a given error requirement. The system $\mathbf{A} \mathbf{T}_{n+1} = \mathbf{b}$ is solved efficiently using specialized $O(N)$ tridiagonal solvers (like the Thomas Algorithm, Chapter 13).

---

## **11.6 Core Application: The 1D "Quenched" Rod**

The transient cooling of a rod, initially hot and instantly quenched at its boundaries (Dirichlet BCs), serves as the ultimate test case for these schemes.

The simulation confirms the core principles of implicit integration:

1.  **FTCS Failure:** The explicit FTCS method immediately fails when tested with a large time step that sets $\alpha > 0.5$ (e.g., $\alpha=0.75$ or $\alpha=12.5$), resulting in catastrophic numerical oscillations.
2.  **CN Success:** The **Crank-Nicolson Method** successfully simulates the smooth, predictable cooling of the rod, even when using large time steps (e.g., $\Delta t = 0.005$ s, resulting in $\alpha=12.5$) that violate the FTCS condition by a factor of $\mathbf{25}$.

This application validates the FDM approach: the stability gained from solving the implicit tridiagonal system is essential for developing efficient and robust dynamic models.

---

## **11.7 Chapter Summary and Bridge to Chapter 12**

This chapter established the full **Parabolic PDE Solver** toolkit, moving from the static fields of Chapter 10 to dynamic, time-evolving systems. The key numerical challenge was the **CFL stability constraint** of explicit schemes, which was solved by adopting the **unconditionally stable** implicit methods (BTCS and the $\mathbf{\mathcal{O}(h_t^2)}$ Crank-Nicolson method).

We now transition from systems that **diffuse** or **smooth out** their energy ($\frac{\partial T}{\partial t}$) to systems that **propagate** and **retain** their energy (waves). This requires replacing the first-order time derivative with a **second-order time derivative**, leading to the **Hyperbolic PDE**, or **Wave Equation**:

$$
\frac{\partial^2 y}{\partial t^2} = v^2 \nabla^2 y
$$

This seemingly minor change introduces a new formulation and a different stability constraint that must be resolved in **Chapter 12**.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

[2] Higham, N.J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[3] Quarteroni, A., Sacco, R., & Saleri, F. (2007). *Numerical Mathematics*. Springer.

[4] Newman, M. (2013). *Computational Physics*. CreateSpace Independent Publishing Platform.

[5] Garcia, A. L. (2000). *Numerical Methods for Physics* (2nd ed.). Prentice Hall.