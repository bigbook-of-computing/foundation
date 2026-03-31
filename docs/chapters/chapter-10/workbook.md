# **Chapter 10: Elliptic PDEs (Workbook)**

---

> **Summary:** This workbook explores the physics of **Static Fields** and steady-state equilibrium. We re-introduce the Laplacian operator ($\nabla^2$) in 2D and discretize it using the **Five-Point Stencil**. You will learn the family of **Relaxation Methods**—Jacobi, Gauss-Seidel, and SOR—which simulate a system "relaxing" into its final, stable equilibrium shape.

---

## **10.1 The Physics of "Steady State"** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Elliptic PDEs and Equilibrium
> 
> **Summary:** Systems in equilibrium (like static heat distributions or electric potentials) are governed by Elliptic PDEs where time is no longer a variable. We define Laplace’s and Poisson’s equations as the governing laws of these fields.

**The "Problem": Elliptic PDEs**
These problems are described by **Elliptic Partial Differential Equations (PDEs)**, defined by the **Laplacian operator** ($\nabla^2$):
$$\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} + \frac{\partial^2 \phi}{\partial z^2} = f(x, y, z)$$

The "Elliptic" nature means the solution is a single, static **shape** determined entirely by the fixed conditions on the surrounding boundary (a pure BVP).

**The "Solution": Relaxation**
We extend the **Finite Difference Method (FDM)** from Chapter 9 into two dimensions. This converts the calculus problem into a large **system of linear equations** (algebra), which we solve using an iterative technique called **relaxation**.

### **Comprehension Check**

!!! note "Quiz"
    1. What class of Partial Differential Equations (PDEs) governs static, steady-state field problems like electrostatics and equilibrium heat flow?
    2. Laplace's Equation, $\nabla^2 \phi = 0$, implies what physical condition at every point in a charge-free region?

??? info "See Answer"
    1. **Elliptic PDEs**.
    2. **The field is at equilibrium, with no net flux (or source) at that point**.

!!! abstract "Interview-Style Question"
    **Question:** Give two distinct physical examples of static fields governed by Elliptic PDEs, and explain why the main difference between Elliptic and Parabolic PDEs is the presence of the time derivative.
    
    ???+ info "Answer Strategy"
        1.  **Examples:** Electrostatic Potential ($\nabla^2 \phi = 0$) and Steady-State Heat Flow ($\nabla^2 T = 0$).
        2.  **Difference:** Elliptic PDEs model systems that have reached **equilibrium**; thus, the $\frac{\partial}{\partial t}$ term is zero. Parabolic PDEs (Chapter 11) model **dynamic diffusion** ($\frac{\partial T}{\partial t} = D \nabla^2 T$), which is inherently time-dependent.

### Hands-On Project

**Project Idea: Modeling Steady-State Heat Flow (Thermal Contours)**

* **Task:** Set up a rectangular plate with four fixed, uneven boundary temperatures (e.g., Left $= 100^\circ\text{C}$, Right $= 50^\circ\text{C}$).
* **Goal:** Visualize the resulting temperature field $T(x, y)$ using a **heatmap** and overlay the **isothermal contour lines** (lines of equal temperature), demonstrating the final equilibrium shape.

## **10.2 The 2D Laplacian: The "Five-Point Stencil"** {.heading-with-pill}

> Summary: The 2D Laplacian is discretized by summing the Central Difference stencils for $\frac{\partial^2}{\partial x^2}$ and $\frac{\partial^2}{\partial y^2}$. This yields the **Five-Point Stencil** rule: $\phi_{i, j} \approx \frac{1}{4} (\text{Average of 4 Neighbors})$.

**The Goal:** Find an algebraic approximation for the 2D Laplacian operator, $\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2}$.

**The Derivation (The FDM Stencil)**:
1.  Substitute the $O(h^2)$ **Central Difference stencil** (Chapter 5) into each dimension.
```
$$\frac{\partial^2 \phi}{\partial x^2} \approx \frac{\phi_{i+1, j} - 2\phi_{i, j} + \phi_{i-1, j}}{h^2}$$
```
2.  Sum the two contributions and set the result to zero (for Laplace's Equation, $\nabla^2 \phi = 0$).
3.  Rearranging and solving for the central point $\phi_{i, j}$ yields the final rule:

$$\boxed{\phi_{i, j} \approx \frac{1}{4} \left( \phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1} \right)}$$

**The "Aha! Moment"**
This **Five-Point Stencil** is the entire algorithm. It means the potential at any interior point in an equilibrium field is simply the **average of the potentials of its four immediate neighbors**.

**Accuracy:** Because it uses the $O(h^2)$ Central Difference stencil, the approximation maintains **second-order accuracy** ($O(h^2)$).

