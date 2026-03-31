# **Chapter 6: Numerical Integration**

---

# **Introduction**

In the previous chapter, we mastered the derivative—the language of instantaneous change. We now turn to its inverse: the **integral** ($\int f(x) dx$), the language of **total accumulation**. Integration is how we sum up a quantity that is continuously changing over a given domain. Whether we are calculating the total work done by a variable force, the probability of finding a quantum particle, or the energy flux through a surface, we are performing an act of accumulation.

In the "Digital Lab," we rarely have the luxury of an analytical antiderivative. Instead, we must perform **Numerical Quadrature**: approximating the "area under the curve" by tiling it with simple geometric shapes. This chapter defines the "Standard" for numerical integration, moving from the intuitive **Trapezoidal Rule** to high-order **Gaussian Quadrature**, and finally to **Monte Carlo** methods that bypass the "Curse of Dimensionality."

---

# **Chapter 6: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **6.1** | **The Physics of Accumulation** | Work, flux, and probability; the "Staircase" problem; area as a finite sum. |
| **6.2** | **Newton-Cotes Formulas** | Extended Trapezoidal Rule ($O(h^2)$); Simpson's Rule ($O(h^4)$); weighting schemes. |
| **6.3** | **Gaussian Quadrature** | Optimal node placement; orthogonal polynomials; the `scipy.integrate.quad` standard. |
| **6.4** | **Taming Singularities** | Change of variables; handling $1/\sqrt{x}$ and infinite limits; adaptive subdivision. |
| **6.5** | **Monte Carlo Integration** | The Curse of Dimensionality; stochastic sampling; $1/\sqrt{N}$ error scaling. |

---

## **6.1 Newton-Cotes Formulas: Tiling the Area**

---

The most common way to integrate discrete data is to divide the domain $[a, b]$ into $N$ equal "panels" of width $h$ and approximate the function within each panel.

### **The Trapezoidal Rule ($O(h^2)$)**
Approximates each panel with a straight line.
$$ I \approx \frac{h}{2} [f(a) + 2\sum f(x_i) + f(b)] $$
It is robust but relatively slow to converge.

### **Simpson's Rule ($O(h^4)$)**
Approximates each pair of panels with a **parabola**. This produces a significant jump in accuracy for the same number of function evaluations.
$$ I \approx \frac{h}{3} [f(x_0) + 4f(x_1) + 2f(x_2) + 4f(x_3) \dots + f(x_N)] $$

!!! tip "The Magic of Simpson"
    Simpson's Rule is technically derived from a 2nd-degree polynomial (parabola), yet it is **4th-order accurate** for many functions. This "extra" order of accuracy occurs because the error terms associated with cubic polynomials cancel out perfectly due to symmetry.

---

## **6.2 Gaussian Quadrature: Optimal Sampling**

---

Newton-Cotes formulas use **equidistant** points. **Gaussian Quadrature** asks: "Where should we place the points to get the most accurate answer?"

By using specifically calculated points (the roots of Legendre polynomials) and weights, Gaussian Quadrature can integrate a polynomial of degree $2N-1$ **exactly** using only $N$ points.

!!! example "The 'Quad' Standard"
    In professional Python code, `scipy.integrate.quad` uses a sophisticated version of Gaussian Quadrature (Clenshaw-Curtis or Gauss-Kronrod). It is **adaptive**, meaning it automatically adds more points in regions where the function is changing rapidly.

---

## **6.3 Taming Singularities and Infinity**

---

Many physical integrals are "improper"—they have infinite limits or blow up at a boundary (e.g., $1/\sqrt{x}$ at $x=0$).

**Strategies:**
1.  **Change of Variables:** Map $[0, \infty)$ to $[0, 1]$ using a transformation like $u = 1/(1+x)$.
2.  **Adaptive Subdivision:** Place an infinite density of points near the singularity (what `quad` does internally).

??? question "Can we integrate a singularity?"
    Yes, as long as the integral is **convergent**. For example, $\int_0^1 x^{-1/2} dx = 2$, even though the function value is infinite at $x=0$. Numerical methods like `quad` can handle this by avoiding the exact point $x=0$.

---

## **6.4 Monte Carlo: Beating the Curse**

---

For 1D integrals, Simpson's Rule is king. But for a 10-dimensional integral (common in statistical mechanics), a grid of only 10 points per dimension requires $10^{10}$ evaluations—an impossible task. This is the **Curse of Dimensionality**.

**Monte Carlo Integration** solves this by sampling points **randomly**:
1.  Pick $N$ random points in the volume.
2.  Average the function values at these points.
3.  Multiply by the total volume.

```mermaid
graph LR
    A[Grid Methods] --> B[Error O(h^k)]
    A --> C[Exponential Cost in D]
    D[Monte Carlo] --> E[Error O(1/sqrt N)]
    D --> F[Independent of Dimension D]
    C --> G{D > 8?}
    F --> G
    G -- Yes --> D
    G -- No --> A
```

!!! tip "The $1/\sqrt{N}$ Law"
    The error in Monte Carlo always scales as $1/\sqrt{N}$, regardless of whether you are integrating in 1D or 1000D. This makes it the only viable tool for high-dimensional physics.

---

## **Summary: Integration Method Comparison**

---

| Method | Order | Optimal For | Note |
| :--- | :--- | :--- | :--- |
| **Trapezoidal** | $\mathcal{O}(h^2)$ | Real-time / Rough data | Simple and robust |
| **Simpson's** | $\mathcal{O}(h^4)$ | Smooth fixed-grid data | The "Go-to" for 1D |
| **Gaussian** | Highly Variable | **Callable Functions** | **Industry Standard (`quad`)** |
| **Monte Carlo** | $\mathcal{O}(1/\sqrt{N})$ | **High-Dimensional ($D > 8$)** | Stochastic and Dimension-blind |

---

## **References**

---

[1] Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing*. Cambridge University Press.

[2] Krommer, A. R., & Ueberhuber, C. W. (1998). *Computational Integration*. SIAM.

[3] Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis*. Brooks/Cole.

[4] Metropolis, N., & Ulam, S. (1949). The Monte Carlo Method. *Journal of the American Statistical Association*.

[5] Piessens, R., et al. (1983). *QUADPACK: A Subroutine Package for Automatic Integration*. Springer-Verlag.