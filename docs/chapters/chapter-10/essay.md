# **Introduction**

In **Part 3** (Chapters 7-9), our focus was on single-dimension physics, primarily solving problems that evolved over time ($t$). We now shift to a new class of multi-dimensional problems that govern **fields** in two or three spatial dimensions. This chapter addresses the physics of **static** or **steady-state** systems—those that have reached **equilibrium**, meaning their properties are no longer changing with respect to time ($\frac{\partial}{\partial t} = 0$).

These equilibrium problems are described by **Elliptic Partial Differential Equations (PDEs)**, which are pure **Boundary Value Problems (BVPs)**. The solution is a single, stable **shape** or field profile determined entirely by the fixed conditions on the boundaries of the domain.

The generalized form of these equations utilizes the **Laplacian operator** ($\nabla^2$):

$$
\nabla^2 \phi = \frac{\partial^2 \phi}{\partial x^2} + \frac{\partial^2 \phi}{\partial y^2} + \frac{\partial^2 \phi}{\partial z^2} = f(x, y, z)
$$

* **Laplace's Equation ($\nabla^2 \phi = 0$):** Governs the potential ($\phi$) in charge-free regions (electrostatics) or the temperature ($T$) in stable, source-free heat flow. The condition $\nabla^2 \phi = 0$ implies that at every interior point, the potential is at **equilibrium**, with no net flux or source.
* **Poisson's Equation ($\nabla^2 \phi = \rho$):** Governs fields in regions that contain a fixed source ($\rho$), such as charge density in electrostatics.

To solve these problems, we extend the **Finite Difference Method (FDM)** from Chapter 9 into two dimensions. This discretizes the Laplacian, transforming the calculus problem into a large **system of linear equations** that is solved iteratively via **relaxation**.

# **Chapter 10: Outline**

| Sec. | Title | Core Ideas & Examples |
| :--- | :--- | :--- |
| **10.1** | The Physics of "Steady State" | Elliptic PDEs, $\frac{\partial}{\partial t} = 0$, Laplace vs. Poisson. |
| **10.2** | The 2D Laplacian | Derivation of the "Five-Point Stencil" from FDM. |
| **10.3** | The Relaxation Analogy | Iterative methods, "rubber sheet" analogy. |
| **10.4** | Method 1: Jacobi | Synchronous updates, two-grid requirement, parallelizable. |
| **10.5** | Method 2: Gauss-Seidel | Sequential updates, one-grid, $\approx 2\times$ faster than Jacobi. |
| **10.6** | Method 3: SOR | Over-relaxation factor $\omega$, fastest convergence. |
| **10.7** | Application: Electrostatic Box | $\nabla^2 \phi = 0$ with fixed boundaries, equipotential lines. |
| **10.8** | Summary & Bridge | From Elliptic to Parabolic PDEs (Heat Equation). |

---

## **10.1 The 2D Laplacian: The "Five-Point Stencil"**

The core of the FDM for Elliptic PDEs is the derivation of an algebraic approximation for the **2D Laplacian operator** ($\nabla^2 \phi$).

---

### **Derivation of the Five-Point Stencil**

Assuming an evenly spaced grid with spacing $h$, the derivation involves substituting the $\mathcal{O}(h^2)$ **Central Difference stencil** (from Chapter 5) into each spatial dimension separately:

$$
\nabla^2 \phi \approx \left( \frac{\phi_{i+1, j} - 2\phi_{i, j} + \phi_{i-1, j}}{h^2} \right) + \left( \frac{\phi_{i, j+1} - 2\phi_{i, j} + \phi_{i, j-1}}{h^2} \right)
$$

For **Laplace's Equation** ($\nabla^2 \phi = 0$), we multiply by $h^2$ and rearrange to solve for the central point, $\phi_{i,j}$:

$$
\phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1} - 4\phi_{i, j} \approx 0
$$

This immediately yields the fundamental FDM rule, known as the **Five-Point Stencil**:

$$
\boxed{\phi_{i, j} \approx \frac{1}{4} \left( \phi_{i+1, j} + \phi_{i-1, j} + \phi_{i, j+1} + \phi_{i, j-1} \right)}
$$

---

### **Physical Interpretation**

