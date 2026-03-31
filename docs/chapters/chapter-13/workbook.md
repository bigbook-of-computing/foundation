# **Chapter 13: Systems of Linear Equations (Workbook)**

---

> **Summary:** This workbook introduces the "Engine Room" of numerical physics: solving $\mathbf{A}\mathbf{x} = \mathbf{b}$. We transition from $O(N^3)$ direct solvers (LU Decomposition) to $O(N)$ iterative solvers for sparse matrices. You will learn why matrix inversion is a cardinal sin of numerical computing and how to choose the right solver for resistors, trusses, and PDEs.

---

## **13.1 The "Engine" We've Been Waiting For** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Matrix Equations ($\mathbf{A}\mathbf{x} = \mathbf{b}$)
> 
> **Summary:** Most complex physical simulations—from steady-state heat to circuit analysis—eventually condense into a system of linear equations. This section defines the universal structure of these problems and previews the direct and iterative strategies for solving them.

$$\mathbf{A}\mathbf{x} = \mathbf{b}$$

We discovered that most "advanced" physical problems transform into this linear system, a critical "magic trick" of numerical methods:

* **Boundary Value Problems (BVPs):** The Finite Difference Method (FDM, Chapter 9) transforms the differential equation ($y'' = f$) into a system $\mathbf{A}\mathbf{y} = \mathbf{b}$.
* **Implicit PDEs:** The Crank-Nicolson method (Chapter 11) requires solving a tridiagonal system $\mathbf{A}\mathbf{T}_{n+1} = \mathbf{b}$ at every time step.
* **Resistor Networks (Core Application):** Kirchhoff's laws applied to a circuit yield a set of coupled voltage equations $\mathbf{A}\mathbf{V} = \mathbf{I}$.

**The "Problem":** We have been hand-waving *how* to solve this. If $\mathbf{A}$ is a $10,000 \times 10,000$ matrix, how do we *actually* find the solution vector $\mathbf{x}$?

**The "Solution":** This chapter is the "engine room." We will build the robust algorithms to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ efficiently. We will categorize solvers into two groups: **Direct Methods** (which find the solution in a fixed number of steps) and **Iterative Methods** (which "relax" to the solution over time).

---

## **13.2 Method 1: Gaussian Elimination** {.heading-with-pill}

> Summary: Gaussian Elimination is the classical direct method for solving $\mathbf{A}\mathbf{x} = \mathbf{b}$. It transforms the full matrix $\mathbf{A}$ into an **upper-triangular matrix $\mathbf{U}$** using forward elimination, followed by trivial **back substitution** to find the solution vector $\mathbf{x}$.

**The Concept:** Gaussian Elimination is the mathematical formalization of the method learned in high school to solve systems of equations by "eliminating" variables.

