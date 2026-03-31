# **Introduction**

Our previous work in **Chapter 13** focused on the **driven problem**, solving the linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$. This determined the system's **response** ($\mathbf{x}$) to an external, known force or source ($\mathbf{b}$).

This chapter pivots to the **natural problem**: calculating the **intrinsic, fundamental properties** of the system itself, assuming there is no external driving force (i.e., $\mathbf{b} = \mathbf{0}$). These intrinsic properties define the core characteristics of a physical system and are revealed by the **Eigenvalue Problem**:

$$
\boxed{\mathbf{A}\mathbf{x} = \lambda \mathbf{x}}
$$

This single equation unifies disparate phenomena across physics and data science:

* **Allowed Energies:** The discrete, quantized energy levels of a quantum particle.
* **Normal Modes:** The fundamental frequencies and shapes of vibration in a coupled mechanical system.
* **Dominant Patterns:** The principal axes of variance in high-dimensional data analysis (Principal Component Analysis, Chapter 16).

The goal of this chapter is to build the dedicated algorithms required to find these "natural states"—the **eigenvalues ($\lambda$)** and the corresponding **eigenvectors ($\mathbf{x}$)**.

# **Chapter 14: Outline**

| Sec.     | Title                     | Core Ideas & Examples                                                                   |
| :------- | :------------------------ | :-------------------------------------------------------------------------------------- |
| **14.1** | The FDM Link: TISE        | $\mathbf{H}\mathbf{\psi} = E\mathbf{\psi}$, mapping calculus to linear algebra. |
| **14.2** | Solution Methods          | Exploiting Symmetric ($\mathbf{A} = \mathbf{A}^T$) and Tridiagonal structure.           |
| **14.3** | Application: Normal Modes | $\mathbf{K}\mathbf{x} = \omega^2\mathbf{M}\mathbf{x}$, natural frequencies.             |
| **14.4** | Summary & Bridge          | Bridge to Part 6: Data Analysis (FFT).                                                  |

---

## **14.1 The FDM Link: The Matrix Eigenvalue Problem**

The computational foundation for solving the **natural problem** was established in **Chapter 9** (Boundary Value Problems) by applying the Finite Difference Method (FDM) to the **Time-Independent Schrödinger Equation** (TISE):

