# **Introduction**

Derivatives are the central language of change in physics. Force, velocity, acceleration, curvature, flux—each is defined not by a value at a point, but by how a quantity varies *between* points. Yet the computer cannot access the smooth continuum on which the derivative is defined. It sees only discrete grid values: $f(x_0), f(x_1), f(x_2), \dots$. The challenge, then, is to reconstruct the continuous behavior of $f(x)$ well enough to approximate its rate of change.

This chapter reveals how numerical differentiation transforms the machinery of calculus into finite algebra using the **Taylor series**. It also introduces one of the most important practical lessons of computational physics: differentiation is inherently unstable. Making the grid spacing $h$ extremely small—intuitively desirable—invites catastrophic round-off error, while making $h$ too large introduces overwhelming truncation error. The key is to navigate the “war” between these competing forces to locate the **optimal** value of $h$.

By the end of this chapter, the derivative becomes not an abstract limit but a carefully engineered approximation, one that demands attention to both floating-point realities and algorithmic structure. This work becomes essential preparation for the more advanced numerical methods and differential-equation solvers to follow.

---

# **Chapter 5: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **5.1** | **Why Differentiation Matters** | Derivatives as the language of change; force as $-dV/dx$; velocity, acceleration, curvature; computing slopes from discrete grid data. |
| **5.2** | **The Taylor Series Engine** | Forward/backward expansions; building finite-difference formulas; Taylor series as the bridge from calculus to algebra. |
| **5.3** | **Forward Difference (First Attempt)** | Derivation from $f(x+h)$; first-order truncation error $O(h)$; slow convergence; intuitive but inefficient. |
| **5.4** | **Central Difference (The Workhorse)** | Symmetric stencil using $x\pm h$; cancellation of low-order terms; second-order accuracy $O(h^2)$; superior precision. |
| **5.5** | **Second Derivative and the Laplacian** | Three-point stencil for $f''(x)$; second-order accuracy; numerical Laplacian as foundation for PDEs (Heat, Wave, Schrödinger). |
| **5.6** | **The War Between Errors** | Truncation vs. round-off; catastrophic cancellation at small $h$; total error model $C h^2 + D\epsilon_m/h$; V-plot and optimal step size. |
| **5.7** | **Application: Lennard-Jones Force** | Numerical vs. analytic force; using optimal $h$ to reach machine-precision accuracy; demonstration of $10^{-14}$–$10^{-15}$ error limits. |

---

## **5.1 Why Differentiation Matters**

The entirety of physics is built on the concept of **change**, and the derivative, $\frac{df}{dx}$, is the fundamental language used to quantify and describe that change. Dynamic systems, from classical motion to quantum fields, are modeled using this operator:

* **Classical Mechanics:** The force $F(x)$ is defined as the negative instantaneous **rate of change** of potential energy $V$:
  
```
$$
F(x) = -\frac{dV}{dx}
$$

```
* **Dynamics:** Velocity $v(t)$ and acceleration $a(t)$ are the first and second derivatives of position $x(t)$ with respect to time, respectively:
  
```
$$
v(t) = \frac{dx}{dt} \quad \text{and} \quad a(t) = \frac{d^2x}{dt^2}
$$

```
* **Fundamental Laws:** The cornerstone equations of theoretical physics—such as the Schrödinger Equation [4], the Heat Equation, and the Wave Equation [5]—are all **differential equations**.

The **computational problem** is that the computer does not operate in the continuous domain of $V(x)$. Instead, it works with **discrete data on a grid**. We may have the potential $V(x_i)$ at evenly-spaced points $x_0, x_1, x_2, \dots$. Our core challenge is to compute the derivative (the "slope") accurately and efficiently **from the raw grid data itself**.

The solution involves using the Taylor series to derive simple **finite difference formulas** [1, 3], transforming continuous calculus into finite algebra. This journey forces us to confront the core "great war" of computational physics: the trade-off between algorithmic error and hardware error.

---

## **5.2 The Taylor Series Engine**

The **Taylor series** is the foundational mathematical tool—the "oracle"—used to derive every finite difference formula [1]. It acts as the bridge between the continuous world of derivatives and the discrete world of grid-point arithmetic.

The Taylor expansion states that if the function's value $f(x)$ and all its derivatives ($f'(x), f''(x), \dots$) are known at a single point $x$, we can predict the function's value at a nearby point $x+h$. The two essential expansions needed for numerical differentiation, written around the point $x$, are:

