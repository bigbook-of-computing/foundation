# **Chapter 14: Eigenvalue Problems (Workbook)**

---

> **Summary:** This workbook explores the physics of **Natural States**. We solve the "Natural Problem" ($\mathbf{A}\mathbf{x} = \lambda \mathbf{x}$) to find intrinsic properties like atomic energy levels, vibration frequencies, and principal directions. You will learn the **Power Method**, the robust **QR Algorithm**, and how to find the Quantum Ground State using **Inverse Iteration**.

---

## **14.1 The Physics of "Natural States"** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Natural Modes and Eigenvalues
> 
> **Summary:** We define the Eigenvalue Problem as the search for the characteristic states of a system matrix. This section bridges mechanical oscillators and the Schrödinger Equation, identifying why "natural" frequencies and energies are the eigenvalues of our physical operators.

These intrinsic properties define the core characteristics of a physical system:
* **Allowed Energies:** The discrete, quantized energy levels of a quantum particle.
* **Normal Modes:** The fundamental frequencies and shapes of vibration in a coupled mechanical system.
* **Dominant Patterns:** The principal axes of variance in a high-dimensional dataset (Chapter 16).

**The Eigenvalue Equation**

All these problems are unified by the single equation of the **Eigenvalue Problem**:

$$\mathbf{A}\mathbf{v} = \lambda \mathbf{v}$$

We are looking for the "special" vectors $\mathbf{v}$ (**eigenvectors**) that, when transformed by the matrix $\mathbf{A}$, only change their *magnitude*. The scaling factor $\lambda$ is the **eigenvalue**.

* **The Bridge:** This problem is the **exact mathematical form** of the 1D Schrödinger Equation we derived using FDM in Chapter 9.

---

## **14.2 Method 1: The Power Iteration** {.heading-with-pill}

> Summary: The **Power Iteration** is a simple iterative method that finds the **dominant eigenvalue** ($\lambda_{\text{dom}}$, the largest in magnitude) by repeatedly multiplying the system matrix $\mathbf{A}$ by a random initial vector $\mathbf{v}_0$.

**The "Analogy": Plucking a Guitar String**

Imagine plucking a guitar string: the initial motion contains a mix of all possible harmonics (eigenvectors). However, the sound you hear is quickly dominated by the fundamental, lowest-frequency note (the **dominant mode**).

* **Theory:** When $\mathbf{A}$ is repeatedly applied to any random vector $\mathbf{v}_0$, the component corresponding to the largest eigenvalue ($\lambda_{\text{dom}}$) grows the fastest and eventually "dominates" the result.
* **Formula:** $\mathbf{v}_{k+1} = \mathbf{A}\mathbf{v}_k$ (followed by normalization).

**Finding the Smallest Eigenvalue (The Inverse Trick)**

To find the **smallest** eigenvalue (like the quantum ground state energy), the Power Iteration is run on the **inverse matrix, $\mathbf{A}^{-1}$**. This works because the smallest eigenvalue of $\mathbf{A}$ is the *dominant* eigenvalue of $\mathbf{A}^{-1}$. Crucially, we **never explicitly compute $\mathbf{A}^{-1}$**; we use the fast solver techniques of Chapter 13 to solve $\mathbf{A}\mathbf{v}_{k+1} = \mathbf{v}_k$ at each step.

**Limitations:** The Power Iteration is slow if $\lambda_{\text{dom}}$ is very close to the next largest eigenvalue, and it only finds one eigenvalue at a time.

### **Comprehension Check**

!!! note "Quiz"
    **1. The Power Iteration algorithm is best suited for finding which component of the eigenvalue spectrum?**
    
    - A. The median eigenvalue.
    - B. The smallest eigenvalue.
    - C. **The dominant eigenvalue (largest in magnitude).**
    - D. All eigenvalues simultaneously.
    
??? info "See Answer"
        **Correct: C**  
        Like a plucked string, the strongest mode eventually dominates after repeated applications.

!!! note "Quiz"
    **2. To find the smallest eigenvalue using the Power Iteration method, one must apply the iteration to which matrix?**
    
    - A. The original matrix $\mathbf{A}$.
    - B. **The inverse matrix $\mathbf{A}^{-1}$ (using a solver to avoid explicit inversion).**
    - C. The transpose matrix $\mathbf{A}^T$.
    - D. The identity matrix.
    