### **Comprehension Check**

!!! note "Quiz"
    1. The final FDM algebraic rule for Laplace's Equation (the Five-Point Stencil) dictates that the potential $\phi_{i,j}$ is equal to:
    2. What is the order of the **Truncation Error** for the FDM stencil used to solve Laplace's Equation?

??? info "See Answer"
    1. **The average of the potentials of its four nearest neighbors.**
    2. **$O(h^2)$**.

!!! abstract "Interview-Style Question"
    **Question:** Explain the physical meaning of the Five-Point Stencil rule ($\phi_{i, j} \approx \frac{1}{4} (\text{Average of 4 Neighbors})$). Why does this simple algebraic statement define "equilibrium" in a static field?
    
    ???+ info "Answer Strategy"
        This rule defines **perfect equilibrium**. If the potential at the center $\phi_{i,j}$ were *not* the average of its surroundings, there would be a non-zero **second derivative** (curvature). In physical terms, this non-zero curvature indicates a source/sink or a net flux (heat flow or electrical current). Since Laplace's Equation ($\nabla^2 \phi = 0$) defines a charge-free, static state, the potential must perfectly average out the influences of its neighbors.

### Hands-On Project

**Project: FDM on a Simple Linear BVP (Validation)**

* **Task:** Write a function `phi_update(i, j, phi)` that applies the Five-Point Stencil rule to a central point $(i, j)$ using the surrounding grid values.
* **Goal:** This function is the single, non-iterative core of all the relaxation methods (Jacobi, Gauss-Seidel, SOR) that will be implemented in the following sections.

## **10.3 The "Relaxation" Analogy** {.heading-with-pill}

> Summary: The iterative solution process is called **relaxation** because it simulates a physical system (like a taut rubber sheet) settling from an initial guess into its final, stable equilibrium shape, defined by the Five-Point Stencil.

The iterative technique of solving Elliptic PDEs is called the **Relaxation Method** because it computationally models the physical system settling into equilibrium.

**The "Analogy": The Taut Rubber Sheet**
The process can be visualized as a **taut rubber sheet** (or trampoline) where the edges are **pinned** (fixed boundary conditions). The interior is given an initial guess (a perturbation) and then iteratively "relaxes" into its final, stable shape, which is the solution to Laplace's equation.

**The Iterative Process**:
1.  **Guess:** Start with an initial grid $\phi_{\text{old}}$.
2.  **Sweep:** Repeatedly loop across every interior grid point $(i, j)$ and update its value using the Five-Point Stencil.
3.  **Convergence:** The iterations stop when the maximum change in potential between successive full sweeps falls below a set **tolerance**, signifying **numerical equilibrium**.

## **10.4 Method 1: The Jacobi Method** {.heading-with-pill}

> Summary: The **Jacobi Method** is the conceptually simplest relaxation method, requiring **two copies** of the grid to update all points **synchronously**, using only $\phi_{\text{old}}$ values. It is highly parallelizable but suffers from **slow convergence**.

The Jacobi Method calculates all new values based **only** on the values that existed **before the current iteration began** ($\phi_{\text{old}}$).

**The Algorithm:**
* **Memory:** Requires **two full copies** of the grid ($\phi_{\text{old}}$ and $\phi_{\text{new}}$).
* **Update:** $\phi_{\text{new}}[i, j]$ is calculated using the average of the four neighbors from $\phi_{\text{old}}[i\pm 1, j\pm 1]$.
* **Limitation:** **Slow Convergence**. Information from the boundary propagates inward by only **one grid unit per iteration**.

## **10.5 Method 2: The Gauss-Seidel Method** {.heading-with-pill}

> Summary: The **Gauss-Seidel Method** utilizes only **one array** and updates points **sequentially**, using newly calculated values immediately. This accelerates information propagation and is typically **twice as fast** as Jacobi.

The **Gauss-Seidel Method** is an efficient improvement that utilizes the newest calculated potential values *immediately* within the current sweep.

**The Algorithm:**
* **Memory:** Requires only **one array** ($\phi$).
* **Update:** Updates are performed **sequentially**. When calculating $\phi_{i, j}$, the method uses $\phi_{\text{new}}$ values for the already-updated neighbors (e.g., $\phi_{i-1, j}$ and $\phi_{i, j-1}$) and $\phi_{\text{old}}$ values for the yet-to-be-updated neighbors ($\phi_{i+1, j}$ and $\phi_{i, j+1}$).
* **Advantage:** **Faster Convergence**. Information propagation is accelerated because the boundary influence travels inward faster. It is approximately **twice as fast** as the Jacobi method.

## **10.6 Method 3: Successive Over-Relaxation (SOR)** {.heading-with-pill}

