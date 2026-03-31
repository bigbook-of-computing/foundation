# **Chapter 5: Numerical Differentiation**

---

# **Introduction**

In the "Digital Lab," we rarely possess the luxury of a continuous, analytical formula for every physical process. Instead, we often work with discrete sets of observations—individual data points collected from experiments, sensors, or sparse simulations. To understand the dynamics of these systems, we must compute their rates of change—their derivatives—using only these discrete values.

This chapter defines the "Standard" for **Numerical Differentiation**. We will transition from the limit definition of calculus to the algebraic reality of **Finite Differences** using the power of the **Taylor Series**. However, we will also discover a fundamental paradox: in numerical calculus, taking a "smaller" step does not always lead to a better answer. We must navigate the "Great War" between **Truncation Error** and **Round-off Error** to find the optimal resolution for our digital calculations.

---

# **Chapter 5: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **5.1** | **The Calculus of Grids** | Force as $-dV/dx$; velocity and acceleration; discrete slopes; the Taylor Series bridge. |
| **5.2** | **First-Order Schemes** | Forward and Backward differences; $O(h)$ accuracy; the cost of asymmetry. |
| **5.3** | **Central Difference (The Standard)** | Symmetric 3-point stencil; $O(h^2)$ accuracy; error cancellation "magic." |
| **5.4** | **Higher-Order Derivatives** | The 1D Laplacian ($f''$); acceleration and curvature; three-point stencils. |
| **5.5** | **The Error V-Plot (The Great War)** | Truncation vs. Round-off; the "Sweet Spot" step size; the $\sqrt{\epsilon_m}$ rule. |
| **5.6** | **Differentiating Noisy Data** | Noise amplification;为何 differentiation acts as a high-pass filter; the need for smoothing. |

---

## **5.1 The Finite Difference Idea: The Taylor Bridge**

---

To compute a derivative from grid data, we use the **Taylor Series** expansion. It allows us to relate the value of a function at a nearby point ($x+h$) to its value and derivatives at the current point ($x$):

$$ f(x+h) = f(x) + h f'(x) + \frac{h^2}{2} f''(x) + \frac{h^3}{6} f'''(x) + \dots $$

By rearranging this series, we can isolate $f'(x)$ and express it in terms of the values we *can* measure ($f(x)$ and $f(x+h)$).

---

## **5.2 Forward vs. Central Differences**

---

### **Forward Difference (First Order)**
The simplest approximation is the "rise over run" from $x$ to $x+h$:
$$ f'(x) \approx \frac{f(x+h) - f(x)}{h} + \mathcal{O}(h) $$
It is **First-Order Accurate**—halving the step $h$ only halves the error.

### **Central Difference (Second Order)**
By using two symmetric points ($x-h$ and $x+h$), we achieve "magic" cancellation of the $h^2$ error term:
$$ f'(x) \approx \frac{f(x+h) - f(x-h)}{2h} + \mathcal{O}(h^2) $$
This is **Second-Order Accurate**—halving $h$ reduces the error by a factor of **four**. This is the standard "workhorse" for numerical derivatives.

!!! tip "Centered is Standard"
    Whenever possible, use symmetric (centered) stencils. They provide higher accuracy for the same computational effort because the anti-symmetric nature of the derivative cancels out even-order error terms automatically.

---

## **5.3 Higher-Order Derivatives: The Laplacian**

---

To find acceleration or curvature, we need the second derivative $f''(x)$. By adding the forward and backward Taylor expansions, we isolate the $f''$ term:

$$ f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2} + \mathcal{O}(h^2) $$

This **Three-Point Stencil** is the fundamental building block for solving physical field equations, such as the Heat Equation or the Schrödinger Equation.

---

## **5.4 The "Great War" of Errors: The V-Plot**

---

In calculus, we take the limit as $h \to 0$. In computers, this is a **recipe for disaster**.

1.  **Truncation Error ($E_T \propto h^2$):** Dominates when $h$ is large.
2.  **Round-off Error ($E_R \propto \epsilon_m / h$):** Dominates when $h$ is small. As $h$ shrinks, the numerator $f(x+h) - f(x-h)$ suffers from **catastrophic cancellation**, and we divide the resulting noise by a tiny $h$, magnifying it.

```mermaid
graph TD
    A[Total Error] --> B[Truncation O(h^2)]
    A --> C[Round-off eps/h]
    B -- h decreases --> B_low[Error Goes Down]
    C -- h decreases --> C_high[Error Explodes!]
    B_low --> D[Sweet Spot]
    C_high --> D
```

!!! example "The Sweet Spot Rule"
    For a second-order formula, the optimal step size $h$ is approximately:
    $$ h_{\text{opt}} \approx \sqrt[3]{\epsilon_m} \approx 10^{-5} \text{ to } 10^{-6} $$
    If you use $h = 10^{-15}$, your "derivative" will be $100\%$ noise.

---

## **5.5 Differentiating Noisy Data**

---

Numerical differentiation is an **inherently unstable** operation. Because it involves subtraction of nearby points, it acts as a **high-pass filter**. It amplifies high-frequency noise while preserving (or dampening) the low-frequency signal.

??? question "How do we differentiate experimental data?"
    **Never** differentiate raw, noisy experimental data directly. You must first **smooth** the data using a fit (Chapter 4) or a filter (Chapter 15), and then differentiate the smooth surrogate model.

---

## **Summary: Differentiation Scheme Comparison**

---

| Scheme | Stencil | Accuracy | Best For |
| :--- | :--- | :--- | :--- |
| **Forward** | $[x, x+h]$ | $\mathcal{O}(h)$ | Real-time causal signals |
| **Backward** | $[x-h, x]$ | $\mathcal{O}(h)$ | Implicit solvers |
| **Central** | $[x-h, x+h]$ | $\mathcal{O}(h^2)$ | **Most offline physics tasks** |
| **Three-Point** | $[x-h, x, x+h]$ | $\mathcal{O}(h^2)$ | Second derivatives ($f''$) |

---

## **References**

---

[1] Press, W. H., et al. (2007). *Numerical Recipes: The Art of Scientific Computing*. Cambridge University Press.

[2] Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[3] Burden, R. L., & Faires, J. D. (2011). *Numerical Analysis*. Brooks/Cole.

[4] Hamming, R. W. (1973). *Numerical Methods for Scientists and Engineers*. McGraw-Hill.

[5] Lanczos, C. (1956). *Applied Analysis*. Prentice-Hall.