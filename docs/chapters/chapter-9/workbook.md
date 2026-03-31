# **Chapter 9: Boundary Value Problems (Workbook)**

### 9.1 Chapter Opener: The "In-Between" Problem

> Summary: Dynamics are solved by Initial Value Problems (IVPs), but **Boundary Value Problems (BVPs)**—where conditions are known at two different spatial points—require new methods because the crucial **initial slope ($y'(0)$) is unknown**.

In **Part 3** (Chapters 7 and 8), we solved **Initial Value Problems (IVPs)**, which involve predicting a system's evolution forward from a single starting point where all conditions (like $x(t_0)$ and $v(t_0)$) are known.

However, a critical class of problems is defined by conditions at the **physical limits** of a system—the **boundaries**. These are **Boundary Value Problems (BVPs)**.

**Physical Examples of BVPs**:
* **Structural Engineering:** Finding the **static shape** ($y(x)$) of a bridge fixed at both ends ($y(0)=0, y(L)=0$).
* **Heat Flow:** Determining the **steady-state temperature profile** ($T(x)$) of a rod held at two different temperatures.
* **Quantum Mechanics:** Finding the stationary **wavefunction $\psi(x)$** of a bound particle ($\psi(0)=0, \psi(L)=0$).

**The "Problem" for Solvers**

A second-order ODE like $y''(x) = f(x)$ requires **two** conditions at the starting point, $x=0$, to be solved by an IVP solver (like RK4). In a BVP, we only know the initial position ($y(0)$) and the condition at the *other* end ($y(L)$). We are missing the critical **initial slope ($y'(0)$)**.

**The "Solution" Strategies**:
1.  **The Shooting Method:** Converts the BVP into an IVP by iteratively guessing the missing initial slope ($y'(0)$).
2.  **The Finite Difference Method (FDM):** Solves the entire domain simultaneously by converting the ODE into a large system of linear algebra equations.

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. What is the core difference between an **Initial Value Problem (IVP)** and a **Boundary Value Problem (BVP)**?**

* a) IVPs are solved with matrices; BVPs are solved with root finding.
* b) IVPs are linear; BVPs are always nonlinear.
* c) IVPs specify all conditions at a **single point** (e.g., $x(t_0), v(t_0)$); BVPs specify conditions at **two different points** (boundaries). (**Correct**)
* d) IVPs solve for shape; BVPs solve for time evolution.

**2. The core challenge in solving a BVP like $y(0)=A, y(L)=B$ with an IVP solver is that you are missing which required initial condition?**

* a) The initial position $y(0)$
* b) The final position $y(L)$
* c) The final slope $y'(L)$
* d) The **initial slope $y'(0)$** (**Correct**)

#### Interview-Style Question

**Question:** Give two examples of BVPs, and for each, explain why the problem cannot be solved by simply integrating forward in time as we did in the RK4 chapter.

**Answer Strategy:**
1.  **The Bridge Problem:** We know $y(0)$ and $y(L)$. We cannot integrate forward because the resulting trajectory is determined by the **initial slope $y'(0)$**, which is unknown. Only one trajectory will hit the target height $y(L)$.
2.  **The Stationary Wavefunction Problem:** We know $\psi(0)=0$ and $\psi(L)=0$. The problem is *not* one of time evolution, but of finding the **static spatial shape** $\psi(x)$ that satisfies the ends. RK4 (a time-stepper) is fundamentally the wrong tool for finding a stationary spatial solution.

### Hands-On Project

**Project Idea: The Flexible Bridge (Simple Structural Deflection)**

* **Problem:** Model a uniform cable deflection BVP: $y''(x) = C$, with boundary conditions $y(0)=0$ and $y(L)=0$.
* **Formulation:** Convert the second-order BVP to a first-order IVP (e.g., $\dot{\mathbf{S}} = [z, C]$).
* **Goal:** Use a placeholder root solver to solve the BVP for the correct initial slope $g=y'(0)$.