$$
\frac{-\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi
$$

By substituting the FDM stencil for the second derivative and rearranging, the TISE is transformed *exactly* into the matrix eigenvalue problem [4]:

$$
\boxed{\mathbf{H}\mathbf{\psi} = E\mathbf{\psi}}
$$

* **Matrix $\mathbf{H}$ (Hamiltonian):** The system matrix, representing the total energy operator (kinetic + potential).
* **Eigenvalues $E$:** The set of allowed, discrete **Energy Levels** (the physical observable).
* **Eigenvectors $\mathbf{\psi}$:** The corresponding **Wavefunctions** (the spatial profile of the probability distribution).

This direct mapping demonstrates that the solution to a complex differential equation lies in efficiently solving a large system of **Linear Algebra**.

!!! tip "The “Magic Trick” of Computational Physics"
    This transformation is arguably the most important "trick" in the field. It converts a complex analytic problem (a differential equation) into a discrete algebraic problem (a matrix equation). We don't solve the TISE; we solve $\mathbf{H}\mathbf{\psi} = E\mathbf{\psi}$, which computers are brilliant at.
    
---

## **14.2 Solution Methods: Exploiting Matrix Structure**

Solving the full eigensystem for all $\lambda$ and $\mathbf{x}$ is computationally more intensive than solving $\mathbf{A}\mathbf{x} = \mathbf{b}$. The key to efficiency is exploiting the specific structures inherent in physics-based matrices.

---

### **The Importance of Structure**

1. **Symmetric (Hermitian) Matrices:**
   The system matrix $\mathbf{A}$ (or $\mathbf{H}$) is almost always **symmetric** ($\mathbf{A} = \mathbf{A}^T$) or **Hermitian** ($\mathbf{A} = \mathbf{A}^\dagger$).

   *Advantage:* symmetric matrices guarantee **real eigenvalues** and orthogonal eigenvectors.

2. **Tridiagonal Matrices:**
   1D FDM discretizations yield **tridiagonal matrices**.

   *Advantage:* specialized solvers compute eigensystems in $\mathcal{O}(N^2)$ instead of $\mathcal{O}(N^3)$.


??? question "Why are physical matrices so often symmetric?"
    Symmetry ($\mathbf{A} = \mathbf{A}^T$) implies that coupling from particle *i* to *j* equals that from *j* to *i*. This reflects Newton's Third Law and energy conservation.
    
---

### **Specialized Solvers (The Professional Toolkit)**

* **`scipy.linalg.eigh`:** solver for **symmetric/Hermitian** matrices.
* **`scipy.linalg.eigh_tridiagonal`:** optimized solver for **symmetric + tridiagonal** matrices.

---

### **The Power Method (Finding the Dominant Mode)**

1. Start with a random vector $\mathbf{x}_0$.
2. Iterate $\mathbf{x}_{k+1} = \mathbf{A}\mathbf{x}_k$.
3. Normalize at each step.
4. Converges to the eigenvector of the **largest eigenvalue**.

```python
# Algorithm: The Power Method

import numpy as np

def power_method(A, x_k=None, tolerance=1e-9, max_iterations=1000):
    """
    Find the largest eigenvalue and corresponding eigenvector using the power method.

    Parameters:
    A: square matrix
    x_k: initial guess vector (random if None)
    tolerance: convergence tolerance
    max_iterations: maximum number of iterations

    Returns:
    lambda_max: largest eigenvalue
    x_k: corresponding eigenvector
    """
    if x_k is None:
        x_k = np.random.rand(A.shape[0])

    x_k = x_k / np.linalg.norm(x_k)

    for i in range(max_iterations):
        x_k_plus_1 = A @ x_k
        x_k_plus_1 = x_k_plus_1 / np.linalg.norm(x_k_plus_1)

        if np.linalg.norm(x_k_plus_1 - x_k) < tolerance:
            break

        x_k = x_k_plus_1

    lambda_max = (x_k.T @ A @ x_k) / (x_k.T @ x_k)
    return lambda_max, x_k
```

---

## **14.3 Core Application: Normal Modes of Oscillation**

For a coupled system of masses and springs:

$$
\mathbf{K}\mathbf{x} = \omega^2 \mathbf{M} \mathbf{x}
$$

* **$\mathbf{M}$:** Mass matrix
* **$\mathbf{K}$:** Stiffness matrix
* **Eigenvalues:** $\lambda = \omega^2$
* **Eigenvectors:** Mode shapes

Transform to standard form via $\mathbf{A}=\mathbf{M}^{-1}\mathbf{K}$.

!!! example "Two Masses, Three Springs"
    A system with $m_1, m_2$ and $k_1,k_2,k_3$ yields a $2\times 2$ eigenproblem with **symmetric** and **antisymmetric** modes.
    
---

## **14.4 Chapter Summary and Bridge to Part 6: Data Analysis**

This chapter completed the foundation for solving the **natural problem**:

> $$\mathbf{A}\mathbf{x} = \lambda \mathbf{x}$$

Efficiency depends critically on exploiting **symmetry** and **tridiagonal structure**, enabling specialized solvers like `eigh_tridiagonal`.

Next: **Part 6 – Data Analysis**, beginning with **Chapter 15 (FFT)**.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes*.

[2] Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*.

[3] Quarteroni, A., Sacco, R., & Saleri, F. (2007). *Numerical Mathematics*.

[4] Newman, M. (2013). *Computational Physics*.

[5] Virtanen, P. et al. (2020). SciPy 1.0.

[6] Thijssen, J. M. (2007). *Computational Physics*.