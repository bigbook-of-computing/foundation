# **Introduction**

In the previous chapters, we mastered **Initial Value Problems (IVPs)**, which involve predicting a system's evolution forward in time from a single starting point where all conditions (e.g., $x(t_0)$, $v(t_0)$) are known. We now turn to a fundamentally different, yet equally critical, class of problems: **Boundary Value Problems (BVPs)**.

BVPs are defined not by a complete set of initial conditions, but by constraints at the **physical limits**, or boundaries, of a system. Common examples include finding the static shape of a beam fixed at both ends ($y(0)=0$, $y(L)=0$), the steady-state temperature profile of a rod ($T(0)=T_A$, $T(L)=T_B$), or the stationary wavefunction of a quantum particle ($\psi(0)=0$, $\psi(L)=0$).

The core challenge is that while a second-order ODE requires two conditions at the start ($y(0)$ and $y'(0)$) for an IVP solver, a BVP provides one at the start ($y(0)$) and one at the end ($y(L)$). This chapter explores the two primary computational strategies for overcoming this: the **Shooting Method** and the **Finite Difference Method**.

# **Chapter 9: Outline**

| Sec. | Title | Core Ideas & Examples |
| :--- | :--- | :--- |
| **9.1** | The "In-Between" Problem | IVPs vs. BVPs, missing initial slope $y'(0)$. |
| **9.2** | The Shooting Method | Converting BVP to a root-finding problem, $E(g)=0$. |
| **9.3** | The Finite Difference Method | Discretization, central difference stencil, linear algebra. |
| **9.4** | The $\mathbf{A}\mathbf{y} = \mathbf{b}$ System | Tridiagonal matrices, $\mathcal{O}(N)$ solvers. |
| **9.5** | The Matrix Eigenvalue Problem | Solving the TISE, $\mathbf{H}\mathbf{\psi} = E\mathbf{\psi}$. |
| **9.6** | Summary and Bridge | From BVPs to PDEs (Partial Differential Equations). |

---

## **9.1 The "In-Between" Problem**

In Part 3 (Chapters 7 and 8), we mastered **Initial Value Problems (IVPs)**. These problems are analogous to launching a projectile: given a perfect set of initial conditions ($x(t_0)$, $v(t_0)$, etc.), we can predict its entire future trajectory.

A **Boundary Value Problem (BVP)** is fundamentally different. We are not given the "launch" conditions. Instead, we are given the start and end points of a trajectory and must find the path "in-between."

**Physical Examples of BVPs**:

  * **Static Structures**: Determining the **static shape** ($y(x)$) of a bridge cable or beam fixed at both ends ($y(0)=0, y(L)=0$).
  * **Equilibrium Fields**: Finding the **steady-state temperature profile** ($T(x)$) of a rod where both ends are held at fixed temperatures.
  * **Quantum Mechanics**: Finding the stationary **wavefunction $\psi(x)$** and its corresponding **energy $E$** for a bound particle, constrained by $\psi(0)=0$ and $\psi(L)=0$.

The primary challenge in solving a second-order ODE like $y''(x) = f(x)$ that governs these systems is that a standard IVP solver requires **two** initial conditions at $x=0$. In a BVP, we know the initial position $y(0)$ but are missing the critical **initial slope $y'(0)$**; the second condition is given only at the far boundary $y(L)$.

To overcome this, we rely on two radically different computational strategies: the **Shooting Method** and the **Finite Difference Method (FDM)**.

---

## **9.2 Method 1: The Shooting Method**

The **Shooting Method** [1, 2] converts the BVP into an iterative **root-finding problem** by treating the missing initial slope as a variable to be guessed.

---

### **The Conversion to Root-Finding**

The process is analogous to firing a cannon toward a target:

1.  **Formulation**: The second-order BVP is converted into a coupled first-order IVP (e.g., using a state vector $\mathbf{S} = [y, y']^T$).

2.  **The Guess ($g$):** An initial slope guess, $g = y'(0)$, is used to launch the trajectory.

3.  **The Trajectory**: An **IVP solver** (like RK4 from Chapter 7) is run from $x=0$ to the far boundary $x=L$, yielding a final position $y_{\text{final}}$.

4.  **The Error Function ($E(g)$):** The **Error Function $E(g)$** measures the "miss distance" between the trajectory's final position and the target boundary condition $B$:

```
$$
E(g) = y_{\text{final}}(L, g) - B
$$

The problem is solved when the specific slope $g$ is found that makes the miss distance zero, $E(g) = 0$.



```
```python
# Algorithm: The Shooting Method

## Define: f(S, x)        # The coupled 1st-order ODEs, S = [y, y']

## Define: y_initial      # Boundary condition y(0)

## Define: y_target       # Boundary condition y(L)

## Define: x_min = 0, x_max = L

def get_error(guess_slope, f, y_initial, y_target, x_min, x_max, solve_ivp):
    # 1. Set initial state vector
    S_initial = [y_initial, guess_slope]

    # 2. Run the IVP solver
    S_final = solve_ivp(f, S_initial, x_min, x_max)

    # 3. Calculate the "miss distance"
    y_final = S_final[0]  # Get the y-component at x=L
    error = y_final - y_target
    return error

## 4. Use a root-finder (e.g., Secant) on the error function

## find_root will call get_error() repeatedly with new guesses

## correct_slope = find_root(get_error, initial_guess_1, initial_guess_2)

```
```python
    flowchart LR
    A[BVP: $y'' = f(x)$] --> B(Discretize Domain)
    B --> C{Replace $y''$ with FDM Stencil}
    C --> D[Generate (N-1) Linear Equations]
    D --> E[Assemble Matrix System $\mathbf{A}\mathbf{y} = \mathbf{b}$]
    E --> F[Solve with Linear Algebra]
    F --> G[Solution $y_i$ at all grid points]
```

---

## **9.4 Core Application: 1D Time-Independent Schrödinger Equation**

The most powerful application of the FDM is its use in solving the **Time-Independent Schrödinger Equation** (TISE): $\hat{H}\psi = E\psi$.

---

### **The Matrix Eigenvalue Problem**

The TISE is a BVP where both the **wavefunction $\psi(x)$** and the **energy $E$** are unknown. Substituting the FDM stencil for the second derivative $\frac{d^2\psi}{dx^2}$ and rearranging yields the algebraic system:

$$
\left( \frac{-\hbar^2}{2mh^2} \right)\psi_{i-1} + \left( \frac{\hbar^2}{mh^2} + V_i \right)\psi_i + \left( \frac{-\hbar^2}{2mh^2} \right)\psi_{i+1} = E\psi_i
$$

This is the canonical **Matrix Eigenvalue Problem** [3, 4]:

$$
\mathbf{H} \mathbf{\psi} = E \mathbf{\psi}
$$

* **Matrix $\mathbf{H}$**: The **Hamiltonian Matrix**. Its main diagonal elements, $H_{i,i} = \frac{\hbar^2}{mh^2} + V_i$, represent the sum of **Kinetic Energy** and **Potential Energy** ($V_i$) at node $i$. The off-diagonal elements, $H_{i, i\pm 1}$, represent the **Kinetic Energy coupling** between neighboring nodes.

  * **Eigenvalues $E$**: The solution's **eigenvalues $E$** give the set of allowed, discrete **Energy Levels**.
  * **Eigenvectors $\mathbf{\psi}$**: The corresponding **eigenvectors $\mathbf{\psi}$** give the spatial profile of the **wavefunctions**.

The FDM thus converts the quantum mechanical differential equation into a matrix equation that is efficiently solved using specialized eigensolvers (Chapter 14).

!!! example "The Particle in a Box"
    The classic "particle in a box" problem is a perfect BVP. The potential $V(x)$ is $0$ inside the box (from $x=0$ to $x=L$) and $\infty$ outside. The boundary conditions are $\psi(0)=0$ and $\psi(L)=0$.
    
    
    Using the FDM, we set $V_i = 0$ for all *interior* grid points. The resulting Hamiltonian matrix $\mathbf{H}$ is a simple tridiagonal matrix. Solving $\mathbf{H}\mathbf{\psi} = E\mathbf{\psi}$ numerically yields the correct quantized energy levels $E_n \propto n^2$ and the sinusoidal wavefunctions $\psi_n(x)$.
    
---

## **9.5 Chapter Summary and Bridge to Part 4: PDEs**

We have successfully built a toolkit for **Boundary Value Problems**:

  * **Shooting Method**: Simple but unstable and inefficient.
  * **FDM**: The **robust, stable, and preferred professional method**.

The key realization is the power of **discretization**, which maps complex differential equations (like the TISE) onto efficient **Linear Algebra** problems ($\mathbf{A}\mathbf{y}=\mathbf{b}$ or $\mathbf{H}\mathbf{\psi}=E\mathbf{\psi}$).

The three-point FDM stencil for $d^2/dx^2$ is the crucial foundation for solving multi-dimensional field problems. **Chapter 10** will extend this technique to discretize the 2D Laplacian, $\nabla^2 = \frac{\partial^2}{\partial x^2} + \frac{\partial^2}{\partial y^2}$, and solve **Laplace's Equation**—the start of **Part 4: Partial Differential Equations (PDEs)**.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

[2] Garcia, A. L. (2000). *Numerical Methods for Physics* (2nd ed.). Prentice Hall.

[3] Newman, M. (2013). *Computational Physics*. CreateSpace Independent Publishing Platform.

[4] Thijssen, J. M. (2007). *Computational Physics* (2nd ed.). Cambridge University Press.