1.  **Stepping forward** by a distance $h$:
```
$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + \dots
$$

```
2.  **Stepping backward** by a distance $h$:
```
$$
f(x-h) = f(x) - h f'(x) + \frac{h^2}{2!} f''(x) - \frac{h^3}{3!} f'''(x) + \dots
$$

```
By **adding, subtracting, and rearranging** these expansions, we can isolate the desired derivatives $f'(x)$ and $f''(x)$, expressing them only in terms of the grid values $f(x), f(x+h),$ and $f(x-h)$.

---

## **5.3 Forward Difference (First Attempt)**

The **Forward Difference** method is the most intuitive approximation of the derivative, defining the slope at $x$ by looking at the change between $x$ and the next point $x+h$.

---

### **Derivation and Formula**

Starting with the forward Taylor expansion and **truncating** all terms of order $h^2$ and higher ($O(h^2)$) yields:

$$
f(x+h) \approx f(x) + h f'(x) + O(h^2)
$$

Solving for $f'(x)$ gives the formula:

$$
f'(x) \approx \frac{f(x+h) - f(x)}{h}
$$

---

### **Truncation Error ($O(h)$)**

The error **truncated** from the Taylor series was $O(h^2)$. However, since the final formula involves **division by $h$**, the total **Truncation Error** in the result is reduced to $O(h)$:

$$
\text{Error} = \frac{O(h^2)}{h} = O(h)
$$

This makes the Forward Difference a **first-order accurate** algorithm. The error is linearly proportional to the step size $h$; thus, halving the grid spacing $h$ only halves the error. This slow rate of convergence is computationally inefficient.

---

## **5.4 Central Difference (The Workhorse)**

The **Central Difference** method is the computational "workhorse" for the first derivative, achieving a vast increase in accuracy (from $O(h)$ to $O(h^2)$) by centering the calculation at $x$ using both the preceding point ($x-h$) and the succeeding point ($x+h$).

---

### **Derivation and Formula**

The key to the Central Difference method is to **subtract** the backward Taylor expansion from the forward expansion:

$$
f(x+h) - f(x-h) = [f(x) - f(x)] + [h f'(x) - (-h f'(x))] + [\frac{h^2}{2} f''(x) - \frac{h^2}{2} f''(x)] + \dots
$$

The terms containing $f(x)$ and the **second derivative $f''(x)$ cancel out perfectly**. After solving for $f'(x)$, the formula is:

$$
f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}
$$

---

### **Truncation Error ($O(h^2)$)**

Because the largest error term, $O(h^2)$, was cancelled in the subtraction, the first term truncated was $O(h^3)$. Dividing by $2h$ means the final **Truncation Error** is $O(h^2)$:

$$
\text{Error} = \frac{O(h^3)}{2h} = O(h^2)
$$

This **second-order accuracy** is the method's "magic": cutting the step size $h$ in half reduces the truncation error by a factor of **four** ($1/2^2$), making it vastly superior and the generally preferred choice over the Forward Difference method [3].

!!! tip "The Power of Symmetry"
```
The Central Difference formula is so accurate because its **symmetric** nature causes the even-powered error terms ($h^2, h^4, \dots$) in the Taylor expansion to cancel out perfectly. This "free lunch" is a core principle in designing good numerical algorithms.

```
```python
def forward_difference(f, x, h=1e-5):
    return (f(x + h) - f(x)) / h
```

---

## **5.5 Second Derivative (The "Laplacian")**

The **second derivative** ($f''(x)$) is essential for modeling acceleration and curvature and is the core component of most fundamental Partial Differential Equations (PDEs) in physics.

---

### **Derivation and Formula**

To isolate $f''(x)$, we **add** the forward and backward Taylor expansions:

$$
f(x+h) + f(x-h) = [f(x) + f(x)] + [h f'(x) - h f'(x)] + [\frac{h^2}{2} f''(x) + \frac{h^2}{2} f''(x)] + \dots
$$

The terms containing the first derivative $f'(x)$ and the third derivative $f'''(x)$ **cancel out**. Solving for $f''(x)$ yields the formula:

$$
f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}
$$

---

### **The 1D Numerical Laplacian**

The formula is **second-order accurate** with a truncation error of $O(h^2)$. Critically, this algebraic expression, also known as the **three-point stencil**, is the fundamental approximation for the **Laplacian operator** ($\nabla^2$) in one dimension. It forms the core mathematical foundation for numerically solving physical systems governed by the Heat, Wave, and Schrödinger Equations [4, 5].