**The Algorithm:**
1.  **Forward Elimination:** The matrix $\mathbf{A}$ is transformed into an **upper-triangular matrix** $\mathbf{U}$ by applying a sequence of row operations to the augmented matrix $[\mathbf{A} \mid \mathbf{b}]$. The goal is to create zeros in all positions *below* the main diagonal.
2.  **The Result ($\mathbf{U}\mathbf{x} = \mathbf{b}'$):** The system is now simple:
```
$$\begin{pmatrix} U_{11} & U_{12} & U_{13} \\ 0 & U_{22} & U_{23} \\ 0 & 0 & U_{33} \end{pmatrix} \begin{pmatrix} x_1 \\ x_2 \\ x_3 \end{pmatrix} = \begin{pmatrix} b'_1 \\ b'_2 \\ b'_3 \end{pmatrix}$$
```
3.  **Back Substitution:** The solution is found by solving for $x_N$ first, and working backward up the rows to find $x_{N-1}, x_{N-2}, \dots, x_1$.

**Cost and Limitations:**
* **Cost:** Gaussian Elimination is an **$\mathcal{O}(N^3)$** algorithm. While conceptually simple, its cost quickly becomes prohibitive for matrices larger than a few thousand rows ($N>1000$).
* **Instability:** It requires **pivoting** (swapping rows) to avoid division by zero or division by very small numbers, which can amplify **round-off error** (Chapter 2).

---

## **13.3 Method 2: LU Decomposition** {.heading-with-pill}

> Summary: **LU Decomposition** is the direct method used by professional libraries. It factors the matrix $\mathbf{A}$ into lower ($\mathbf{L}$) and upper ($\mathbf{U}$) triangular matrices once ($\mathcal{O}(N^3)$), allowing the system to be solved for any subsequent right-hand side vector $\mathbf{b}$ very quickly ($\mathcal{O}(N^2)$).

**The Problem:** Gaussian Elimination is too slow if you need to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ many times with a constant $\mathbf{A}$ matrix but a changing $\mathbf{b}$ vector (e.g., in Crank-Nicolson, Chapter 11).

**The Concept:** The elimination steps only depend on $\mathbf{A}$. LU Decomposition factors $\mathbf{A}$ once:

$$\mathbf{A} = \mathbf{L} \mathbf{U}$$

* $\mathbf{L}$ is a **Lower-triangular matrix** (stores the elimination steps).
* $\mathbf{U}$ is an **Upper-triangular matrix** (the result of forward elimination).

**The Two-Step Solution:** The problem $\mathbf{A}\mathbf{x} = \mathbf{b}$ becomes $\mathbf{L}(\mathbf{U}\mathbf{x}) = \mathbf{b}$. This is solved by introducing an intermediate vector $\mathbf{y} = \mathbf{U}\mathbf{x}$:
1.  **Solve $\mathbf{L}\mathbf{y} = \mathbf{b}$:** Solved for $\mathbf{y}$ using fast **forward substitution**.
2.  **Solve $\mathbf{U}\mathbf{x} = \mathbf{y}$:** Solved for $\mathbf{x}$ using fast **back substitution**.

**Cost and Efficiency:**
* **Cost to Factor $\mathbf{A} \to \mathbf{L}\mathbf{U}$:** $\mathcal{O}(N^3)$ (done only once).
* **Cost to Solve $\mathbf{A}\mathbf{x} = \mathbf{b}$:** $\mathcal{O}(N^2)$ (forward/back substitution).

This makes it vastly superior to Gaussian elimination when multiple solutions are required. **Professional functions like `np.linalg.solve()` and `scipy.linalg.solve()` use optimized LU decomposition.**

---

## **13.4 The "Do Not Do This" Method: Matrix Inversion** {.heading-with-pill}

> Summary: **Matrix Inversion** ($\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$) is computationally inefficient ($\mathcal{O}(N^3)$ with a large pre-factor) and numerically unstable. **Never** compute the inverse to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$.

The mathematical identity $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$ is tempting, but using it in computation is considered **poor numerical practice**.

**Why Matrix Inversion Fails Numerically:**
1.  **It's Slow:** Computing the inverse $\mathbf{A}^{-1}$ is slower than the LU factorization required by the direct solver.
2.  **It's Unstable:** The process of matrix inversion involves complex intermediate steps that maximize the effects of **round-off error** (Chapter 2). The resulting $\mathbf{A}^{-1}$ matrix is often less accurate than the LU factors.
3.  **It's Unnecessary:** You do not need the entire $N \times N$ inverse matrix; you only need the single $N \times 1$ solution vector $\mathbf{x}$.

**Mantra:** Always use a direct solver that performs the efficient LU decomposition (`np.linalg.solve(A, b)`), which bypasses the unstable step of explicit matrix inversion.

---

## **13.5 Iterative Solvers (Gauss-Seidel, CG)** {.heading-with-pill}

> Summary: **Iterative Solvers** are essential for huge, sparse systems ($\mathbf{A}$ is mostly zeros), avoiding the $\mathcal{O}(N^3)$ cost and memory limitations of direct methods by "relaxing" to the solution using only the non-zero elements.

**The Problem:** Direct solvers (LU Decomposition) are $\mathcal{O}(N^3)$. If a 3D PDE simulation generates a $1,000,000 \times 1,000,000$ matrix ($\mathbf{A}$), the computational time and the memory needed to *store* $\mathbf{A}$ are impossibly large.

**The "Aha! Moment": Sparsity**
The matrices resulting from FDM (Chapters 9-12) are **sparse**—they are mostly zeros (e.g., the 5-point stencil gives a matrix with $\sim 5N$ non-zero entries, not $N^2$).

**The Solution:** Use **Iterative Solvers** (also called **Relaxation Methods**).
1.  **Guess:** Start with an initial guess $\mathbf{x}_0$.
2.  **Iterate:** Refine the guess $\mathbf{x}_{k+1}$ by using the previous guess $\mathbf{x}_k$ and applying the $\mathbf{A}\mathbf{x} = \mathbf{b}$ equation in a loop until the solution converges.

**Examples of Iterative Solvers:**
* **Jacobi & Gauss-Seidel:** (Revisited from Chapter 10) These are simple, general iterative solvers that "relax" to the solution. Their cost is only $\mathcal{O}(N)$ per iteration for sparse matrices.
* **Conjugate Gradient (CG) Method:** The standard professional iterative solver for **symmetric** matrices. It mathematically guarantees convergence in at most $N$ steps and is highly efficient for the enormous sparse matrices of modern physics.

---

## **13.6 Core Application: A Resistor Network** {.heading-with-pill}

> Summary: Applying **Kirchhoff's Current Law** and **Ohm's Law** to a resistor network yields a system $\mathbf{A}\mathbf{V} = \mathbf{I}$, where $\mathbf{V}$ is the unknown voltage vector and $\mathbf{A}$ is the matrix of conductances ($\mathbf{G}$). This is a classic $\mathbf{A}\mathbf{x} = \mathbf{b}$ problem solved via a direct method.

**The Physics:** We seek to find the unknown voltages ($V_i$) at the nodes of an electrical circuit.

**The Laws:**
1.  **Kirchhoff's Current Law (KCL):** The sum of currents entering any node must be zero ($\sum I_{\text{in}} = 0$).
2.  **Ohm's Law (Conductance Form):** Current $I_{ij}$ flowing from node $i$ to node $j$ is $I_{ij} = G_{ij}(V_i - V_j)$, where $G_{ij} = 1/R_{ij}$ is the conductance.

**The Setup ($\mathbf{A}\mathbf{V} = \mathbf{I}$):**
Applying KCL to a node $i$ involves summing the current flowing from $i$ to all its neighbors $j$:

$$\sum_{j} G_{ij}(V_i - V_j) = 0$$

This equation is rearranged to group the unknown voltages ($V_i, V_j, \dots$) on the LHS and the known source currents/boundary conditions (like ground, $V=0$) on the RHS. This results in the matrix equation $\mathbf{A}\mathbf{V} = \mathbf{I}$, where $\mathbf{A}$ is the **conductance matrix**.

**The Computational Strategy:**
Since the system is typically linear and small/medium-sized ($N$ nodes), the fastest and most stable method is the **direct solution** using LU decomposition.

---

## **13.7 Chapter Summary & Next Steps** {.heading-with-pill}

**What We Built: The Linear Algebra Engine**
We have mastered the solutions for the core computational problem: $\mathbf{A}\mathbf{x} = \mathbf{b}$.

* **Direct Solvers (LU Decomposition):** The fastest, most stable method for dense or constant matrices. Solves $\mathbf{A}\mathbf{x} = \mathbf{b}$ in $\mathcal{O}(N^3)$ (factor) and $\mathcal{O}(N^2)$ (solve) time.
* **Iterative Solvers (Gauss-Seidel, CG):** Essential for massive, **sparse** FDM matrices, exploiting $\mathcal{O}(N)$ cost per iteration.
* **The Mantra:** **Never, *ever* compute $\mathbf{A}^{-1}$ to solve a linear system**. Always use a solver.

**Bridge to Chapter 14: The Eigenvalue Problem**

We have mastered the **driven problem** ($\mathbf{A}\mathbf{x} = \mathbf{b}$), where a known source $\mathbf{b}$ drives the solution $\mathbf{x}$.

The next step is to address the **natural problem**: What if there is no driving source? This leads to the **Eigenvalue Problem**:

$$\mathbf{A}\mathbf{x} = \lambda \mathbf{x}$$

This is the *exact* mathematical form of the **Schrödinger Equation** (Chapter 9) and the **Normal Modes of Oscillation**. We must now build the dedicated algorithms to find these "natural states"—the eigenvalues $\lambda$ and the eigenvectors $\mathbf{x}$—which is the focus of **Chapter 14**.

---

---

## **13.9 Comprehensive Review** {.heading-with-pill}

### **Section Quiz**

!!! note "Quiz"
    1. What is the fundamental algebraic structure that most complex FDM/Implicit PDE problems simplify to?
    2. Which direct solution method is the foundation for all professional linear algebra solvers and is broken down into two matrices $\mathbf{L}$ and $\mathbf{U}$?
    3. Why is it considered poor numerical practice to solve a system by computing the matrix inverse, $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$?
    4. For a large, sparse matrix resulting from an FDM problem, what is the primary advantage of using an **iterative solver** (like Gauss-Seidel or Conjugate Gradient) over a **direct solver** (like LU Decomposition)?
    5. What is the computational complexity of the **forward/back substitution** steps required to solve $\mathbf{L}\mathbf{U}\mathbf{x} = \mathbf{b}$?

??? info "See Answer"
    1. **A system of linear equations $\mathbf{A}\mathbf{x} = \mathbf{b}$**.
    2. **LU Decomposition**.
    3. **Because matrix inversion is slow, unnecessary, and numerically unstable (prone to round-off error)**.
    4. **Iterative solvers exploit sparsity, avoiding the $O(N^3)$ storage and time cost of dense matrices**.
    5. **$O(N^2)$**.

!!! abstract "Interview-Style Question"
    **Question:** You need to solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ one thousand times, where the matrix $\mathbf{A}$ is constant, but the vector $\mathbf{b}$ changes in every step. Explain the steps and the corresponding computational cost of the most efficient approach using a direct solver.
    
    ???+ info "Answer Strategy"
        The most efficient approach is **LU Decomposition**.
        1.  **Factorization (Pre-processing):** Factor the constant matrix $\mathbf{A}$ into $\mathbf{L}\mathbf{U}$ once. The cost of this step is $\mathcal{O}(N^3)$.
        2.  **Solving:** For each of the 1000 steps, solve the two triangular systems ($\mathbf{L}\mathbf{y} = \mathbf{b}$ and $\mathbf{U}\mathbf{x} = \mathbf{y}$) using forward and back substitution. The cost for *each* solve is only $\mathcal{O}(N^2)$.
        This approach avoids re-doing the $O(N^3)$ elimination 1000 times.

## **13.8 Hands-On Projects** {.heading-with-pill}

**1. Project: Simulating a Resistor Network (Core Application)**

* **Problem:** Find the unknown voltages ($V_1$ and $V_2$) in a simple three-node resistor network where two nodes are unknown and one is a fixed battery voltage.
* **Formulation:** Apply **Kirchhoff's Current Law** and **Ohm's Law** to each unknown node to derive a $2\times 2$ system of linear equations $\mathbf{A}\mathbf{V} = \mathbf{I}$.
* **Tasks:**
    1.  Define the $2\times 2$ conductance matrix $\mathbf{A}$ and the RHS vector $\mathbf{I}$.
    2.  Use `np.linalg.solve(A, I)` to find the unknown voltage vector $\mathbf{V}=[V_1, V_2]^T$.
    3.  Plot the circuit diagram (optional) and clearly label the calculated voltages.

**2. Project: LU Decomposition Efficiency Test**

* **Problem:** Demonstrate the computational advantage of LU decomposition for solving multiple systems compared to matrix inversion.
* **Formulation:** Use a random dense $N \times N$ matrix $\mathbf{A}$ and solve $\mathbf{A}\mathbf{x} = \mathbf{b}$ one thousand times.
* **Tasks:**
    1.  Define a large matrix $\mathbf{A}$ (e.g., $N=1000$).
    2.  **Method A (Inversion):** Use `A_inv = np.linalg.inv(A)` once, then calculate $\mathbf{x} = \mathbf{A}^{-1}\mathbf{b}$ one thousand times, recording the total time.
    3.  **Method B (LU/Solve):** Use `x = np.linalg.solve(A, b)` one thousand times, recording the total time.
    4.  **Analysis:** Show that Method B is significantly faster than Method A, validating the chapter's "Do Not Do This" warning.

**3. Project: The Tridiagonal Solver (Thomas Algorithm)**

* **Problem:** Solve the tridiagonal system $\mathbf{A}\mathbf{y} = \mathbf{b}$ that results from the FDM BVP (Chapter 9) using the specialized Thomas Algorithm solver.
* **Formulation:** Use the simple BVP $y'' = -x^2$ with $y(0)=0, y(1)=0$. The matrix $\mathbf{A}$ is tridiagonal with a constant structure ($[1, -2, 1]$).
* **Tasks:**
    1.  Build the RHS vector $\mathbf{b}$ (including boundary contributions).
    2.  Use `scipy.linalg.solve_banded` (SciPy's implementation of the Thomas Algorithm) to find the solution vector $\mathbf{y}$.
    3.  Plot the solution and verify its accuracy against the analytic solution $y(x) = (1/12)(x-x^4)$.

**4. Project: The Gauss-Seidel Iterative Solution**

* **Problem:** Implement the **Gauss-Seidel** iterative solver (from Chapter 10) and use it to solve a medium-sized system, comparing its result to the direct solution.
* **Formulation:** Use the resistor network problem ($\mathbf{A}\mathbf{V} = \mathbf{I}$) with a larger $N$ (e.g., $N=10$ nodes).
* **Tasks:**
    1.  Implement the Gauss-Seidel iterative update loop (using the same $\mathbf{A}$ and $\mathbf{I}$ from the direct method).
    2.  Solve the system using `np.linalg.solve()` (the direct solution) to get the "true" answer.
    3.  Run the Gauss-Seidel solver until it converges (e.g., tolerance $10^{-6}$).
    4.  **Analysis:** Plot the absolute error of the Gauss-Seidel solution vs. the iteration number (on a semilog plot) and compare the final solution vector to the direct solution vector.

**5. Project: Finding the Optimal $\mathbf{b}$ for a Target $\mathbf{x}$**

* **Problem:** Given a desired outcome vector $\mathbf{x}_{\text{target}}$ (e.g., the final temperatures in a room) and a fixed system matrix $\mathbf{A}$ (the geometry of the room's heat flow), find the required driving source vector $\mathbf{b}$ (the heat inputs/outputs) that produces that outcome.
* **Formulation:** This is still $\mathbf{A}\mathbf{b} = \mathbf{x}$. The problem is rewritten as $\mathbf{A}\mathbf{b} = \mathbf{x}$.
* **Tasks:**
    1.  Define a random, fixed $N \times N$ matrix $\mathbf{A}$ and a desired target vector $\mathbf{x}_{\text{target}}$.
    2.  Solve the system $\mathbf{A}\mathbf{b} = \mathbf{x}_{\text{target}}$ for the unknown source vector $\mathbf{b}$.
    3.  **Verification:** Plug the calculated $\mathbf{b}$ back into the original system and solve for the output $\mathbf{x}$. Show that $\mathbf{x}$ equals $\mathbf{x}_{\text{target}}$.