## 🎯 9.2 Method 1: The Shooting Method

> Summary: The Shooting Method converts a BVP into a **root-finding problem** by defining an **Error Function $E(g)$** equal to the miss distance at the boundary, which is solved by iteratively adjusting the initial slope guess ($g=y'(0)$).

The **Shooting Method** is a clever, but often unstable, technique that solves the BVP by making it look like a solvable **IVP**.

**The Error Function $E(g)$**:
The BVP is solved when the initial slope $g = y'(0)$ yields a final position $y_{\text{final}}$ that exactly matches the target $B$.

$$E(g) = y_{\text{final}}(L, g) - B$$

* **Tool Coupling:** The solution is a hybrid algorithm:
    1.  The **Internal Engine** runs the IVP for each guess (using RK4/`solve_ivp` from **Chapter 7**).
    2.  The **External Intelligence** finds the root $g$ of $E(g)$ (using the **Secant Method** from **Chapter 3**).

**Secant Update Rule for the Slope $g$**:

$$g_{n+1} = g_n - E(g_n) \left[ \frac{g_n - g_{n-1}}{E(g_n) - E(g_{n-1})} \right]$$

**Limitations**:
* **Instability:** Errors in the initial slope $g$ are **exponentially amplified** over the trajectory, causing $y_{\text{final}}$ to quickly fly off to $\pm\infty$.
* **Inefficiency:** It requires running a full IVP simulation for *every single step* of the root-finding algorithm.

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. The "Aha! Moment" of the Shooting Method is that the entire BVP is converted into what kind of problem?**

* a) A Matrix Eigenvalue Problem.
* b) A **Root-Finding Problem**. (**Correct**)
* c) A Spline Interpolation Problem.
* d) A Monte Carlo Simulation.

**2. What is the primary disadvantage of the Shooting Method, especially for chaotic or exponentially growing ODEs?**

* a) It requires an $O(h^4)$ RK4 solver.
* b) It runs an entire simulation only once.
* c) It is **very unstable**, as small errors in the initial slope are exponentially amplified. (**Correct**)
* d) It requires the analytical derivative $E'(g)$.

#### Interview-Style Question

**Question:** The Shooting Method is a hybrid algorithm. Which two core algorithms from earlier chapters are essential components of the method, and what does the Secant Method's root represent?

**Answer Strategy:** The two core components are the **IVP Solver** (RK4/`solve_ivp` from Chapter 7) and the **Root Finder** (Secant Method from Chapter 3). The root of the error function $E(g)$ represents the **optimal initial slope $y'(0)$** that ensures the trajectory hits the far boundary condition $y(L)$.

### Hands-On Project

**Project: The Flexible Bridge (Secant Implementation)**

1.  **Formulation:** Solve the bridge BVP: $y''(x) = C$, with $y(0)=0$ and $y(L)=0$.
2.  **Tasks:**
    * Implement the `error_function(g)` which calls `solve_ivp`.
    * Use `scipy.optimize.root_scalar` with `method='secant'` and two initial guesses for $g$ to find the optimal slope.
3.  **Goal:** Plot the final trajectory $y(x)$, which should be a symmetric parabola that starts and ends at zero.

## 🧊 9.3 Method 2: The Finite Difference (Relaxation) Method

> Summary: The Finite Difference Method (FDM) converts the BVP into a stable **System of Linear Equations** ($\mathbf{A}\mathbf{y} = \mathbf{b}$) by substituting the $O(h^2)$ Central Difference stencil for $y''$ at every grid point.

The **Finite Difference Method (FDM)**, often called the **Relaxation Method**, is the preferred approach because it avoids the exponential instability of the Shooting Method.

**The "Concept": Discretization**

The BVP is solved by **discretizing** the entire domain ($x \in [0, L]$) into $N+1$ points. At every interior point $x_i$, the second derivative $y''(x_i)$ is replaced by the $O(h^2)$ **Central Difference stencil**:

