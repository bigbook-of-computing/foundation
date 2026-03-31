# **Chapter 14: Linear Algebra II (Eigenvalue Problems)**

---

# **Introduction**

In Chapter 13, we solved the "Driven Problem" ($Ax=b$), where an external force (the source $b$) determined the state of the system $x$. However, some of the most profound questions in physics are "Natural Problems"—what does the system do when left entirely to itself? What are its natural frequencies, its stable configurations, or its allowed energy levels? These questions are answered by the **Eigenvalue Problem**.

$$ \mathbf{A} \mathbf{x} = \lambda \mathbf{x} $$

In this equation, the matrix $\mathbf{A}$ represents the system's internal constraints. We seek the **eigenvalues** ($\lambda$), which are the "characteristic values" (like energy or frequency), and the **eigenvectors** ($\mathbf{x}$), which are the "characteristic shapes" (like wavefunctions or vibrational modes). This chapter moves beyond simple matrix inversion to the iterative algorithms—like the **Power Method** and the **QR Algorithm**—that reveal the hidden spectrum of a physical system.

---

# **Chapter 14: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **14.1** | **The Intrinsic System** | Natural modes vs. Driven response; the Schrödinger connection; $Ax = \lambda x$. |
| **14.2** | **The Power Method** | Finding the dominant eigenvalue; iterative vector multiplication; convergence. |
| **14.3** | **Inverse Iteration** | Finding the smallest (ground state) eigenvalue; the "Shift and Invert" trick. |
| **14.4** | **The QR Algorithm** | Finding the **full spectrum**; orthogonal transformations; eigenvalue "peeling." |
| **14.5** | **Diagonalization & Symmetry** | The Spectral Theorem; why physical matrices are almost always symmetric. |

---

## **14.1 Eigenvalues in Physics: Finding the Resonance**

---

Eigenvalues appear whenever a system has "Natural Modes":
1.  **Classical Mechanics:** The **Normal Modes** of a set of coupled springs. The eigenvalues are the square of the vibrational frequencies ($\omega^2$).
2.  **Quantum Mechanics:** The **Time-Independent Schrödinger Equation**. The eigenvalues are the allowed **Energy Levels** ($E$).
3.  **Data Science:** **Principal Component Analysis (PCA)**. The eigenvalues represent the variance captured by each "Principal Component."

!!! tip "Eigenvalues are Resonances"
    Think of eigenvectors as the "pure notes" a system can play, and eigenvalues as the "pitch" of those notes. Any complex motion of the system can be built by adding these pure notes together.

---

## **14.2 The Power Method: The Dominant Mode**

---

How do you find the largest eigenvalue of a $1000 \times 1000$ matrix without solving a 1000th-degree polynomial? You multiply!
1.  Start with a random vector $x_0$.
2.  Multiply by $A$: $x_{new} = A x_{old}$.
3.  Normalize the vector to keep it from blowing up.
4.  **Repeat.**

```mermaid
graph TD
    A[Random Vector x] --> B[Multiply: x = Ax]
    B --> C[Normalize: x = x / |x|]
    C --> D{Has x converged?}
    D -- No --> B
    D -- Yes --> E[x is the Dominant Eigenvector]
    E --> F[Lambda = x.T A x]
```

!!! example "Quantum Ground State"
    In many physics problems, we only care about the **Ground State** (the lowest energy). By applying the Power Method to the *inverse* matrix $A^{-1}$, we can find the smallest eigenvalue of $A$—this is called **Inverse Iteration**.

---

## **14.3 The QR Algorithm: Solving the Whole Spectrum**

---

If you need **all** the eigenvalues, the Power Method is too slow. The **QR Algorithm** is the desktop standard. It works by "peeling" the matrix until it becomes upper-triangular:
1.  Decompose $A$ into an Orthogonal matrix $Q$ and an Upper-triangular matrix $R$ ($A = QR$).
2.  Multiply them in reverse order: $A_{new} = RQ$.
3.  **Repeat.**
Surprisingly, this process causes the off-diagonal elements of $A$ to shrink to zero, leaving the **entire spectrum** of eigenvalues on the main diagonal.

---

## **14.4 The Importance of Symmetry**

---

Most physical matrices (Hamiltonians, Stiffness matrices) are **Symmetric** ($A = A^T$).
- Symmetric matrices **always** have real eigenvalues (no imaginary frequencies).
- Their eigenvectors are **always** orthogonal (each mode is independent of the others).

??? question "What if the matrix isn't symmetric?"
    Non-symmetric matrices can have complex eigenvalues (representing damped or growing oscillations) and non-orthogonal eigenvectors. These are common in fluids and open systems where energy is not conserved.

---

## **Summary: Eigenvalue Solver Comparison**

---

| Method | Complexity | Best For | Note |
| :--- | :--- | :--- | :--- |
| **Power Method** | $\mathcal{O}(N^2)$ | **Largest** eigenvalue | Simplest to implement |
| **Inverse Iteration**| $\mathcal{O}(N^2)$ | **Smallest** eigenvalue | Uses LU hidden inside |
| **QR Algorithm** | $\mathcal{O}(N^3)$ | **All** eigenvalues | The "Gold Standard" |
| **Lanczos/Arnoldi** | $\mathcal{O}(N)$ | Massive Sparse matrices| Used for huge quantum systems |

---

## **References**

---

[1] Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing*. Cambridge University Press.

[2] Francis, J. G. F. (1961). The QR Transformation. *Physical Review*.

[3] Parlett, B. N. (1998). *The Symmetric Eigenvalue Problem*. SIAM.

[4] Golub, G. H., & Van Loan, C. F. (2013). *Matrix Computations*. Johns Hopkins University Press.

[5] Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.