> Summary: **SOR** is the fastest iterative method, building on Gauss-Seidel by using an **over-relaxation factor** ($\omega$, where $1 < \omega < 2$) to intentionally **overshoot** the equilibrium value, dramatically accelerating convergence.

The **Successive Over-Relaxation (SOR) Method** is a direct acceleration of Gauss-Seidel using **extrapolation**.

**The Algorithm:**
The SOR update applies the Gauss-Seidel correction multiplied by the over-relaxation factor $\omega$:
$$\phi[i, j] = \phi_{\text{old}}[i, j] + \mathbf{\omega} \cdot (\phi_{\text{GS}}[i, j] - \phi_{\text{old}}[i, j])$$

* **Over-Relaxation Factor ($\omega$):** The factor must satisfy **$1 < \omega < 2$**.
* **Tuning:** When $\omega$ is tuned correctly (often $\approx 1.8$ to $1.9$), SOR can reduce the total number of iterations by an **order of magnitude** compared to Gauss-Seidel.

### **Comprehension Check**

!!! note "Quiz"
    1. What is the primary characteristic of the **Jacobi Method**?
    2. The **Gauss-Seidel Method** improves upon the Jacobi Method by making what adjustment?
    3. What is the purpose of the **over-relaxation factor $\omega$** in the **SOR Method**?

??? info "See Answer"
    1. **All new values are calculated based *only* on the potentials from the previous iteration ($\phi_{\text{old}}$)**.
    2. **Using newly calculated potential values immediately within the current sweep** (sequential update).
    3. **To push the updated potential past its equilibrium value to accelerate dampening.**

!!! abstract "Interview-Style Question"
    **Question:** Explain why the **Gauss-Seidel Method** is typically more efficient for a single-processor (serial) implementation compared to the **Jacobi Method**.
    
    ???+ info "Answer Strategy"
        The efficiency gain comes from **faster information propagation**. Gauss-Seidel updates the grid **in place** (one array) and uses the newest calculated values immediately within the current sweep, accelerating the transmission of boundary influence to the interior. Jacobi, requiring two arrays, forces a full wait until the end of the iteration, resulting in slower convergence.

### Hands-On Project

**Project: Convergence Rate Showdown (Jacobi vs. Gauss-Seidel)**

1.  **Formulation:** Set up a grid with fixed boundary conditions (Section 10.7).
2.  **Tasks:** Implement both the Jacobi and Gauss-Seidel Methods.
3.  **Goal:** Create a **semilog plot** showing $\log_{10}(\text{Max Change})$ versus the $\text{Iteration Number}$ for both methods, visually proving that Gauss-Seidel requires fewer iterations to reach the same tolerance.

## **10.7 Core Application: The Electrostatic Box** {.heading-with-pill}

> Summary: The electrostatic box governed by Laplace's Equation is solved via the Gauss-Seidel Method, iteratively applying the Five-Point Stencil until the potential field stabilizes, yielding equipotential contour lines perpendicular to the field.

The **Electrostatic Box** is the classic application of FDM relaxation.

**The Physics:** We solve **Laplace's Equation** ($\nabla^2 \phi = 0$) for a square region where three walls are $0$ V and one source wall is $V_0$.

**The Strategy (Gauss-Seidel):** We iteratively sweep across the grid, updating all interior points based on the **Five-Point Stencil average rule** until the maximum change between iterations falls below a tolerance.

**Physical Interpretation**:
* **Heatmap:** Shows the final static potential distribution $\phi(x, y)$.
* **Contour Lines:** Trace the **equipotential lines** (paths of constant $\phi$). The hidden **electric field ($\mathbf{E}$) is always perpendicular** to these lines.

## **10.8 Chapter Summary & Next Steps** {.heading-with-pill}

**What We Built: A 2D Static Solver**
* **Operator:** Discretized the 2D Laplacian into the **Five-Point Stencil** ($O(h^2)$ accurate).
* **Methods:** Implemented iterative **relaxation** using Jacobi, Gauss-Seidel, and SOR.

**The "Big Picture": Sparse Matrix Solvers**
The relaxation methods are **iterative solvers** for the underlying sparse matrix system $\mathbf{A}\mathbf{x} = \mathbf{b}$ that results from FDM.

**Bridge to Chapter 11: The Time Dimension**
We now re-introduce the time derivative ($\frac{\partial T}{\partial t}$) to solve the **Parabolic PDE** (Heat/Diffusion Equation):
$$\frac{\partial T}{\partial t} = D \nabla^2 T$$
This requires coupling FDM stencils with time-marching, forcing us to immediately confront **CFL stability constraints**.

---

Would you like to move on to **Chapter 11: Parabolic PDEs (e.g., The Heat/Diffusion Equation)**?