The mathematical form of the Five-Point Stencil provides a powerful **physical insight**: the potential or temperature at any interior grid point in a static, equilibrium field is simply the **average of the potentials of its four immediate neighbors** (North, South, East, West). This condition *defines* equilibrium, as any deviation from this average implies a non-zero $\nabla^2 \phi$ and thus an unphysical flux.

!!! tip "The Definition of Equilibrium"
```
The Five-Point Stencil isn't just a mathematical trick; it's a profound physical statement. It says that for a field in equilibrium ($\nabla^2\phi = 0$), the value at *any* point must be the **exact average** of its neighbors. If it were higher or lower, there would be a "dip" or "peak," implying a source or sink, which violates the equilibrium condition.

```
The local truncation error for this FDM approximation remains **$\mathcal{O}(h^2)$**.

---

## **10.2 The "Relaxation" Analogy and Iterative Methods**

The technique used to solve the large algebraic system resulting from FDM is called the **Relaxation Method**, which models the physical system settling into its final equilibrium shape.

The process is analogous to a **taut rubber sheet** pinned at its edges (the fixed boundary conditions). An initial perturbation in the interior is gradually "damped out" or **relaxed** until the sheet assumes its final, stable shape.

```python
    flowchart TD
    A[Start: Initial Grid (Guesses + Boundaries)] --> B{Sweep Grid (e.g., Gauss-Seidel)}
    B --> C[Apply 5-Point Stencil to each interior node $\phi_{i,j}$]
    C --> D{Check Convergence}
    D -- No (Error > Tolerance) --> B
    D -- Yes (Error <= Tolerance) --> E[Stop: Final Equilibrium Solution]
```

```python
import numpy as np

def solve_laplace(grid_size, boundary_conditions, max_iter=1000, tol=1e-4):
    u = np.zeros((grid_size, grid_size))
    # Apply boundary conditions...

    for _ in range(max_iter):
        u_next = u.copy()
        # Finite difference update
        u_next[1:-1, 1:-1] = 0.25 * (u[0:-2, 1:-1] + u[2:, 1:-1] +
                                     u[1:-1, 0:-2] + u[1:-1, 2:])

        if np.max(np.abs(u_next - u)) < tol:
            break
        u = u_next

    return u
```

```python
# Algorithm: Jacobi Relaxation

import numpy as np

def jacobi_relaxation(phi_old, tolerance=1e-6):
    # Initialize: phi_new[M, N], phi_old[M, N] (with boundaries)
    M, N = phi_old.shape
    phi_new = np.copy(phi_old)
    max_error = 1.0

    while max_error > tolerance:
        max_error = 0.0

        # 1. Calculate all new values using only old values
        for i in range(1, M-1):
            for j in range(1, N-1):
                phi_new[i,j] = 0.25 * (phi_old[i+1,j] + phi_old[i-1,j] +
                                     phi_old[i,j+1] + phi_old[i,j-1])

        # 2. Check for convergence (compare new to old)
        for i in range(1, M-1):
            for j in range(1, N-1):
                error = abs(phi_new[i,j] - phi_old[i,j])
                if error > max_error:
                    max_error = error

        # 3. Copy new to old for next iteration
        phi_old = np.copy(phi_new)

    return phi_new
```
```python

---

## **10.4 Method 2: The Gauss-Seidel Method**

The **Gauss-Seidel Method** is the standard serial implementation, offering an immediate and simple improvement over the Jacobi Method by accelerating the propagation of information.

The method updates the grid **sequentially** and utilizes the newly calculated potential values *immediately*. When calculating $\phi_{i, j}$ in a standard left-to-right sweep, the potentials at the left ($\phi_{i-1, j}$) and lower ($\phi_{i, j-1}$) neighbors have already been refreshed in the current iteration.

* **Advantages:** It is typically **twice as fast** as the Jacobi method and requires only **one copy** of the solution array, reducing memory overhead.
* **Disadvantage:** It is inherently **sequential**, making straightforward parallelization difficult.

??? question "How does Gauss-Seidel accelerate convergence?"
    In Jacobi, information from a boundary moves one cell per iteration. In Gauss-Seidel (left-to-right sweep), information from the left ($i-1$) and bottom ($j-1$) boundaries is used *immediately* by the point $(i, j)$. This allows boundary information to propagate diagonally across the *entire grid* in a *single iteration*, leading to much faster convergence.

```
## Algorithm: Gauss-Seidel Relaxation