??? info "See Answer"
        **Correct: B**  
        The smallest eigenvalue of $\mathbf{A}$ is the reciprocal of the largest eigenvalue of $\mathbf{A}^{-1}$.

!!! abstract "Interview-Style Question"
    **Question:** Explain the philosophical reason why one must normalize the resulting vector ($\mathbf{v}_{k+1} = \mathbf{w} / ||\mathbf{w}||$) at each step of the Power Iteration.
    
    ???+ info "Answer Strategy"
        Normalization prevents the components of the vector from growing indefinitely and causing a **floating-point overflow** (Chapter 2). The eigenvalue $\lambda_{\text{dom}}$ is simply the magnitude of the growth ($||\mathbf{w}||$), and the normalized vector $\mathbf{v}$ converges to the **direction** of the eigenvector.

---

## **14.3 Method 2: The QR Algorithm** {.heading-with-pill}

> Summary: The **QR Algorithm** is the iterative, $\mathcal{O}(N^3)$ workhorse for finding **all** eigenvalues and eigenvectors of a dense matrix simultaneously. It works by iteratively rotating the matrix until it converges to a triangular form where the eigenvalues lie on the diagonal.

The **QR Algorithm** is the standard, high-level method used inside libraries like `numpy.linalg.eig` for finding the **complete set** of eigenvalues and eigenvectors.

**The Concept: Iterative Diagonalization**

The QR Algorithm operates by factoring the matrix $\mathbf{A}$ into an orthogonal matrix ($\mathbf{Q}$) and an upper-triangular matrix ($\mathbf{R}$) at each step, then recombining the factors in reverse order:
1.  **Decompose:** $\mathbf{A}_k = \mathbf{Q}_k \mathbf{R}_k$
2.  **Recombine:** $\mathbf{A}_{k+1} = \mathbf{R}_k \mathbf{Q}_k$

This process iteratively rotates the matrix $\mathbf{A}$ until it converges to an upper-triangular form. The entries on the **main diagonal of the final matrix are the eigenvalues**.

**Performance:** The QR Algorithm is an $\mathcal{O}(N^3)$ method, suitable for small-to-medium-sized **dense** matrices where *all* states are required.

### **Comprehension Check**

!!! note "Quiz"
    **1. The QR Algorithm works by iteratively transforming the matrix $\mathbf{A}$ until the eigenvalues are found where?**
    
    - A. In the first column.
    - B. **On the main diagonal of the resulting triangular matrix.**
    - C. In the determinant.
    - D. They vanish.
    
??? info "See Answer"
        **Correct: B**  
        Each iteration "pushes" non-zero values towards the diagonal.

!!! note "Quiz"
    **2. The QR Algorithm is generally used when the user needs:**
    
    - A. Only the largest eigenvalue.
    - B. Only the eigenvectors.
    - C. **All eigenvalues and eigenvectors simultaneously for a dense matrix.**
    - D. To solve a linear system $\mathbf{A}\mathbf{x} = \mathbf{b}$.
    
??? info "See Answer"
        **Correct: C**  
        It is the "gold-standard" direct method for full spectrum analysis.

!!! abstract "Interview-Style Question"
    **Question:** The QR Algorithm relies on the $\mathbf{A}_{k+1} = \mathbf{R}_k \mathbf{Q}_k$ step. Why does the matrix $\mathbf{A}_{k+1}$ have the *same* eigenvalues as $\mathbf{A}_k$?
    
    ???+ info "Answer Strategy"
        The step $\mathbf{A}_{k+1} = \mathbf{R}_k \mathbf{Q}_k$ can be rewritten as a **similarity transformation**: $\mathbf{A}_{k+1} = (\mathbf{Q}_k^T \mathbf{A}_k) \mathbf{Q}_k$. A similarity transformation preserves the eigenvalues of the matrix. The iterative process applies a sequence of orthogonal rotations (which preserve lengths and angles) until the new basis (the eigenvectors) naturally reveals the scaling factors (the eigenvalues).

## **14.4 Method 3: Specialized Solvers and the Hermitian Property** {.heading-with-pill}