---

## **5.6 The War Between Errors and the "Sweet Spot"**

The $O(h^2)$ truncation rule suggests making the step size $h$ **"as small as possible"** to minimize error. However, the constraints of **floating-point arithmetic** (Chapter 2) declare this advice **disastrous** [2].

---

### **The Dilemma: Truncation vs. Round-off**

The total error in a numerical derivative is the result of a "war" between two opposing sources:

1.  **Truncation Error ($E_{\text{trunc}}$):** The error from the approximate algorithm. It **decreases** as $h$ decreases:
```
$$
E_{\text{trunc}} \propto h^2
$$

```
2.  **Round-off Error ($E_{\text{round}}$):** The error from the computer's finite precision ($\epsilon_m$), amplified by the formula. It **explodes** as $h$ decreases:
```
$$
E_{\text{round}} \propto \frac{\epsilon_m}{h}
$$

```
When $h$ becomes tiny (e.g., $h \sim 10^{-15}$), the numerator of the Central Difference formula, $f(x+h) - f(x-h)$, suffers **catastrophic cancellation** (the Chapter 2 bug), where the accurate signal is replaced by amplified round-off noise [2]. This noise is then massively amplified by dividing by the tiny denominator $2h$.

```mermaid
    flowchart TD
    A(Start: Choose step size h) --> B{Is h very small?}
    B -- Yes --> C[Round-off Error Dominates <br/> (Catastrophic Cancellation <br/> divided by small h)]
    C --> F(Total Error is HIGH)
    B -- No --> D{Is h very large?}
    D -- Yes --> E[Truncation Error Dominates <br/> (Algorithm approximation $O(h^2)$ is poor)]
    E --> F
    D -- No --> G[h is "Just Right" <br/> (Optimal h)]
    G --> H(Total Error is LOW <br/> "Sweet Spot")
```

---

### **The "Sweet Spot" V-Plot**

The **Total Error** is the sum of these two opposing components:

$$
E_{\text{Total}} \approx C \cdot h^2 + D \cdot \frac{\epsilon_m}{h}
$$

A log-log plot of $\text{Error}$ vs. $h$ reveals a characteristic **"V" shape**:

* The **right side** ($h$ large) has a slope of $+2$ and is dominated by **Truncation Error**.
* The **left side** ($h$ small) has a slope of $-1$ and is dominated by **Round-off Error**.

The **"sweet spot"** is the minimum point at the bottom of the "V" where the two error sources are perfectly balanced, typically around $h \sim 10^{-5}$ to $10^{-6}$ for 64-bit precision [1]. The crucial lesson is that the **most accurate answer** is found at this optimal $h$, not at the smallest possible $h$.

??? question "Where does the optimal h come from?"
You can find it analytically\! By taking the derivative of the total error $E_{\text{Total}}(h)$ with respect to $h$ and setting it to zero ($dE/dh = 0$), you can solve for the $h$ that minimizes the error. This confirms the optimal $h$ scales with $\epsilon_m^{1/3}$ for this $O(h^2)$ formula.

---

## **5.7 Core Application: Force from a Lennard-Jones Potential**

The calculation of force $F(r)$ from the interatomic **Lennard-Jones (LJ) potential** $V(r)$ via the relationship:

$$
F(r) = -\frac{dV}{dr}
$$

serves as a critical test of numerical differentiation.

The **computational strategy** is to use the analytically known force, $F_{\text{analytic}}(r)$, as the **"ground truth"** to verify the accuracy of the numerical result. The numerical force, $F_{\text{numeric}}(r)$, is found by applying the $O(h^2)$ Central Difference formula to the potential $V(r)$ using the **optimal step size $h$** determined from the V-plot analysis.

By choosing this optimal $h$ (e.g., $10^{-6}$), the method successfully avoids the major error sources. When the absolute error $\|F_{\text{numeric}} - F_{\text{analytic}}\|$ is plotted, it reveals values down to $10^{-14}$ or $10^{-15}$, confirming that the numerical method is stable and accurate to the **limit of machine precision** for 64-bit floats.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

[2] Higham, N.J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[3] Quarteroni, A., Sacco, R., & Saleri, F. (2007). *Numerical Mathematics*. Springer.

[4] Hamming, R. W. (1973). *Numerical Methods for Scientists and Engineers* (2nd ed.). McGraw-Hill.

[5] Süli, E., & Mayers, D. F. (2003). *An Introduction to Numerical Analysis*. Cambridge University Press.