$$y''(x_i) \approx \frac{y_{i+1} - 2y_i + y_{i-1}}{h^2}$$

**The $\mathbf{A}\mathbf{y} = \mathbf{b}$ System**:
Applying this stencil to the linear BVP $y'' = -x^2$ (for example) at every interior point $i$ results in a large **System of Linear Equations**:

$$\mathbf{A} \mathbf{y} = \mathbf{b}$$

* **Unknowns ($\mathbf{y}$):** The vector of solution values $[y_1, y_2, \dots, y_{N-1}]^T$.
* **Matrix ($\mathbf{A}$):** A **tridiagonal matrix** (non-zero entries only on the main diagonal and the two adjacent off-diagonals). The constant structure is a hallmark of the 1D FDM.
* **RHS ($\mathbf{b}$):** The vector of constants (including the known boundary values $y_0$ and $y_N$).

**Solution and Advantages**
The final solution $\mathbf{y}$ is found by solving the system using fast, specialized **Linear Algebra** techniques (e.g., LU Decomposition, solved efficiently via `solve_banded` or `np.linalg.solve` from **Chapter 13**).

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. The "Aha! Moment" of the Finite Difference Method (FDM) is that it solves the BVP by converting the calculus problem into what?**

* a) A single nonlinear equation.
* b) A chaotic system of ODEs.
* c) A time-stepping integration problem.
* d) A **System of Linear Equations** ($\mathbf{A}\mathbf{y} = \mathbf{b}$). (**Correct**)

**2. Why is the tridiagonal structure of the matrix $\mathbf{A}$ highly advantageous for computation?**

* a) It guarantees the existence of an analytic solution.
* b) It can be solved directly in $O(N^3)$ time.
* c) It **can be solved rapidly** (in $O(N)$ time) using specialized linear algebra algorithms. (**Correct**)
* d) It prevents the solution from spiraling outward.

#### Interview-Style Question

**Question:** Explain the distinction between the FDM approach (a "global" method) and the Shooting Method (a "local" method) in terms of how they generate the final solution.

**Answer Strategy:**
* **FDM (Global):** The FDM sets up a system of equations that links **every single point** on the grid simultaneously. The solver then computes the final solution $y(x)$ for the *entire domain at once*.
* **Shooting (Local):** The Shooting Method is local and sequential. It only solves the solution one point at a time, repeatedly trying a local trajectory ($y(0), y'(0)$) to see if it reaches the correct far boundary $y(L)$.

### Hands-On Project

**Project: FDM on a Simple Linear BVP (Validation)**

1.  **Problem:** Solve the linear BVP: $y'' = -6x$, with $y(0)=0$ and $y(1)=1$.
2.  **Tasks:**
    * Construct the tridiagonal matrix $\mathbf{A}$ (the constant $[1, -2, 1]$ structure).
    * Build the RHS vector $\mathbf{b}$ using the known boundary conditions.
    * Use `scipy.linalg.solve_banded` to find the interior solution $\mathbf{y}$.
3.  **Goal:** Plot the FDM solution and the analytic solution $y(x) = -x^3 + 3x$ on the same graph to demonstrate convergence.

## ⚛️ 9.4 Core Application: 1D Time-Independent Schrödinger Equation

> Summary: Applying FDM to the Schrödinger Equation ($\frac{-\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$) transforms it into the **Matrix Eigenvalue Problem** ($\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$), where the **eigenvalues ($E$) are the energy levels** and the **eigenvectors ($\boldsymbol{\psi}$) are the wavefunctions**.

The **Time-Independent Schrödinger Equation** ($\hat{H}\psi = E\psi$) is a classic BVP. FDM provides the ideal numerical solution by mapping it directly onto a linear algebra problem.

**The Hamiltonian Matrix ($\mathbf{H}$)**:
Substituting the $y''$ stencil and rearranging yields the algebraic form:
$$\left( \frac{-\hbar^2}{2mh^2} \right)\psi_{i-1} + \left( \frac{\hbar^2}{mh^2} + V_i \right)\psi_i + \left( \frac{-\hbar^2}{2mh^2} \right)\psi_{i+1} = E\psi_i$$

This is the eigenvalue problem $\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$.

* **Main Diagonal ($H_{i,i}$):** Represents the sum of **Kinetic Energy** and **Potential Energy** ($V_i$) at node $i$.
* **Off-Diagonals ($H_{i, i\pm 1}$):** Represents the **Kinetic Energy coupling** between neighboring nodes.

**The Solution:** The FDM transforms the differential equation into a matrix equation, which is solved by finding the eigenvalues and eigenvectors (using specialized solvers like `scipy.linalg.eigh_tridiagonal` from **Chapter 14**).

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. When FDM is applied to the Schrödinger equation, the problem naturally maps to which category of linear algebra problem?**

* a) A System of Linear Equations ($\mathbf{A}\mathbf{x} = \mathbf{b}$).
* b) A **Matrix Eigenvalue Problem** ($\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$). (**Correct**)
* c) A Matrix Inversion Problem.
* d) A LU Decomposition Problem.