> Summary: Professional libraries provide specialized solvers (like $\text{eigh}$) that exploit the **Hermitian (symmetric)** property of many physics matrices ($\mathbf{A} = \mathbf{A}^T$) for guaranteed real eigenvalues and significantly faster, more stable computation.

**The Professional Approach:** **Never write your own eigensolver** for real work. Optimized libraries are faster and more stable.

**The Hermitian/Symmetric Property:**

* **Physics:** Hamiltonian matrices ($\mathbf{H}$, Chapter 9) and coupled oscillator matrices are *always* **Hermitian** (or real-symmetric, $\mathbf{A} = \mathbf{A}^T$).
* **Guarantee:** This property **guarantees that all eigenvalues are real** (as energy and frequency must be).
* **The Tool ($\text{eigh}$):** Solvers like `np.linalg.eigh` are specialized for this property, using faster algorithms than the general `np.linalg.eig`.
* **Specialist ($\text{eigh\_tridiagonal}$):** For the specific **tridiagonal** matrices resulting from 1D FDM (Chapter 9), `scipy.linalg.eigh_tridiagonal` is even faster, often achieving $\mathcal{O}(N)$ performance.

**Solving Sparse Problems:** For huge, sparse matrices (e.g., 2D PDEs), specialized sparse solvers are required, such as `scipy.sparse.linalg.eigsh`, which only calculates a few of the most important (smallest or largest) eigenvalues.

### **Comprehension Check**

!!! note "Quiz"
    **1. The primary reason a specialized solver like $\text{eigh}$ is used instead of the general $\text{eig}$ in computational physics is that $\text{eigh}$ is designed to exploit which property of the Hamiltonian matrix?**
    
    - A. The fact that it is a small matrix.
    - B. **The Hermitian (symmetric) property, ensuring real eigenvalues and faster computation.**
    - C. The fact that it is mostly zeros.
    - D. The presence of complex numbers.
    
??? info "See Answer"
        **Correct: B**  
        Symmetry is a fundamental physical law that allows for significant algorithmic optimization.

!!! note "Quiz"
    **2. Which specialized solver is recommended for the tridiagonal matrix that results from the 1D FDM Schrödinger Equation?**
    
    - A. `np.linalg.inv`
    - B. **`scipy.linalg.eigh_tridiagonal`**
    - C. `np.fft.fft`
    - D. `scipy.optimize.minimize`
    
??? info "See Answer"
        **Correct: B**  
        This specialized $O(N)$ solver is the "magic bullet" for 1D quantum problems.

!!! abstract "Interview-Style Question"
    **Question:** The mantra of this section is "never write your own eigensolver." Besides stability, what is the major computational advantage that a specialized library function (like $\text{eigh\_tridiagonal}$) has over a generic $\mathcal{O}(N^3)$ solver?
    
    ???+ info "Answer Strategy"
        A specialized solver exploits the **sparsity** and **structure** of the matrix. For a tridiagonal matrix, the algorithm can be simplified to a recursive process (like the Thomas Algorithm), reducing the complexity from $\mathcal{O}(N^3)$ (for a general matrix) down to **$\mathcal{O}(N)$** or **$\mathcal{O}(N^2)$**. This is essential for large-scale FDM problems where $N$ can be $10^5$.

---

## **14.5 Core Application 1: Normal Modes of Coupled Oscillators** {.heading-with-pill}

> Summary: The system of $F=ma$ equations for coupled oscillators naturally simplifies to a **generalized eigenvalue problem** ($\mathbf{K}\mathbf{v} = \lambda\mathbf{M}\mathbf{v}$), where the **eigenvalues ($\lambda$) are the squared frequencies ($\omega^2$)** and the **eigenvectors ($\mathbf{v}$) are the normal modes** (the intrinsic patterns of motion).

The physics of mechanical systems with multiple coupled degrees of freedom (e.g., two masses connected by springs) is described by a system of linear ODEs.

**The Formulation:** By assuming an oscillatory solution ($\mathbf{x}(t) = \mathbf{v}e^{i\omega t}$) and applying Newton's Second Law, the $F=ma$ equations simplify to the **generalized eigenvalue problem**:

$$\mathbf{K}\mathbf{v} = \lambda \mathbf{M}\mathbf{v}$$