```python
import numpy as np

def gauss_seidel_relaxation(phi, tolerance=1e-6):
```
```
# Initialize: phi[M, N] (with boundaries)
M, N = phi.shape
max_error = 1.0

while max_error > tolerance:
    max_error = 0.0

    for i in range(1, M-1):
        for j in range(1, N-1):
            # Store old value just for error check
            phi_old = phi[i,j]

            # Calculate new value using *most recent* neighbors
            # Note: phi[i-1,j] and phi[i,j-1] are from the *current* sweep
            phi[i,j] = 0.25 * (phi[i+1,j] + phi[i-1,j] +
                             phi[i,j+1] + phi[i,j-1])

            # Check error for this point
            error = abs(phi[i,j] - phi_old)
            if error > max_error:
                max_error = error

return phi
```
```python
```

---

## **10.5 Method 3: Successive Over-Relaxation (SOR)**

The **Successive Over-Relaxation (SOR) Method** [1] is the fastest and most efficient iterative technique for dense grids, built as a direct acceleration of the Gauss-Seidel method.

SOR introduces **extrapolation** by using a tunable **over-relaxation factor ($\omega$)** to intentionally **push the point past** its equilibrium value.

The update incorporates $\omega$ into the Gauss-Seidel ($\phi_{\text{GS}}$) correction:

$$
\phi[i, j] = \phi_{\text{old}}[i, j] + \omega \cdot (\phi_{\text{GS}}[i, j] - \phi_{\text{old}}[i, j])
$$

* **Tuning:** The factor must satisfy **$1 < \omega < 2$**. When tuned correctly (optimal $\omega \approx 1.8$ to $1.9$ for many problems), SOR can reduce the total number of iterations required for convergence by an **order of magnitude** compared to Gauss-Seidel, making it the most efficient method for dense grids [1, 3].

---

## **10.6 Core Application: The Electrostatic Box**

The simulation of the **electrostatic potential $\phi(x, y)$** inside a charge-free box is the classic application of FDM relaxation, governed by Laplace's Equation ($\nabla^2 \phi = 0$).

By fixing the potential on the four boundaries (e.g., three at $0$ V and one at a source voltage $V_0$) and iteratively applying the Five-Point Stencil via the Gauss-Seidel Method, the interior potential gradually **relaxes** to its final, stable distribution.

The final visualization (heatmap) yields critical physical insights:
* **Heatmap:** Shows the total, static potential field.
* **Contour Lines:** Trace the **equipotential lines** (paths of constant $\phi$). Physically, the **electric field ($\mathbf{E}$) is always perpendicular** to these lines.

!!! example "Visualizing the Physics"
```
A heatmap of the final potential distribution clearly shows the physics. The potential "flows" from the high-voltage $V_0$ boundary to the $0$ V boundaries. The contour lines, which show paths of equal voltage, are always perpendicular to the electric field $\mathbf{E}$. A test charge placed in this field would feel a force $\mathbf{F} = q\mathbf{E}$, pushing it "downhill" along the steepest gradient.

```
---

## **10.7 Chapter Summary & Bridge to Chapter 11**

The FDM for Elliptic PDEs successfully converts the continuous problem into a massive, sparse **system of linear equations** ($\mathbf{A}\mathbf{x} = \mathbf{b}$). The three relaxation methods (Jacobi, Gauss-Seidel, SOR) are, mathematically, iterative solvers for this system.

This chapter's methods are the final preparation for modeling **dynamic fields**. **Chapter 11** will re-introduce the **time derivative** ($\frac{\partial T}{\partial t}$) to solve the **Parabolic PDE** (Heat/Diffusion Equation):

$$
\frac{\partial T}{\partial t} = D \nabla^2 T
$$

This requires coupling the **spatial discretization** (FDM stencils from this chapter) with **time stepping** (marching techniques from Chapter 7), forcing the simulation to confront **CFL stability constraints**.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

[2] Higham, N.J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[3] Quarteroni, A., Sacco, R., & Saleri, F. (2007). *Numerical Mathematics*. Springer.

[4] Newman, M. (2013). *Computational Physics*. CreateSpace Independent Publishing Platform.

[5] Garcia, A. L. (2000). *Numerical Methods for Physics* (2nd ed.). Prentice Hall.