**2. In the resulting matrix equation $\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$, the **unknown energy $E$** corresponds to which component of the matrix solution?**

* a) The eigenvector.
* b) The Hamiltonian matrix.
* c) The potential $V(x)$.
* d) The **eigenvalue**. (**Correct**)

#### Interview-Style Question

**Question:** In the resulting equation $\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$, which physical quantity corresponds to the **eigenvalue $E$**, and which corresponds to the **eigenvector $\boldsymbol{\psi}$**?

**Answer Strategy:** This is a direct mapping:
* The **Eigenvalue $E$** represents the set of allowed, discrete **Energy Levels** (the physically observable quantities).
* The **Eigenvector $\boldsymbol{\psi}$** represents the spatial profile of the corresponding **Wavefunction** (the probability distribution).

### Hands-On Project

**Project: The 1D Quantum Harmonic Oscillator**

1.  **Problem:** Find the energy levels for the quantum harmonic oscillator, where the potential is $V(x) = \frac{1}{2}kx^2$.
2.  **Tasks:**
    * Construct the Hamiltonian $\mathbf{H}$ with the variable potential $V_i$ on the main diagonal.
    * Solve the eigenvalue problem using `scipy.linalg.eigh_tridiagonal`.
3.  **Goal:** Plot the first three wavefunctions and verify that the energy eigenvalues are close to the expected half-integer values $E_n \approx (n + 1/2)$.

## 🧭 9.5 Chapter Summary & Next Steps

**What We Built: A Boundary Value Problem (BVP) Toolkit**:
| Method | Core Concept | Stability & Use Case |
| :--- | :--- | :--- |
| **1. Shooting Method** | Converts BVP to a **Root-Finding Problem** | Prone to **exponential instability**. |
| **2. Finite Difference Method (FDM)** | Converts BVP to a **Matrix Equation** ($\mathbf{A}\mathbf{y} = \mathbf{b}$) | **Robust** and **stable**. The preferred professional method. |

**The "Big Picture": Discretization**
The key takeaway is the power of **discretization**, which maps complex differential equations onto efficient **Linear Algebra** problems.

* $y'' = -x^2 \to \mathbf{A}\mathbf{y} = \mathbf{b}$.
* $\hat{H}\psi = E\psi \to \mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$.

**Bridge to Part 4: Partial Differential Equations (PDEs)**
The $d^2/dx^2$ FDM stencil is the essential foundation for solving PDEs. **Chapter 10** will extend FDM to the **2D Laplacian** ($\nabla^2$) to find the static shape of fields by solving **Laplace's Equation**.

---

Would you like to move on to **Chapter 10: Elliptic PDEs (e.g., Laplace's Equation)**?