Where $\mathbf{K}$ is the stiffness matrix, $\mathbf{M}$ is the mass matrix, and $\lambda = \omega^2$.

* **Eigenvalues $\lambda$:** Give the **squared frequencies ($\omega^2$)** of the oscillation.
* **Eigenvectors $\mathbf{v}$:** Give the **Normal Modes**—the intrinsic patterns where all masses oscillate at the same frequency ($\lambda$).

---

## **14.6 Core Application 2: 1D Time-Independent Schrödinger Equation** {.heading-with-pill}

> Summary: The FDM discretization of the Schrödinger Equation ($\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$) is the final, most powerful demonstration of the FDM-to-Eigenvalue mapping, yielding the complete spectrum of **allowed energies ($E_n$) and corresponding wavefunctions ($\boldsymbol{\psi}_n$)**.

We revisit the FDM solution from Chapter 9. The second-order differential equation $\frac{-\hbar^2}{2m}\frac{d^2\psi}{dx^2} + V(x)\psi = E\psi$ was mapped onto the **tridiagonal matrix eigenvalue problem**:

$$\mathbf{H}\boldsymbol{\psi} = E\boldsymbol{\psi}$$

**The Solution:** The tridiagonal Hamiltonian matrix $\mathbf{H}$ is built using the FDM stencils, and $\text{scipy.linalg.eigh\_tridiagonal}$ finds the complete set of solutions:
* **Eigenvalues $E_n$:** The discrete, allowed **energy levels**.
* **Eigenvectors $\boldsymbol{\psi}_n$:** The shape of the **wavefunctions** (with the correct number of nodes).

---

## **14.8 Hands-On Projects** {.heading-with-pill}

**1. Project: The Inverse Power Iteration (Quantum Ground State Preview)**
* **Formulation:** Set up the $N \times N$ Hamiltonian matrix $\mathbf{H}$ for the **Particle in a Box** problem (Chapter 9, $V=0$). The ground state energy $E_1$ is the smallest eigenvalue.
* **Tasks:**
    1. Implement the Inverse Power Iteration using `np.linalg.solve(H, v_old)` to avoid explicit inversion.
    2. Start with a random initial vector $\mathbf{v}_0$ and iterate until the solution converges.
* **Goal:** Show that the resulting eigenvalue $\lambda$ converges to the known analytical ground state energy $E_1$.

**2. Project: Comparing Eigensolvers**
* **Formulation:** Set up the tridiagonal Hamiltonian matrix $\mathbf{H}$ for the **Particle in a Box** problem (Chapter 9, $V=0$).
* **Tasks:**
    1. Solve for the eigenvalues using both the general `np.linalg.eig()` and the specialized `scipy.linalg.eigh_tridiagonal()`.
    2. Use Python's `time` module to measure the execution time for both methods on a large matrix (e.g., $N=5000$).
* **Goal:** Show that the specialized solver is significantly faster, validating its use in professional codes.

---

## **14.7 Chapter Summary & Next Steps** {.heading-with-pill}

> Summary: We've established that the most fundamental physics problems (oscillators, quantum states) naturally map to the eigenvalue problem $\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$. Efficiency requires choosing specialized solvers that exploit matrix structure (like $\text{eigh}$ or $\text{eigh\_tridiagonal}$).

**What We Built: The Linear Algebra Engine**
We completed the solution methods for linear algebra: the **driven problem** ($\mathbf{A}\mathbf{x} = \mathbf{b}$) and the **natural problem** ($\mathbf{A}\mathbf{v} = \lambda\mathbf{v}$).

**The Key Lessons:**
* **The Mapping:** FDM and linear algebra are inseparable tools for solving complex differential equations.
* **The Tool:** Professional code requires exploiting the **symmetric (Hermitian)** or **tridiagonal** nature of physics matrices for speed and stability.

**Bridge to Part 6: Analyzing Signals & Data**

We have completed the toolkit for **generating** data (ODEs, PDEs, Linear Algebra). The final challenge of Volume I is to build the algorithms for **analyzing** the results. This final part will cover:
* Finding frequencies in signals (**FFT**, Chapter 15).
* Discovering hidden patterns in high-dimensional data (**PCA**, which is another eigenvalue problem, Chapter 16).
* Modeling chance (**Monte Carlo**, Chapter 17).