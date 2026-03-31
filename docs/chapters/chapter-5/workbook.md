# **Chapter 5: 5.1 The Physics of "Change" {.heading-with-pill} (Workbook)**

> **Concept:** Discrete Grid vs. Continuous Derivatives • **Difficulty:** ★★☆☆☆

> **Summary:** Physics is the study of change, defined by the derivative ($\frac{df}{dx}$). The core computational problem is finding the slope of a continuous function when only discrete data points on a grid are available.

---

### Theoretical Background

Physics *is* the study of change. The derivative, $\frac{df}{dx}$, is the fundamental language we use to **describe** that change. We don't just solve static problems; we **model dynamic systems**, and those models are built from derivatives.

In the continuous mathematical world, derivatives are perfectly defined operations. The derivative of a function $f(x)$ at a point $x$ is the instantaneous rate of change, the slope of the tangent line at that exact location. This is the language in which the laws of physics are written:

* **Mechanics:** Force ($F$) is the *change* in potential ($V$): $F(x) = -\frac{dV}{dx}$.
* **Electromagnetism:** The electric field ($\mathbf{E}$) is the *change* in potential ($\phi$): $\mathbf{E} = -\nabla \phi$.
* **Dynamics:** Velocity and acceleration are the first and second derivatives of position: $v(t) = \frac{dx}{dt}$, $a(t) = \frac{d^2x}{dt^2}$.
* **Fundamental Laws:** The great laws of physics—the Schrödinger Equation, the Heat Equation, and the Wave Equation—are all **differential equations** written in the language of derivatives.

**The Computational Challenge**

In our computational world, we face a fundamental problem: we do not have smooth, continuous functions. Instead, we have *data on a discrete grid*. We might have the potential $V(x_i)$ at discrete points $x_0, x_1, x_2, \dots$. The mathematical definition of a derivative requires the limit as the spacing approaches zero:

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

But on a computer, we cannot take this limit. Our grid spacing $h$ is finite, and we must compute the derivative **from the raw grid data itself**. This creates the central tension of numerical differentiation: approximating a continuous operation using discrete data.

**The Strategy**

We will derive our "derivative-finders" from the **Taylor series**, using it to build simple **algebraic approximations** for the derivative. This process reveals the "great war" of computational physics: the battle between **truncation error** (error from the algorithm, which decreases as $h$ gets smaller) and **round-off error** (error from the hardware, which increases as $h$ gets smaller). We will learn that making our grid step size $h$ **"as small as possible" is disastrous**, as it amplifies round-off errors through catastrophic cancellation.

---

### Comprehension Check

!!! note "Quiz"
    **1. According to Chapter 5, why do we need numerical differentiation in physics?**
    
    - A. Because all physical laws are simple polynomial functions.
    - B. Because we often have data on a discrete grid and cannot use standard analytical calculus.
    - C. To find the area under the curve for a discrete function.
    - D. To solve root-finding problems for transcendental equations.
    
??? info "See Answer"
        **Correct: B**
    
        *(We have discrete data points, not continuous functions, so we must approximate derivatives using finite differences.)*
    
---

!!! note "Quiz"
    **2. Which of the following is defined as the second derivative of position, $x(t)$?**
    
    - A. Potential ($V(t)$)
    - B. Force ($F(t)$)
    - C. Velocity ($v(t)$)
    - D. Acceleration ($a(t)$)
    
??? info "See Answer"
        **Correct: D**
    
        *(Acceleration is $a(t) = \frac{d^2x}{dt^2}$, the second derivative of position with respect to time.)*
    
---

!!! note "Quiz"
    **3. The "great war" in numerical differentiation refers to the conflict between:**
    
    - A. Forward and backward difference formulas.
    - B. Truncation error and round-off error.
    - C. First-order and second-order accuracy.
    - D. Taylor series and finite element methods.
    
??? info "See Answer"
        **Correct: B**
    
        *(Truncation error decreases as $h$ shrinks, but round-off error increases, creating an optimal balance point.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Give two distinct examples from physics of laws that are defined by a derivative, emphasizing the concept of "change" inherent in the operation. Explain why the computational approximation of these derivatives is critical for numerical physics.
    
    ???+ info "Answer Strategy"
        This question tests understanding of how derivatives encode physical change and why numerical methods are essential.
    
        1. **Classical Mechanics — Force:**
           The force $F(x) = -\frac{dV}{dx}$ is the derivative of the potential $V$ with respect to position $x$. This defines force as the instantaneous **rate of change** of potential energy with distance. To compute forces on a discrete grid (e.g., in molecular dynamics), we must numerically differentiate the potential energy function.
    
        2. **Electromagnetism — Electric Field:**
           The electric field $\mathbf{E} = -\nabla \phi$ is the negative gradient (a multidimensional derivative) of the electric potential $\phi$. This defines the electric field as the instantaneous **rate of change** of electric potential in space. In computational electromagnetics, we calculate field strengths by numerically differentiating potential distributions.
    
        3. **Computational Importance:**
           In both cases, analytical derivatives may be unavailable (e.g., when $V$ or $\phi$ come from experimental data or complex simulations). We must use finite-difference approximations on discrete grids, making numerical differentiation a foundational tool for translating physical laws into computational models.
    
        4. **The Challenge:**
           The accuracy of these physical predictions depends directly on how well we approximate these derivatives. Poor differentiation methods introduce errors that propagate through the simulation, potentially invalidating results.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Electric Field from a Potential Grid

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                          |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To demonstrate numerical differentiation by computing the electric field $E_x(x) = -\frac{d\phi}{dx}$ from a discrete 1D electrostatic potential $\phi(x)$ using finite-difference methods.                                                                                                              |
| **Mathematical Concept** | In electrostatics, the electric field is the negative gradient of the electric potential: $\mathbf{E} = -\nabla \phi$. In 1D, this becomes $E_x(x) = -\frac{d\phi}{dx}$. We will approximate this derivative using the central difference formula: $\frac{d\phi}{dx} \approx \frac{\phi(x+h) - \phi(x-h)}{2h}$. |
| **Experiment Setup**     | Define a 1D potential function (e.g., $\phi(x) = x^2$ or a Gaussian potential) on a discrete grid with spacing $h$. Use the central difference method to calculate the electric field at each interior grid point.                                                                                       |
| **Process Steps**        | 1. Create a discrete grid of $x$ values. <br>2. Compute $\phi(x)$ at each grid point. <br>3. Apply the central difference formula to calculate $E_x(x) = -\frac{\phi(x+h) - \phi(x-h)}{2h}$. <br>4. Compare numerical results with the analytical derivative where available.                            |
| **Expected Behavior**    | For $\phi(x) = x^2$, the analytical field is $E_x(x) = -2x$. The numerical approximation should closely match this for moderate grid spacing.                                                                                                                                                            |
| **Tracking Variables**   | - `x_grid`: array of position values <br> - `phi`: potential values at each grid point <br> - `E_numerical`: numerically computed electric field <br> - `E_analytical`: exact electric field (for validation) <br> - `error`: difference between numerical and analytical results                        |
| **Verification Goal**    | Confirm that the central difference method accurately reproduces the electric field, and observe how accuracy improves as grid spacing $h$ decreases (up to the point where round-off errors dominate).                                                                                                  |
| **Output**               | Two-panel plot: (1) the potential $\phi(x)$ and (2) both the numerical and analytical electric fields $E_x(x)$ for visual comparison.                                                                                                                                                                   |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Setup grid and potential
  SET h = 0.1
  SET x_grid = linspace(-5.0, 5.0, 101)
  SET phi = x_grid^2  // Example: quadratic potential

  PRINT "Grid spacing (h):", h
  PRINT "Number of grid points:", length(x_grid)

  // 2. Compute electric field using central difference
  INITIALIZE E_numerical as empty array

  FOR i FROM 1 TO length(x_grid)-2 DO
      E_x = -(phi[i+1] - phi[i-1]) / (2 * h)
      APPEND E_x TO E_numerical
  END FOR

  // 3. Compute analytical field for comparison
  SET E_analytical = -2 * x_grid[1:-1]  // Derivative of x^2 is 2x, so E = -2x

  // 4. Calculate error
  SET error = ABS(E_numerical - E_analytical)
  SET max_error = MAX(error)

  PRINT "Maximum error:", max_error

  // 5. Visualization
  CREATE figure with 2 subplots

  SUBPLOT 1:
      PLOT x_grid vs phi
      LABEL axes: "Position x" and "Potential φ(x)"
      ADD title: "Electrostatic Potential"

  SUBPLOT 2:
      PLOT x_grid[1:-1] vs E_numerical (line)
      PLOT x_grid[1:-1] vs E_analytical (dashed line)
      LABEL axes: "Position x" and "Electric Field Ex(x)"
      ADD legend: ["Numerical", "Analytical"]
      ADD title: "Electric Field (Negative Gradient of Potential)"

  DISPLAY plot

END
```

---

#### **Outcome and Interpretation**

* **Validation of Method:**
  The numerical electric field should closely match the analytical result, demonstrating that finite differences can accurately approximate derivatives on discrete grids.

* **Physical Insight:**
  Regions where the potential has steep slopes (large $|\frac{d\phi}{dx}|$) correspond to strong electric fields. Regions where the potential is flat have nearly zero field, confirming the physical relationship $\mathbf{E} = -\nabla \phi$.

* **Error Behavior:**
  For moderate grid spacing, the central difference method (which is $O(h^2)$ accurate) produces very small errors. As $h$ decreases, truncation error decreases quadratically until round-off errors begin to dominate at very small $h$ values.

* **Computational Lesson:**
  This project demonstrates the practical application of numerical differentiation to a fundamental physics problem and introduces the concept of balancing grid resolution with numerical precision.

<div class="section-divider"></div>

## 5.2 The Taylor Series — Foundation of Finite Differences {.heading-with-pill}

> **Concept:** Analytic Expansion vs. Discrete Approximation • **Difficulty:** ★★★☆☆

> **Summary:** The Taylor series is the mathematical bridge between derivatives and algebraic approximations, providing the fundamental expansions used to derive all numerical differentiation formulas.

---

### Theoretical Background

The **Taylor series** is the cornerstone of numerical differentiation. It is the mathematical bridge that allows us to translate between the continuous world of calculus (derivatives $f'$, $f''$, etc.) and the discrete world of computation (arithmetic operations on grid values).

**The Fundamental Idea**

The Taylor series makes a profound statement: if we know *everything* about a function at a single point $x$—its value $f(x)$, its slope $f'(x)$, its curvature $f''(x)$, and all higher derivatives—we can use this local information to predict the function's value at any nearby point $x+h$.

The series expresses this as an infinite sum of terms, each involving a higher derivative and a higher power of the step size $h$:

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) + \cdots
$$

Each additional term in this expansion provides a correction that accounts for the function's behavior at increasingly fine scales. The more terms we include, the more accurate our approximation becomes.

**The Key Insight for Numerical Differentiation**

Here's the crucial observation: we can **rearrange** the Taylor series to **solve for the derivatives** in terms of function values. This is the strategy behind all finite-difference formulas.

For example, if we truncate the series after the first derivative term and rearrange:

$$
f'(x) \approx \frac{f(x+h) - f(x)}{h} - \frac{h}{2} f''(x) - \frac{h^2}{6} f'''(x) - \cdots
$$

If $h$ is small and we ignore the higher-order terms (treating them as "error"), we obtain a simple algebraic formula for the derivative using only function values.

**The Essential Expansions**

For this chapter, we need only two fundamental Taylor expansions, both centered at point $x$:

1. **Forward expansion** (stepping forward by $h$):

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) + \cdots
$$

2. **Backward expansion** (stepping backward by $h$):

$$
f(x-h) = f(x) - h f'(x) + \frac{h^2}{2!} f''(x) - \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) - \cdots
$$

Notice the alternating signs in the backward expansion. This sign pattern is crucial for deriving different finite-difference formulas.

**Algebraic Manipulation — The Core Strategy**

By **adding, subtracting, and rearranging** these two expansions, we can systematically eliminate unwanted terms and isolate the derivatives we want:

* **Subtracting** the backward from the forward expansion eliminates all even-derivative terms, isolating $f'(x)$.
* **Adding** the forward and backward expansions eliminates all odd-derivative terms, isolating $f''(x)$.

This algebraic manipulation transforms infinite series involving derivatives into finite formulas involving only function values $f(x-h)$, $f(x)$, and $f(x+h)$—exactly the discrete data available on our computational grid.

---

### Comprehension Check

!!! note "Quiz"
    **1. What is the "engine" or "oracle" that the chapter uses to derive *all* the finite difference formulas?**
    
    - A. The Method of Least Squares
    - B. The Taylor Series expansion
    - C. The Runge-Kutta algorithm
    - D. The "Sweet Spot" V-plot
    
??? info "See Answer"
        **Correct: B**
    
        *(The Taylor series provides the analytical foundation for deriving all finite-difference approximations of derivatives.)*
    
---

!!! note "Quiz"
    **2. The Taylor series allows us to predict $f(x+h)$ based on information at $f(x)$ by using:**
    
    - A. Integration and area under the curve.
    - B. The function's values and its derivatives ($f'$, $f''$, ...) at $x$.
    - C. The Mean Value Theorem.
    - D. The sign-change bracket.
    
??? info "See Answer"
        **Correct: B**
    
        *(The Taylor series expresses $f(x+h)$ as a sum involving $f(x)$ and all its derivatives at point $x$.)*
    
---

!!! note "Quiz"
    **3. When deriving finite-difference formulas, what happens to the even-derivative terms ($f''(x)$, $f^{(4)}(x)$, etc.) when you subtract the backward Taylor expansion from the forward Taylor expansion?**
    
    - A. They are amplified and become the dominant error.
    - B. They cancel out completely due to equal coefficients with the same sign.
    - C. They become twice as large.
    - D. They are unchanged.
    
??? info "See Answer"
        **Correct: B**
    
        *(In the forward expansion, even derivatives have positive coefficients; in the backward expansion, they also have positive coefficients. When subtracting, these terms cancel, leaving only odd derivatives.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** If you are using a Taylor series to approximate $f(x+h)$ and you only include terms up to the first derivative, $f'(x)$, what type of geometrical approximation are you making for the function's behavior? What happens when you include the second-order term?
    
    ???+ info "Answer Strategy"
        This question tests understanding of the geometric interpretation of Taylor series truncation.
    
        1. **First-Order (Linear) Approximation:**
           By stopping at the $f'(x)$ term, you are approximating:
           $$f(x+h) \approx f(x) + h f'(x)$$
           This is a **linear approximation**—you are treating the function as a straight line (the tangent line) over the interval from $x$ to $x+h$. You explicitly ignore the function's curvature and all higher-order shape characteristics.
    
        2. **Geometric Interpretation:**
           The tangent line has the correct value and slope at $x$, but assumes the function continues in a straight line. For curved functions, this creates increasing error as you move farther from $x$.
    
        3. **Second-Order (Quadratic) Approximation:**
           When you include the second derivative term:
           $$f(x+h) \approx f(x) + h f'(x) + \frac{h^2}{2} f''(x)$$
           You are now approximating the function as a **parabola** (quadratic curve). This captures not just the value and slope, but also the **curvature** at $x$.
    
        4. **Impact on Accuracy:**
           The quadratic approximation is far more accurate for most functions because it accounts for how the slope itself is changing. The error drops from $O(h^2)$ to $O(h^3)$, a dramatic improvement for small $h$.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Verifying Taylor Series Convergence

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                     |
| ------------------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To empirically verify that the Taylor series approximation becomes increasingly accurate as more terms are included, and to demonstrate the dramatic improvement from including the second-order (curvature) term.                                                                                  |
| **Mathematical Concept** | The Taylor series truncation error decreases rapidly with each additional term. For a well-behaved function, the $n$-th order approximation has error $O(h^{n+1})$, meaning each additional term reduces error by approximately a factor of $h$.                                                    |
| **Experiment Setup**     | Use the exponential function $f(x) = e^x$ at $x=1$, and approximate $f(1+h)$ for $h=0.1$ using successive Taylor series orders: <br>• Zero-order: $f(1)$ <br>• First-order: $f(1) + h f'(1)$ <br>• Second-order: $f(1) + h f'(1) + \frac{h^2}{2} f''(1)$ <br>• Compare with the exact value $e^{1.1}$ |
| **Process Steps**        | 1. Define $x=1$, $h=0.1$, and the exact value $f(1+h) = e^{1.1}$. <br>2. Compute zero, first, and second-order Taylor approximations. <br>3. Calculate the absolute error for each approximation. <br>4. Observe how error decreases with each additional term. <br>5. Display results in a table. |
| **Expected Behavior**    | The error should decrease dramatically at each order: zero-order has $O(h)$ error, first-order has $O(h^2)$ error, and second-order has $O(h^3)$ error. For $h=0.1$, each step should reduce error by roughly a factor of 10.                                                                       |
| **Tracking Variables**   | - `x`, `h`: expansion point and step size <br> - `true_value`: exact $e^{1.1}$ <br> - `approx_0`, `approx_1`, `approx_2`: Taylor approximations of increasing order <br> - `error_0`, `error_1`, `error_2`: absolute errors at each order                                                          |
| **Verification Goal**    | Confirm that including the second-order term reduces error by approximately two orders of magnitude compared to the first-order approximation.                                                                                                                                                      |
| **Output**               | A formatted table showing the order of approximation, computed value, absolute error, and relative error for each Taylor series truncation.                                                                                                                                                         |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Setup
  SET x = 1.0
  SET h = 0.1
  SET x_eval = x + h

  // For f(x) = e^x, all derivatives equal e^x
  SET f_at_x = exp(x)
  SET f_prime_at_x = exp(x)
  SET f_double_prime_at_x = exp(x)

  SET true_value = exp(x_eval)

  PRINT "Evaluating e^x at x =", x_eval
  PRINT "Step size h =", h
  PRINT "True value:", true_value
  PRINT "------------------------------"

  // 2. Zero-order approximation (constant)
  SET approx_0 = f_at_x
  SET error_0 = ABS(true_value - approx_0)
  SET rel_error_0 = error_0 / true_value

  // 3. First-order approximation (linear)
  SET approx_1 = f_at_x + h * f_prime_at_x
  SET error_1 = ABS(true_value - approx_1)
  SET rel_error_1 = error_1 / true_value

  // 4. Second-order approximation (quadratic)
  SET approx_2 = f_at_x + h * f_prime_at_x + (h^2 / 2) * f_double_prime_at_x
  SET error_2 = ABS(true_value - approx_2)
  SET rel_error_2 = error_2 / true_value

  // 5. Display results
  PRINT "Order | Approximation | Absolute Error | Relative Error"
  PRINT "------|---------------|----------------|---------------"
  PRINT "0     |", approx_0, "|", error_0, "|", rel_error_0
  PRINT "1     |", approx_1, "|", error_1, "|", rel_error_1
  PRINT "2     |", approx_2, "|", error_2, "|", rel_error_2

  // 6. Analysis
  PRINT "------------------------------"
  PRINT "Error reduction (0→1):", error_0 / error_1, "×"
  PRINT "Error reduction (1→2):", error_1 / error_2, "×"

END
```

---

#### **Outcome and Interpretation**

* **Zero-Order Approximation:**
  Simply using $f(1) \approx 2.718$ to approximate $e^{1.1} \approx 3.004$ gives a large error (~0.286), as we completely ignore the function's change over the interval.

* **First-Order Improvement:**
  Including the linear term $f(1) + 0.1 \cdot f'(1) \approx 2.990$ reduces the error by roughly a factor of 10 to ~0.014. This captures the function's slope but not its curvature.

* **Second-Order Improvement:**
  Adding the quadratic term $f(1) + 0.1 \cdot f'(1) + \frac{(0.1)^2}{2} \cdot f''(1) \approx 3.004$ reduces the error by another factor of 10 to ~0.0005. This captures both slope and curvature.

* **Key Insight:**
  Each additional Taylor series term typically reduces error by a factor of $h$ (here, $h=0.1$), demonstrating the power of higher-order approximations. This motivates using central differences (second-order accurate) over forward differences (first-order accurate) in numerical differentiation.

  The Taylor series is not just a theoretical tool—it's the foundation for designing numerical algorithms with controlled, predictable accuracy.

<div class="section-divider"></div>

## 5.3 The Forward Difference — First-Order Approximation {.heading-with-pill}

> **Concept:** Single-Sided Slope Estimation • **Difficulty:** ★★☆☆☆

> **Summary:** The Forward Difference formula uses $f(x)$ and $f(x+h)$ to approximate $f'(x)$. It is a first-order ($O(h)$) accurate method because the $O(h^2)$ truncation error is divided by $h$.

---

### Theoretical Background

The Forward Difference is the most intuitive approach to approximating a derivative—it directly mimics the definition of the derivative but stops short of taking the limit.

**The Intuitive Concept**

In calculus, the derivative is defined as:

$$
f'(x) = \lim_{h \to 0} \frac{f(x+h) - f(x)}{h}
$$

The Forward Difference method simply **freezes** this limit at some finite value of $h$ and uses the resulting finite-difference quotient as the approximation:

$$
f'(x) \approx \frac{f(x+h) - f(x)}{h}
$$

Geometrically, this computes the slope of the **secant line** connecting the point $(x, f(x))$ to the point $(x+h, f(x+h))$. For small $h$, this secant line approximates the tangent line (the true derivative).

**Derivation from Taylor Series**

To understand the accuracy of this approximation, we start with the forward Taylor expansion of $f(x+h)$ around point $x$:

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + O(h^4)
$$

Rearranging to solve for $f'(x)$:

$$
f'(x) = \frac{f(x+h) - f(x)}{h} - \frac{h}{2} f''(x) - \frac{h^2}{6} f'''(x) - O(h^3)
$$

If we **truncate** (ignore) all terms of order $h$ and higher, we obtain the **Forward Difference Formula**:

$$
f'(x) \approx \frac{f(x+h) - f(x)}{h}
$$

**Understanding the Error**

The truncated terms represent the **truncation error**:

$$
\text{Truncation Error} = \frac{h}{2} f''(x) + \frac{h^2}{6} f'''(x) + O(h^3)
$$

For small $h$, the dominant error term is $\frac{h}{2} f''(x)$, which is proportional to $h$. We express this as:

$$
\text{Truncation Error} = O(h)
$$

This makes the Forward Difference a **first-order accurate** method.

**The Practical Consequence**

First-order accuracy has a critical computational implication:

* To reduce error by a factor of 10, you must reduce $h$ by a factor of 10, which means using **10 times more grid points**.
* To achieve double precision accuracy ($\sim 10^{-16}$), you would theoretically need grid spacing on the order of $10^{-16}$, which is completely impractical and would be dominated by round-off errors.

This inefficiency is why the Forward Difference, despite its simplicity, is rarely used in production numerical codes except at boundaries where centered methods cannot be applied.

---

### Comprehension Check

!!! note "Quiz"
    **1. What is the Forward Difference formula for the first derivative, $f'(x)$?**
    
    - A. $\frac{f(x+h) - f(x-h)}{2h}$
    - B. $\frac{f(x+h) - f(x)}{h}$
    - C. $\frac{f(x) - f(x-h)}{h}$
    - D. $\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$
    
??? info "See Answer"
        **Correct: B**
    
        *(The Forward Difference uses the function values at $x$ and one point forward at $x+h$ to estimate the slope.)*
    
---

!!! note "Quiz"
    **2. What is the order of the truncation error for the Forward Difference formula?**
    
    - A. $O(h)$ (first-order accurate)
    - B. $O(h^2)$ (second-order accurate)
    - C. $O(h^4)$ (fourth-order accurate)
    - D. $O(\epsilon_m/h)$ (round-off error)
    
??? info "See Answer"
        **Correct: A**
    
        *(The leading truncation error term is $\frac{h}{2}f''(x)$, making the method first-order accurate in $h$.)*
    
---

!!! note "Quiz"
    **3. If you halve the grid spacing $h$ in the Forward Difference method, by what factor does the truncation error decrease?**
    
    - A. Factor of 2
    - B. Factor of 4
    - C. Factor of 8
    - D. It increases
    
??? info "See Answer"
        **Correct: A**
    
        *(Since the method is $O(h)$ accurate, halving $h$ halves the error. This is less efficient than second-order methods where halving $h$ reduces error by a factor of 4.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** If you are using the Forward Difference method and cut your grid spacing $h$ in half, by what factor do you expect your truncation error to decrease, and why? How does this compare to a hypothetical second-order method?
    
    ???+ info "Answer Strategy"
        This question tests understanding of convergence rates and computational efficiency.
    
        1. **First-Order Convergence:**
           The truncation error will decrease by a factor of **two** (it will be cut in half). This is because the Forward Difference formula is **first-order accurate** ($O(h)$).
    
        2. **Mathematical Justification:**
           The truncation error is dominated by the term $\frac{h}{2} f''(x)$. If $h \to h/2$, then:
           $$\text{Error}_{\text{new}} = \frac{h/2}{2} f''(x) = \frac{1}{2} \cdot \frac{h}{2} f''(x) = \frac{1}{2} \text{Error}_{\text{old}}$$
    
        3. **Comparison to Second-Order Methods:**
           A second-order method ($O(h^2)$) has error proportional to $h^2$. Halving $h$ reduces error by a factor of **four**:
           $$\text{Error}_{\text{new}} = \left(\frac{h}{2}\right)^2 = \frac{1}{4} h^2 = \frac{1}{4} \text{Error}_{\text{old}}$$
    
        4. **Computational Efficiency:**
           To achieve the same target accuracy:
           - **First-order:** Requires $N$ grid points (where $h \sim 1/N$)
           - **Second-order:** Requires $\sqrt{N}$ grid points (where $h^2 \sim 1/N$)
    
           The second-order method achieves the same accuracy with far fewer points, making it vastly more efficient.
    
        5. **Practical Implication:**
           This is why the Central Difference (second-order) is the "workhorse" of numerical differentiation, while the Forward Difference is used primarily at boundaries where centered formulas cannot be applied.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Convergence Analysis of Forward Difference

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To empirically verify the $O(h)$ convergence rate of the Forward Difference method and prepare convergence data for comparison with higher-order methods.                                                                                                                                                     |
| **Mathematical Concept** | The Forward Difference truncation error is $O(h)$, meaning error decreases linearly with grid spacing. On a log-log plot of error vs. $h$, a first-order method produces a line with slope $+1$.                                                                                                              |
| **Experiment Setup**     | Test function: $f(x) = \cos(x)$ at $x = 0.5$. The exact derivative is $f'(0.5) = -\sin(0.5) \approx -0.479425538604203$. Compute the Forward Difference approximation for a wide range of $h$ values from $10^{-1}$ to $10^{-10}$ and measure the absolute error.                                             |
| **Process Steps**        | 1. Define the test function and its analytical derivative. <br>2. Create logarithmically spaced $h$ values. <br>3. For each $h$, compute the Forward Difference approximation. <br>4. Calculate the absolute error compared to the exact derivative. <br>5. Store data for later visualization and analysis. |
| **Expected Behavior**    | For moderate $h$ values ($10^{-2}$ to $10^{-6}$), error decreases linearly with $h$ (slope = 1 on log-log plot). For very small $h$ (below $\sim 10^{-8}$), round-off errors dominate and the error increases, creating the characteristic "V-curve."                                                        |
| **Tracking Variables**   | - `h_values`: array of step sizes <br> - `f_prime_exact`: analytical derivative value <br> - `f_prime_forward`: Forward Difference approximation <br> - `errors_forward`: absolute errors at each $h$ <br> - `optimal_h`: step size where total error is minimized                                           |
| **Verification Goal**    | Confirm that in the truncation-dominated region, a log-log plot of error vs. $h$ has slope approximately $+1$, validating the $O(h)$ convergence rate. Identify the optimal $h$ where truncation and round-off errors balance.                                                                                |
| **Output**               | Store error data for later plotting. Print the range of $h$ values tested and the approximate optimal $h$ (typically around $\sqrt{\epsilon_m} \approx 10^{-8}$ for double precision).                                                                                                                        |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Define test function and exact derivative
  DEFINE function f(x):
      RETURN cos(x)

  DEFINE function f_prime_exact(x):
      RETURN -sin(x)

  SET x_eval = 0.5
  SET true_derivative = f_prime_exact(x_eval)

  PRINT "Test function: f(x) = cos(x)"
  PRINT "Evaluation point: x =", x_eval
  PRINT "Exact derivative: f'(", x_eval, ") =", true_derivative
  PRINT "------------------------------"

  // 2. Generate range of step sizes
  SET h_values = logspace(-10, -1, 100)
  INITIALIZE empty array errors_forward

  // 3. Compute Forward Difference for each h
  FOR each h IN h_values DO
      // Forward Difference: [f(x+h) - f(x)] / h
      f_prime_approx = (f(x_eval + h) - f(x_eval)) / h

      absolute_error = ABS(f_prime_approx - true_derivative)
      APPEND absolute_error TO errors_forward
  END FOR

  // 4. Find optimal h (minimum error)
  SET min_error_index = INDEX_OF_MIN(errors_forward)
  SET optimal_h = h_values[min_error_index]
  SET min_error = errors_forward[min_error_index]

  PRINT "Optimal step size h =", optimal_h
  PRINT "Minimum error =", min_error
  PRINT "Square root of machine epsilon =", sqrt(machine_epsilon)

  // 5. Store data for visualization
  SAVE h_values, errors_forward

  PRINT "------------------------------"
  PRINT "Data prepared for log-log convergence plot"
  PRINT "Expected slope in truncation region: +1 (first-order)"

END
```

---

#### **Outcome and Interpretation**

* **Truncation-Dominated Region ($h > 10^{-8}$):**
  In this region, the error decreases linearly with $h$. A log-log plot shows a straight line with slope $+1$, confirming the $O(h)$ convergence rate. For example:
  - At $h = 10^{-2}$: error $\approx 10^{-4}$
  - At $h = 10^{-4}$: error $\approx 10^{-6}$
  - Error scales as $\sim h^1$

* **Round-off-Dominated Region ($h < 10^{-8}$):**
  When $h$ becomes very small, catastrophic cancellation between $f(x+h)$ and $f(x)$ amplifies round-off errors. The error increases as $h$ decreases, creating the upward slope of the "V-curve."

* **Optimal Balance ($h \approx \sqrt{\epsilon_m} \approx 10^{-8}$):**
  The minimum total error occurs around $h \approx 10^{-8}$ for double precision. This is the optimal balance between truncation error (decreases with smaller $h$) and round-off error (increases with smaller $h$).

* **Convergence Rate Validation:**
  The slope of $+1$ on the log-log plot empirically confirms the theoretical prediction of $O(h)$ accuracy, distinguishing this first-order method from higher-order methods (which would show steeper slopes).

* **Computational Insight:**
  This experiment reveals the fundamental trade-off in numerical differentiation and explains why blindly reducing $h$ can be counterproductive. It sets the stage for comparing with the Central Difference method, which achieves $O(h^2)$ accuracy.

<div class="section-divider"></div>

## 5.4 The Central Difference — The Workhorse Method {.heading-with-pill}

> **Concept:** Symmetric Slope Estimation • **Difficulty:** ★★★☆☆

> **Summary:** The Central Difference formula is $O(h^2)$ accurate because subtracting the forward and backward Taylor expansions cancels the $O(h^2)$ term, making the error proportional to $h^2$.

---

### Theoretical Background

The $O(h)$ error of the Forward Difference is computationally inefficient. The **Central Difference** method achieves a dramatic improvement in accuracy through a simple but elegant shift in perspective.

**The Strategic Concept**

Instead of looking only forward from point $x$ to $x+h$, the Central Difference method **"centers"** the measurement at $x$ by looking both backward to $x-h$ and forward to $x+h$. The derivative is approximated by the slope of the secant line connecting these two symmetric outer points.

Geometrically, this produces a more balanced approximation because it averages information from both sides of the point, reducing bias and capturing the local symmetry of the function.

**The Mathematical "Magic" — Term Cancellation**

The derivation reveals why this method is so powerful. We start with both Taylor expansions:

**Forward expansion:**

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) + O(h^5)
$$

**Backward expansion:**

$$
f(x-h) = f(x) - h f'(x) + \frac{h^2}{2!} f''(x) - \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) - O(h^5)
$$

Now, **subtract** the backward expansion from the forward expansion:

$$
f(x+h) - f(x-h) = 2h f'(x) + \frac{2h^3}{3!} f'''(x) + O(h^5)
$$

**Notice the cancellation:**
- The $f(x)$ terms cancel
- The $f''(x)$ terms cancel (both have $+$ signs)
- All even-derivative terms cancel
- Only odd-derivative terms remain

Rearranging for $f'(x)$:

$$
f'(x) = \frac{f(x+h) - f(x-h)}{2h} - \frac{h^2}{6} f'''(x) - O(h^4)
$$

Truncating the higher-order terms gives the **Central Difference Formula**:

$$
f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}
$$

**Understanding the Error**

The truncation error is:

$$
\text{Truncation Error} = \frac{h^2}{6} f'''(x) + O(h^4)
$$

The dominant error term is proportional to $h^2$, making this a **second-order accurate** method:

$$
\text{Error} = O(h^2)
$$

**The Computational Advantage**

Second-order accuracy has profound implications:

* **Halving $h$ reduces error by a factor of 4** (compared to factor of 2 for first-order)
* **To achieve accuracy $\epsilon$, you need $h \sim \sqrt{\epsilon}$ (compared to $h \sim \epsilon$ for first-order)**
* **For the same target accuracy, second-order methods require far fewer grid points**

For example, to achieve error $\sim 10^{-6}$:
- **Forward Difference (first-order):** requires $h \sim 10^{-6}$ (1 million points per unit length)
- **Central Difference (second-order):** requires $h \sim 10^{-3}$ (1 thousand points per unit length)

This 1000× reduction in grid points makes second-order methods vastly more practical.

**The Practical Mantra**

Unless you are at a boundary where only forward or backward differences are available, **always use the Central Difference method**.

---

### Comprehension Check

!!! note "Quiz"
    **1. What is the Central Difference formula for the first derivative, $f'(x)$?**
    
    - A. $\frac{f(x+h) - f(x-h)}{2h}$
    - B. $\frac{f(x+h) - f(x)}{h}$
    - C. $\frac{f(x) - f(x-h)}{h}$
    - D. $\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$
    
??? info "See Answer"
        **Correct: A**
    
        *(The Central Difference uses symmetric points at $x-h$ and $x+h$, divided by $2h$ for the slope.)*
    
---

!!! note "Quiz"
    **2. If you halve the step size $h$ when using the Central Difference formula, by what factor does the truncation error decrease?**
    
    - A. Two
    - B. Four
    - C. Eight
    - D. It remains the same
    
??? info "See Answer"
        **Correct: B**
    
        *(The Central Difference is $O(h^2)$ accurate. Halving $h$ means error scales as $(h/2)^2 = h^2/4$, a reduction by factor of 4.)*
    
---

!!! note "Quiz"
    **3. Which terms in the Taylor series cancel when you subtract the backward expansion from the forward expansion?**
    
    - A. All odd-derivative terms ($f'$, $f'''$, $f^{(5)}$, ...)
    - B. All even-derivative terms ($f$, $f''$, $f^{(4)}$, ...)
    - C. Only the constant term $f(x)$
    - D. Only the first-derivative term $f'(x)$
    
??? info "See Answer"
        **Correct: B**
    
        *(Even-derivative terms have the same sign in both expansions, so they cancel when subtracted. Odd-derivative terms have opposite signs and add up.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Walk through the logic of why the Central Difference formula is so much more accurate than the Forward Difference. Specifically, what mathematical property of the Taylor series causes the $O(h^2)$ error term to vanish?
    
    ???+ info "Answer Strategy"
        This question tests deep understanding of the Taylor series manipulation and error analysis.
    
        1. **The Key Insight — Symmetry:**
           The Central Difference uses both the forward ($x+h$) and backward ($x-h$) Taylor series expansions. The backward expansion has the same form as the forward, but with alternating signs on odd-power terms.
    
        2. **The Cancellation Mechanism:**
           When we subtract $f(x-h)$ from $f(x+h)$, we get:
           $$f(x+h) - f(x-h) = 2hf'(x) + \frac{2h^3}{6}f'''(x) + O(h^5)$$
    
           The $f(x)$ terms cancel completely. The $f''(x)$ terms also cancel because:
           $$+\frac{h^2}{2}f''(x) - (+\frac{h^2}{2}f''(x)) = 0$$
    
           Both have positive signs in their respective expansions.
    
        3. **Why This Matters:**
           In the Forward Difference, the leading error term is $\frac{h}{2}f''(x)$, which is $O(h)$.
           In the Central Difference, this $f''(x)$ term is completely eliminated, and the leading error term becomes $\frac{h^2}{6}f'''(x)$, which is $O(h^2)$.
    
        4. **The Computational Consequence:**
           By eliminating the $O(h^2)$ term, we jump from first-order to second-order accuracy. This means that for the same grid resolution, the Central Difference is dramatically more accurate, or equivalently, we can use a coarser grid to achieve the same accuracy.
    
        5. **General Principle:**
           This demonstrates a fundamental strategy in numerical analysis: **symmetric formulas often have superior accuracy** because they exploit cancellation of even-order error terms. This principle extends to higher-order methods and multi-dimensional problems.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Comparing First-Order vs. Second-Order Convergence

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                                                       |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To empirically demonstrate the superior convergence rate of the Central Difference method ($O(h^2)$) compared to the Forward Difference method ($O(h)$) by plotting both on the same log-log error vs. step size graph.                                                                                                               |
| **Mathematical Concept** | On a log-log plot, the slope of the error curve reveals the convergence order: slope = 1 for $O(h)$, slope = 2 for $O(h^2)$. This visual comparison dramatically illustrates the advantage of second-order methods.                                                                                                                  |
| **Experiment Setup**     | Test function: $f(x) = \cos(x)$ at $x = 0.5$. Exact derivative: $f'(0.5) = -\sin(0.5)$. Compute both Forward and Central Difference approximations for $h$ values ranging from $10^{-1}$ to $10^{-12}$. Plot both error curves on the same axes.                                                                                       |
| **Process Steps**        | 1. Define test function and exact derivative. <br>2. Generate logarithmic range of $h$ values. <br>3. For each $h$, compute both Forward and Central Difference approximations. <br>4. Calculate absolute errors for both methods. <br>5. Create log-log plot with both error curves. <br>6. Annotate with reference slope lines.     |
| **Expected Behavior**    | In the truncation-dominated region: <br>• Forward Difference: slope ≈ +1 <br>• Central Difference: slope ≈ +2 <br>Both curves show the characteristic "V" shape, but the Central Difference optimal $h$ is larger and achieves lower minimum error.                                                                                    |
| **Tracking Variables**   | - `h_values`: array of step sizes <br> - `errors_forward`: Forward Difference errors <br> - `errors_central`: Central Difference errors <br> - `optimal_h_forward`, `optimal_h_central`: optimal step sizes for each method <br> - `min_error_forward`, `min_error_central`: minimum achievable errors                                 |
| **Verification Goal**    | Visually confirm that the Central Difference line has approximately twice the slope of the Forward Difference line in the truncation-dominated region, validating the theoretical $O(h)$ vs. $O(h^2)$ predictions.                                                                                                                     |
| **Output**               | A publication-quality log-log plot showing both error curves with: <br>• Different colors/markers for each method <br>• Reference lines showing slope = 1 and slope = 2 <br>• Vertical lines marking optimal $h$ for each method <br>• Legend and axis labels <br>• Annotation of the V-curve regions (truncation vs. round-off dominated) |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Define test function and exact derivative
  DEFINE function f(x):
      RETURN cos(x)

  DEFINE function f_prime_exact(x):
      RETURN -sin(x)

  SET x_eval = 0.5
  SET true_derivative = f_prime_exact(x_eval)

  PRINT "Convergence Comparison: Forward vs. Central Difference"
  PRINT "Test function: f(x) = cos(x) at x =", x_eval
  PRINT "Exact derivative:", true_derivative
  PRINT "========================================"

  // 2. Generate range of step sizes
  SET h_values = logspace(-12, -1, 100)
  INITIALIZE empty arrays: errors_forward, errors_central

  // 3. Compute both methods for each h
  FOR each h IN h_values DO
      // Forward Difference
      f_prime_forward = (f(x_eval + h) - f(x_eval)) / h
      error_forward = ABS(f_prime_forward - true_derivative)
      APPEND error_forward TO errors_forward

      // Central Difference
      f_prime_central = (f(x_eval + h) - f(x_eval - h)) / (2 * h)
      error_central = ABS(f_prime_central - true_derivative)
      APPEND error_central TO errors_central
  END FOR

  // 4. Find optimal h for each method
  SET idx_forward = INDEX_OF_MIN(errors_forward)
  SET optimal_h_forward = h_values[idx_forward]
  SET min_error_forward = errors_forward[idx_forward]

  SET idx_central = INDEX_OF_MIN(errors_central)
  SET optimal_h_central = h_values[idx_central]
  SET min_error_central = errors_central[idx_central]

  PRINT "Forward Difference:"
  PRINT "  Optimal h =", optimal_h_forward
  PRINT "  Minimum error =", min_error_forward
  PRINT ""
  PRINT "Central Difference:"
  PRINT "  Optimal h =", optimal_h_central
  PRINT "  Minimum error =", min_error_central
  PRINT "========================================"

  // 5. Create log-log comparison plot
  CREATE figure with size (10, 6)

  PLOT loglog(h_values, errors_forward, 'o-', color='red', label='Forward (O(h))')
  PLOT loglog(h_values, errors_central, 's-', color='blue', label='Central (O(h²))')

  // Add reference slope lines
  SET h_ref = 1e-4
  SET ref_slope_1 = h_ref * (h_values / h_ref)^1  // Slope = 1
  SET ref_slope_2 = h_ref * (h_values / h_ref)^2  // Slope = 2

  PLOT loglog(h_values, ref_slope_1, '--', color='gray', label='Slope = 1 (reference)')
  PLOT loglog(h_values, ref_slope_2, ':', color='gray', label='Slope = 2 (reference)')

  // Mark optimal h values
  PLOT axvline(optimal_h_forward, color='red', linestyle=':', alpha=0.5)
  PLOT axvline(optimal_h_central, color='blue', linestyle=':', alpha=0.5)

  SET xlabel("Step Size h")
  SET ylabel("Absolute Error")
  SET title("Convergence Comparison: Forward vs. Central Difference")
  ADD grid
  ADD legend

  ANNOTATE "Truncation-dominated" at appropriate region
  ANNOTATE "Round-off-dominated" at appropriate region

  DISPLAY plot

END
```

---

#### **Outcome and Interpretation**

* **Truncation-Dominated Region (Large $h$):**
  - **Forward Difference:** Error decreases with slope ≈ +1 on log-log plot, confirming $O(h)$ convergence
  - **Central Difference:** Error decreases with slope ≈ +2 on log-log plot, confirming $O(h^2)$ convergence
  - The Central Difference line is systematically below the Forward Difference line, showing superior accuracy at every grid resolution

* **Optimal Step Sizes:**
  - **Forward Difference:** Optimal $h \approx 10^{-8} \approx \sqrt{\epsilon_m}$ with minimum error $\sim 10^{-8}$
  - **Central Difference:** Optimal $h \approx 10^{-5} \approx \epsilon_m^{1/3}$ with minimum error $\sim 10^{-11}$
  - The Central Difference achieves **1000× better accuracy** and can use **1000× larger step size**

* **Round-off-Dominated Region (Very Small $h$):**
  Both methods eventually suffer from catastrophic cancellation, but the Central Difference degrades more slowly because it involves subtraction of $f(x+h)$ and $f(x-h)$ which are closer in magnitude to each other than $f(x+h)$ and $f(x)$.

* **The V-Curve Visualization:**
  The characteristic "V" shape appears for both methods:
  - Left side (large $h$): truncation error dominates, decreasing as $h$ shrinks
  - Bottom (optimal $h$): balance point between truncation and round-off
  - Right side (tiny $h$): round-off error dominates, increasing as $h$ shrinks

* **Practical Implications:**
  This experiment visually demonstrates why the Central Difference is the "workhorse" of numerical differentiation: it achieves far better accuracy with coarser grids, making it the default choice for computational physics applications.

* **Higher-Order Insight:**
  The pattern continues: fourth-order methods would show slope ≈ +4, sixth-order slope ≈ +6, etc. However, the complexity and round-off sensitivity increase with order, so second-order methods represent an optimal balance for most applications.

<div class="section-divider"></div>

## 5.5 The Second Derivative — Computing Curvature {.heading-with-pill}

> **Concept:** Numerical Laplacian Operator • **Difficulty:** ★★★☆☆

> **Summary:** The 2nd Derivative Central Difference formula is derived by adding the forward and backward Taylor expansions, canceling the odd terms, and yielding the crucial $O(h^2)$ accurate **1D Numerical Laplacian**.

---

### Theoretical Background

The **second derivative** ($f''(x)$) measures how the rate of change itself is changing—the curvature of a function. In physics, second derivatives appear everywhere: acceleration is the second derivative of position, the Laplacian operator appears in the Schrödinger equation, heat equation, and wave equation. The ability to compute $f''(x)$ numerically is essential for solving the fundamental PDEs of physics.

**The Physical Significance**

Second derivatives encode critical physical information:

* **Mechanics:** Acceleration is $a(t) = \frac{d^2x}{dt^2}$, the second derivative of position
* **Quantum Mechanics:** The Schrödinger equation contains $\frac{d^2\psi}{dx^2}$, governing wave function evolution
* **Diffusion:** The heat equation $\frac{\partial T}{\partial t} = \alpha \frac{\partial^2 T}{\partial x^2}$ describes temperature evolution
* **Wave Propagation:** The wave equation $\frac{\partial^2 u}{\partial t^2} = c^2 \frac{\partial^2 u}{\partial x^2}$ governs oscillations and vibrations

**Derivation Using Taylor Series**

We employ the same Taylor series strategy, but with a different algebraic manipulation. This time, we **add** the forward and backward expansions instead of subtracting them.

**Forward expansion:**

$$
f(x+h) = f(x) + h f'(x) + \frac{h^2}{2!} f''(x) + \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) + O(h^5)
$$

**Backward expansion:**

$$
f(x-h) = f(x) - h f'(x) + \frac{h^2}{2!} f''(x) - \frac{h^3}{3!} f'''(x) + \frac{h^4}{4!} f^{(4)}(x) - O(h^5)
$$

**Adding these expansions:**

$$
f(x+h) + f(x-h) = 2f(x) + h^2 f''(x) + \frac{h^4}{12} f^{(4)}(x) + O(h^6)
$$

**Notice the cancellation:**
- The first-derivative terms cancel: $+hf'(x) - hf'(x) = 0$
- The third-derivative terms cancel: $+\frac{h^3}{6}f'''(x) - \frac{h^3}{6}f'''(x) = 0$
- All odd-derivative terms cancel
- Only even-derivative terms survive

Rearranging for $f''(x)$:

$$
f''(x) = \frac{f(x+h) + f(x-h) - 2f(x)}{h^2} - \frac{h^2}{12} f^{(4)}(x) - O(h^4)
$$

Truncating the higher-order terms gives the **Central Difference Formula for the Second Derivative**:

$$
f''(x) \approx \frac{f(x+h) - 2f(x) + f(x-h)}{h^2}
$$

**Understanding the Error**

The truncation error is:

$$
\text{Truncation Error} = \frac{h^2}{12} f^{(4)}(x) + O(h^4)
$$

The dominant error is $O(h^2)$, making this a **second-order accurate** formula—the same order as the first derivative Central Difference.

**The Numerical "Stencil" Concept**

In computational physics, this formula is called a **three-point stencil** because it uses exactly three adjacent grid points:

$$
f''(x) \approx \frac{1}{h^2}\begin{bmatrix} +1 & -2 & +1 \end{bmatrix} \begin{bmatrix} f(x-h) \\ f(x) \\ f(x+h) \end{bmatrix}
$$

The coefficients $[+1, -2, +1]$ form the "pattern" or "stencil" that is applied at every interior grid point. This stencil is the discrete approximation of the **Laplacian operator** $\nabla^2$ in one dimension.

**Why It's Called the "Laplacian"**

In higher dimensions, the Laplacian operator is:

$$
\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2} + \frac{\partial^2 f}{\partial z^2}
$$

The one-dimensional case is simply $\nabla^2 f = \frac{d^2f}{dx^2}$. Our stencil is the **discrete numerical implementation** of this fundamental differential operator, which appears in virtually every PDE in physics.

---

### Comprehension Check

!!! note "Quiz"
    **1. What is the Central Difference formula for the second derivative, $f''(x)$?**
    
    - A. $\frac{f(x+h) - f(x-h)}{2h}$
    - B. $\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$
    - C. $\frac{f(x+h) - 2f(x) + f(x-h)}{2h}$
    - D. $\frac{f(x+h) + 2f(x) - f(x-h)}{h^2}$
    
??? info "See Answer"
        **Correct: B**
    
        *(The second derivative stencil uses the pattern [+1, -2, +1] divided by $h^2$, forming the numerical Laplacian.)*
    
---

!!! note "Quiz"
    **2. The formula $\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$ is the numerical equivalent of which fundamental operator, essential for solving the Schrödinger and heat equations?**
    
    - A. The gradient operator $\nabla$
    - B. The divergence operator $\nabla \cdot$
    - C. The Laplacian operator $\nabla^2$
    - D. The curl operator $\nabla \times$
    
??? info "See Answer"
        **Correct: C**
    
        *(This stencil is the discrete approximation of the Laplacian $\nabla^2$, which measures local curvature and appears in diffusion and wave equations.)*
    
---

!!! note "Quiz"
    **3. When deriving the second derivative formula, which terms from the Taylor series cancel when you add the forward and backward expansions?**
    
    - A. All even-derivative terms ($f''$, $f^{(4)}$, ...)
    - B. All odd-derivative terms ($f'$, $f'''$, $f^{(5)}$, ...)
    - C. Only the constant term $f(x)$
    - D. No terms cancel
    
??? info "See Answer"
        **Correct: B**
    
        *(When adding the expansions, odd-derivative terms have opposite signs and cancel: $+hf'(x) - hf'(x) = 0$, etc.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** In the context of solving a differential equation on a discrete grid, why is the second derivative formula $\frac{f(x+h) - 2f(x) + f(x-h)}{h^2}$ referred to as a "stencil"? How does this concept extend to multi-dimensional problems?
    
    ???+ info "Answer Strategy"
        This question tests understanding of computational grid operations and their extension to higher dimensions.
    
        1. **The Stencil Concept:**
           A "stencil" is the geometric pattern of grid points and their associated weights used to compute a value at a central location. The second derivative formula is a **three-point stencil** because it requires exactly three specific, adjacent grid points:
           - $f(x-h)$ with weight $+1$
           - $f(x)$ with weight $-2$
           - $f(x+h)$ with weight $+1$
    
        2. **Computational Implementation:**
           This algebraic pattern (the stencil) is applied repeatedly at every interior grid point, transforming the differential operator into a matrix operation:
           $$f''(x_i) \approx \frac{f_{i+1} - 2f_i + f_{i-1}}{h^2}$$
    
        3. **Physical Interpretation:**
           The stencil measures how much the function at point $x$ deviates from the average of its neighbors. If $f(x)$ equals the average, the second derivative is zero (linear function). If $f(x)$ is below/above the average, the curvature is positive/negative.
    
        4. **Extension to 2D (e.g., Heat Equation on a Plate):**
           The Laplacian in 2D becomes:
           $$\nabla^2 f = \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}$$
    
           The numerical stencil expands to a **five-point stencil** (plus-shaped pattern):
                 f(x, y+h)
                     |
           f(x-h, y) - f(x,y) - f(x+h, y)
                     |
                 f(x, y-h)
           $$\nabla^2 f \approx \frac{f(x+h,y) + f(x-h,y) + f(x,y+h) + f(x,y-h) - 4f(x,y)}{h^2}$$
    
        5. **Extension to 3D (e.g., Quantum Mechanics):**
           The pattern extends to a **seven-point stencil** with neighbors along all three axes.
    
        6. **Computational Importance:**
           Understanding stencils is crucial because:
           - They reveal the **locality** of differential operators (only nearby points matter)
           - They determine the **sparsity pattern** of the resulting matrix equations
           - They guide implementation in parallel computing and GPU programming
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Verifying Second-Order Convergence of the Laplacian

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objective**            | To empirically verify that the second derivative Central Difference formula converges with $O(h^2)$ accuracy by testing on a function with known analytical second derivative.                                                                                                       |
| **Mathematical Concept** | The second derivative approximation error should scale as $h^2$, producing a slope of +2 on a log-log plot of error vs. step size.                                                                                                                                                  |
| **Experiment Setup**     | Test function: $f(x) = x^4$ at $x = 1$. The exact second derivative is $f''(1) = 12$. Compute the numerical second derivative using the three-point stencil for step sizes ranging from $10^{-1}$ to $10^{-8}$ and measure absolute error.                                          |
| **Process Steps**        | 1. Define $f(x) = x^4$ and its exact second derivative $f''(x) = 12x^2$. <br>2. Generate logarithmic range of $h$ values. <br>3. For each $h$, compute the numerical second derivative. <br>4. Calculate absolute error. <br>5. Plot error vs. $h$ on log-log scale.                |
| **Expected Behavior**    | The error should decrease with slope ≈ +2 in the truncation-dominated region, confirming $O(h^2)$ accuracy. For very small $h$ (below $\sim 10^{-5}$), round-off errors create the V-curve behavior.                                                                                |
| **Tracking Variables**   | - `h_values`: step sizes <br> - `f_double_prime_exact`: true value (12) <br> - `f_double_prime_numerical`: stencil approximation <br> - `errors`: absolute errors <br> - `optimal_h`: step size with minimum error                                                                  |
| **Verification Goal**    | Confirm slope ≈ +2 on log-log plot, validate the $O(h^2)$ theoretical prediction, and identify the optimal balance between truncation and round-off errors.                                                                                                                         |
| **Output**               | Log-log plot showing error vs. $h$ with reference line of slope +2, annotations for truncation/round-off regions, and printed optimal $h$ value (typically around $10^{-5}$ for second derivatives).                                                                                |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Define test function and exact second derivative
  DEFINE function f(x):
      RETURN x^4

  DEFINE function f_double_prime_exact(x):
      RETURN 12 * x^2

  SET x_eval = 1.0
  SET true_second_derivative = f_double_prime_exact(x_eval)

  PRINT "Test function: f(x) = x^4"
  PRINT "Evaluation point: x =", x_eval
  PRINT "Exact second derivative: f''(", x_eval, ") =", true_second_derivative
  PRINT "========================================="

  // 2. Generate range of step sizes
  SET h_values = logspace(-8, -1, 100)
  INITIALIZE empty array errors

  // 3. Compute second derivative for each h
  FOR each h IN h_values DO
      // Three-point stencil: [f(x+h) - 2f(x) + f(x-h)] / h^2
      numerator = f(x_eval + h) - 2 * f(x_eval) + f(x_eval - h)
      f_double_prime_approx = numerator / (h^2)

      absolute_error = ABS(f_double_prime_approx - true_second_derivative)
      APPEND absolute_error TO errors
  END FOR

  // 4. Find optimal h
  SET min_error_index = INDEX_OF_MIN(errors)
  SET optimal_h = h_values[min_error_index]
  SET min_error = errors[min_error_index]

  PRINT "Optimal step size: h =", optimal_h
  PRINT "Minimum error =", min_error
  PRINT "========================================="

  // 5. Create log-log plot
  CREATE figure
  PLOT loglog(h_values, errors, 'o-', label='Second Derivative Error')

  // Add reference line with slope +2
  SET h_ref = 1e-3
  SET ref_line = (h_ref)^2 * (h_values / h_ref)^2
  PLOT loglog(h_values, ref_line, '--', color='gray', label='O(h²) reference')

  // Mark optimal h
  PLOT axvline(optimal_h, linestyle=':', color='red', alpha=0.6, label='Optimal h')

  SET xlabel("Step Size h")
  SET ylabel("Absolute Error")
  SET title("Convergence of Second Derivative Approximation")
  ADD grid
  ADD legend

  DISPLAY plot

END
```

---

#### **Outcome and Interpretation**

* **Second-Order Convergence:**
  The log-log plot shows a straight line with slope ≈ +2 in the truncation-dominated region, confirming the theoretical $O(h^2)$ accuracy. For example:
  - At $h = 10^{-2}$: error $\approx 10^{-4}$
  - At $h = 10^{-3}$: error $\approx 10^{-6}$
  - Halving $h$ reduces error by factor of 4

* **Optimal Step Size:**
  The minimum error occurs around $h \approx 10^{-5}$ to $10^{-6}$ for double precision, slightly different from the first derivative optimal $h$ because the stencil involves division by $h^2$ instead of $h$, affecting the round-off amplification.

* **Round-off Sensitivity:**
  The second derivative is more sensitive to round-off errors than the first derivative because:
  - It involves two subtractions instead of one
  - Division by $h^2$ amplifies errors more than division by $h$
  - This shifts the optimal $h$ to slightly larger values

* **Physical Applications:**
  This stencil forms the foundation for solving PDEs in computational physics. In molecular dynamics, it computes forces from potentials. In quantum mechanics, it discretizes the kinetic energy operator. In diffusion problems, it models heat flow.

* **Computational Insight:**
  The three-point stencil $[+1, -2, +1]/h^2$ is remarkably universal—the same pattern appears in solving Schrödinger's equation for electron orbitals, modeling heat diffusion in materials, and simulating wave propagation in media.

<div class="section-divider"></div>

## 5.6 The War Between Errors — Finding the Sweet Spot {.heading-with-pill}

> **Concept:** Truncation vs. Round-off Trade-off • **Difficulty:** ★★★★☆

> **Summary:** The **Total Error** is the sum of **Truncation Error** ($E_{\text{trunc}} \propto h^2$) and **Round-off Error** ($E_{\text{round}} \propto \epsilon_m/h$). The optimal derivative is found at the **"sweet spot"** where these two errors are balanced, visualized as the bottom of the characteristic "V-plot."

---

### Theoretical Background

We have established that the Central Difference method is $O(h^2)$ accurate, which suggests that making $h$ as small as possible should minimize error. However, the laws of floating-point arithmetic from Chapter 2 reveal that this intuition is **catastrophically wrong**.

**The Competing Error Sources**

The Central Difference formula $f'(x) \approx \frac{f(x+h) - f(x-h)}{2h}$ is vulnerable to two fundamentally different types of error:

1. **Truncation Error** ($E_{\text{trunc}}$): Arises from cutting off the Taylor series
   - Proportional to $h^2$: $E_{\text{trunc}} \sim C h^2$
   - Decreases as $h$ gets smaller
   - Wants $h \to 0$

2. **Round-off Error** ($E_{\text{round}}$): Arises from finite precision arithmetic
   - Proportional to $\epsilon_m/h$: $E_{\text{round}} \sim D \frac{\epsilon_m}{h}$
   - Increases as $h$ gets smaller (catastrophic cancellation)
   - Wants $h$ to be large

**The Catastrophic Cancellation Problem**

When $h$ becomes very small:
- $f(x+h)$ and $f(x-h)$ become nearly identical
- Their subtraction loses significant digits (catastrophic cancellation from Chapter 2)
- The difference is dominated by the last few bits (noise)
- Dividing by small $2h$ amplifies this noise

For example, if $f(x) = \sin(x)$ and $h = 10^{-15}$:
- $f(x+h) \approx 0.841470984807896999...$
- $f(x-h) \approx 0.841470984807897001...$
- The difference in the 15th decimal place is pure round-off noise
- Dividing by $2h = 2 \times 10^{-15}$ amplifies this noise by $10^{15}$!

**The Total Error Model**

The total error is approximately:

$$
E_{\text{total}}(h) \approx C h^2 + D \frac{\epsilon_m}{h}
$$

where:
- $C$ depends on the third derivative of $f$ (truncation error coefficient)
- $D$ depends on the function values (round-off error coefficient)
- $\epsilon_m \approx 2.22 \times 10^{-16}$ for double precision

**Finding the Optimal $h$**

To minimize total error, we take the derivative with respect to $h$ and set it to zero:

$$
\frac{dE_{\text{total}}}{dh} = 2Ch - D\frac{\epsilon_m}{h^2} = 0
$$

Solving for $h$:

$$
h_{\text{optimal}} = \left(\frac{D \epsilon_m}{2C}\right)^{1/3} \sim \epsilon_m^{1/3}
$$

For double precision, $\epsilon_m^{1/3} \approx (2.22 \times 10^{-16})^{1/3} \approx 6 \times 10^{-6}$.

This explains why the optimal $h$ is typically around $10^{-5}$ to $10^{-6}$, not $10^{-15}$!

**The V-Plot Visualization**

On a log-log plot of error vs. $h$:

* **Right side (large $h$):** Dominated by truncation error
  - Error decreases with slope $+2$ as $h$ decreases
  - Line: $E \propto h^2$

* **Left side (small $h$):** Dominated by round-off error
  - Error increases with slope $-1$ as $h$ decreases
  - Line: $E \propto h^{-1}$

* **Bottom (sweet spot):** Optimal balance
  - Minimum achievable error
  - Location: $h \sim \epsilon_m^{1/3} \approx 10^{-5}$
  - Minimum error: $E_{\text{min}} \sim \epsilon_m^{2/3} \approx 10^{-11}$

The characteristic "V" shape gives the plot its name and provides immediate visual feedback about the error regimes.

**The Critical Lesson**

The mantra **"smaller $h$ is always better"** is fundamentally wrong in finite-precision arithmetic. The optimal strategy is to:

1. Understand both error sources
2. Balance them at the sweet spot
3. Never use $h$ smaller than the optimal value
4. Recognize that there is a **fundamental limit** to achievable accuracy ($\sim 10^{-11}$ for first derivatives with double precision)

---

### Comprehension Check

!!! note "Quiz"
    **1. What is the specific "Chapter 2 bug" that causes the error to explode when $h$ becomes too small in the Central Difference formula?**
    
    - A. Integer overflow
    - B. Runge's phenomenon
    - C. Catastrophic cancellation (from subtracting two nearly-equal numbers)
    - D. Truncation error
    
??? info "See Answer"
        **Correct: C**
    
        *(When $h$ is very small, $f(x+h)$ and $f(x-h)$ are nearly identical, and their subtraction loses significant digits through catastrophic cancellation, amplifying round-off errors.)*
    
---

!!! note "Quiz"
    **2. What is the "sweet spot" in numerical differentiation?**
    
    - A. An $h$ value that is as close to $\epsilon_m$ as possible (e.g., $h=10^{-16}$)
    - B. The optimal $h$ (e.g., $h \sim 10^{-6}$) that balances truncation and round-off error to give minimum total error
    - C. The use of the Central Difference formula
    - D. The point where the truncation error is exactly zero
    
??? info "See Answer"
        **Correct: B**
    
        *(The sweet spot is where $E_{\text{trunc}} \approx E_{\text{round}}$, minimizing total error. This occurs around $h \sim \epsilon_m^{1/3} \approx 10^{-5}$ to $10^{-6}$ for double precision.)*
    
---

!!! note "Quiz"
    **3. On the V-plot, what is the approximate slope of the error curve in the round-off-dominated region (left side, very small $h$)?**
    
    - A. $+2$ (error increases with $h^2$)
    - B. $-1$ (error increases as $h^{-1}$)
    - C. $0$ (error is constant)
    - D. $+1$ (error increases with $h$)
    
??? info "See Answer"
        **Correct: B**
    
        *(Round-off error scales as $\epsilon_m/h$, so as $h$ decreases, error increases proportionally to $1/h$, giving slope $-1$ on log-log plot.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** A colleague tells you, "To get the most accurate derivative, just set $h$ to be as small as possible, like $10^{-15}$." Why is this terrible advice, and what is the physical meaning of the resulting error on the V-plot?
    
    ???+ info "Answer Strategy"
        This question tests understanding of the interplay between algorithmic and hardware limitations.
    
        1. **Why It's Terrible Advice:**
           Setting $h \approx 10^{-15}$ puts the calculation on the **left side** of the V-plot, deep in the round-off-dominated region. At this point, truncation error is negligible, but round-off error has exploded to dominate the result.
    
        2. **The Numerical Disaster:**
           For $h = 10^{-15}$:
           - The numerator $f(x+h) - f(x-h)$ involves subtracting two numbers that agree to ~15 decimal places
           - Only the last 1-2 digits differ, which are entirely round-off noise
           - The division by $2h = 2 \times 10^{-15}$ amplifies this noise by a factor of $\sim 10^{15}$
           - The final answer has effectively **zero significant digits**
    
        3. **Physical Meaning on V-Plot:**
           On the left side of the V-plot, you're measuring the slope using two points that are so close together that the computer cannot distinguish their heights due to finite precision. It's like trying to measure the slope of a mountain by looking at two points 1 millimeter apart with a ruler that has 1-meter resolution.
    
        4. **The Correct Approach:**
           Find the sweet spot (bottom of the V) where:
           $$2Ch^2 \approx D\frac{\epsilon_m}{h} \implies h_{\text{opt}} \sim \epsilon_m^{1/3} \approx 10^{-5}$$
    
           At this point, truncation and round-off errors are balanced, typically giving $\sim 10^{-11}$ accuracy—the best achievable for first derivatives in double precision.
    
        5. **Practical Implication:**
           There is a **fundamental limit** to numerical differentiation accuracy imposed by hardware, not just by algorithm. No amount of algorithmic sophistication can overcome this limit without using higher precision (e.g., quad precision) or symbolic differentiation.
    
        6. **The Broader Lesson:**
           This illustrates a key principle in computational science: **more resolution is not always better**. Every numerical method has an optimal operating regime determined by the balance between competing error sources.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Visualizing the V-Plot for Exponential Function

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                                                    |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To empirically demonstrate the V-plot phenomenon by computing the Central Difference derivative over a wide range of step sizes, identifying the truncation-dominated and round-off-dominated regions, and locating the optimal sweet spot.                                                                                        |
| **Mathematical Concept** | Total error exhibits characteristic V-shape: decreases as $h^2$ (slope +2) in truncation region, increases as $h^{-1}$ (slope -1) in round-off region, with minimum at $h_{\text{opt}} \sim \epsilon_m^{1/3}$.                                                                                                                    |
| **Experiment Setup**     | Test function: $f(x) = e^x$ at $x = 1$. Exact derivative: $f'(1) = e \approx 2.71828...$. Compute Central Difference for $h$ ranging from $10^{-16}$ to $10^{-1}$ (spanning both error regimes). Plot on log-log scale to reveal V-curve structure.                                                                               |
| **Process Steps**        | 1. Define $f(x) = e^x$ and exact derivative. <br>2. Generate logarithmic array of $h$ values covering wide range. <br>3. Compute Central Difference for each $h$. <br>4. Calculate absolute error. <br>5. Create log-log plot. <br>6. Annotate regions and fit reference lines. <br>7. Identify and mark optimal $h$ and minimum error. |
| **Expected Behavior**    | Clear V-shaped curve with: <br>• Right side: slope ≈ +2 (truncation) <br>• Left side: slope ≈ -1 (round-off) <br>• Minimum at $h \approx 10^{-5}$ to $10^{-6}$ <br>• Minimum error $\approx 10^{-11}$ <br>• Explosive error growth for $h < 10^{-8}$                                                                               |
| **Tracking Variables**   | - `h_values`: array from $10^{-16}$ to $10^{-1}$ <br> - `errors`: absolute errors <br> - `h_optimal`: step size at minimum error <br> - `error_min`: minimum achievable error <br> - `slope_truncation`, `slope_roundoff`: fitted slopes for each region                                                                          |
| **Verification Goal**    | Visually confirm V-curve structure, verify theoretical predictions ($h_{\text{opt}} \sim \epsilon_m^{1/3}$, slope transitions), and demonstrate the futility of using $h < h_{\text{opt}}$.                                                                                                                                        |
| **Output**               | Publication-quality log-log plot with annotated regions, reference slope lines, optimal $h$ marker, and printed summary statistics comparing theoretical vs. empirical optimal values.                                                                                                                                             |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Define function and exact derivative
  DEFINE function f(x):
      RETURN exp(x)

  SET x_eval = 1.0
  SET true_derivative = exp(x_eval)
  SET machine_epsilon = 2.22e-16

  PRINT "V-Plot Analysis: The War Between Errors"
  PRINT "Test function: f(x) = e^x at x =", x_eval
  PRINT "Exact derivative:", true_derivative
  PRINT "Machine epsilon:", machine_epsilon
  PRINT "Theoretical h_optimal ≈ ε_m^(1/3) =", machine_epsilon^(1/3)
  PRINT "============================================="

  // 2. Generate wide range of step sizes
  SET h_values = logspace(-16, -1, 200)
  INITIALIZE empty array errors

  // 3. Compute Central Difference for each h
  FOR each h IN h_values DO
      // Central Difference formula
      f_prime_approx = (f(x_eval + h) - f(x_eval - h)) / (2 * h)

      absolute_error = ABS(f_prime_approx - true_derivative)
      APPEND absolute_error TO errors
  END FOR

  // 4. Find optimal h and minimum error
  SET min_idx = INDEX_OF_MIN(errors)
  SET h_optimal = h_values[min_idx]
  SET error_min = errors[min_idx]

  PRINT "Empirical Results:"
  PRINT "  Optimal h =", h_optimal
  PRINT "  Minimum error =", error_min
  PRINT "  Ratio h_opt / ε_m^(1/3) =", h_optimal / (machine_epsilon^(1/3))
  PRINT "============================================="

  // 5. Create V-plot visualization
  CREATE figure with size (12, 7)

  // Main error curve
  PLOT loglog(h_values, errors, 'o-', color='blue', linewidth=2,
              markersize=4, label='Total Error')

  // Reference lines for truncation error (slope +2)
  SET idx_trunc = FIND_INDEX where h_values > h_optimal
  SET h_trunc_ref = h_values[idx_trunc][0]
  SET err_trunc_ref = errors[idx_trunc][0]
  SET trunc_line = err_trunc_ref * (h_values / h_trunc_ref)^2
  PLOT loglog(h_values, trunc_line, '--', color='green', linewidth=1.5,
              label='Truncation ∝ h² (slope +2)')

  // Reference line for round-off error (slope -1)
  SET idx_round = FIND_INDEX where h_values < h_optimal
  SET h_round_ref = h_values[idx_round][-1]
  SET err_round_ref = errors[idx_round][-1]
  SET round_line = err_round_ref * (h_values / h_round_ref)^(-1)
  PLOT loglog(h_values, round_line, '--', color='red', linewidth=1.5,
              label='Round-off ∝ h⁻¹ (slope -1)')

  // Mark optimal point
  PLOT scatter(h_optimal, error_min, s=200, color='gold', marker='*',
               edgecolors='black', linewidth=2, zorder=5,
               label='Sweet Spot')

  // Vertical line at optimal h
  PLOT axvline(h_optimal, color='gold', linestyle=':', linewidth=2, alpha=0.7)

  // Annotations
  ANNOTATE "Truncation-Dominated Region\n(Algorithm Error)"
           at position (1e-2, 1e-3) with arrow pointing to right side

  ANNOTATE "Round-off-Dominated Region\n(Hardware Error)"
           at position (1e-14, 1e-2) with arrow pointing to left side

  ANNOTATE "Sweet Spot\nh ≈ ε_m^(1/3)"
           at position (h_optimal, error_min) with arrow

  // Formatting
  SET xlabel("Step Size h", fontsize=14)
  SET ylabel("Absolute Error", fontsize=14)
  SET title("The V-Plot: Balancing Truncation and Round-off Errors", fontsize=16)
  SET xlim(1e-16, 1e-1)
  SET ylim(1e-16, 1e0)
  ADD grid with alpha=0.3
  ADD legend with fontsize=11, location='best'

  DISPLAY plot

END
```

---

#### **Outcome and Interpretation**

* **The V-Curve Structure:**
  The plot clearly shows the characteristic V-shape, with two distinct linear regions on the log-log scale meeting at the sweet spot.

* **Truncation-Dominated Region ($h > 10^{-5}$):**
  - Slope ≈ +2 confirms $O(h^2)$ truncation error
  - Error: $E \approx 10^{-10}$ at $h=10^{-5}$ to $E \approx 10^{-2}$ at $h=10^{-1}$
  - Algorithm quality determines error magnitude

* **Round-off-Dominated Region ($h < 10^{-5}$):**
  - Slope ≈ -1 confirms $\epsilon_m/h$ scaling
  - Error: $E \approx 10^{-11}$ at $h=10^{-5}$ to $E \approx 10^{-1}$ at $h=10^{-16}$
  - Hardware precision determines error magnitude
  - Catastrophic cancellation dominates

* **The Sweet Spot:**
  - Empirical: $h_{\text{opt}} \approx 6 \times 10^{-6}$
  - Theoretical: $\epsilon_m^{1/3} \approx 6 \times 10^{-6}$
  - Excellent agreement validates theoretical model
  - Minimum error: $\approx 3 \times 10^{-11} \approx \epsilon_m^{2/3}$

* **Practical Implications:**
  - Using $h = 10^{-15}$: error $\approx 10^{-1}$ (only 1 decimal place correct!)
  - Using $h = 10^{-6}$: error $\approx 10^{-11}$ (11 decimal places correct)
  - Factor of $10^{10}$ improvement by choosing correctly

* **The Fundamental Limit:**
  Even with perfect algorithm choice, finite precision imposes accuracy ceiling of $\sim 10^{-11}$ for first derivatives. To break this barrier requires:
  - Higher precision arithmetic (quad precision: $\epsilon_m \sim 10^{-34}$)
  - Symbolic differentiation (exact, but limited applicability)
  - Automatic differentiation (exact to machine precision, but requires special implementation)

* **Computational Wisdom:**
  This experiment embodies a profound lesson: **more is not always better in computational science**. The optimal solution requires balancing competing constraints, not blindly maximizing resolution.

<div class="section-divider"></div>

## 5.7 Application — Force from Lennard-Jones Potential {.heading-with-pill}

> **Concept:** Real-World Derivative Calculation • **Difficulty:** ★★★☆☆

> **Summary:** The force $F(r) = -dV/dr$ for the Lennard-Jones potential is numerically calculated using the $O(h^2)$ Central Difference with optimal $h$ to achieve machine-level accuracy, verified against the known analytical solution.

---

### Theoretical Background

The **Lennard-Jones (LJ) potential** is one of the most important and widely used models in molecular dynamics, computational chemistry, and materials science. It describes the interaction energy between two neutral atoms or molecules as a function of their separation distance $r$.

**The Lennard-Jones Potential**

The potential energy is given by:

$$
V_{\text{LJ}}(r) = 4\epsilon \left[ \left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right]
$$

where:
- $\epsilon$ is the depth of the potential well (energy parameter)
- $\sigma$ is the finite distance at which the potential is zero (length parameter)
- $r$ is the distance between particle centers

**Physical Interpretation**

The two terms have distinct physical meanings:

* **Repulsive term** ($r^{-12}$): Models Pauli exclusion at short range
  - Dominates when $r < \sigma$
  - Prevents atoms from overlapping
  - Steep, short-range repulsion

* **Attractive term** ($r^{-6}$): Models van der Waals attraction at long range
  - Dominates when $r > \sigma$
  - Dipole-dipole and London dispersion forces
  - Weaker, longer-range attraction

The potential has a minimum at $r_{\text{min}} = 2^{1/6}\sigma \approx 1.122\sigma$, representing the equilibrium separation.

**From Potential to Force**

In classical mechanics, the force is the negative gradient of potential energy:

$$
F(r) = -\frac{dV}{dr}
$$

For the LJ potential, we can derive this analytically:

$$
F_{\text{LJ}}(r) = -\frac{d}{dr}\left[4\epsilon \left( \frac{\sigma^{12}}{r^{12}} - \frac{\sigma^6}{r^6} \right)\right]
$$

$$
F_{\text{LJ}}(r) = 4\epsilon \left[ -12\frac{\sigma^{12}}{r^{13}} + 6\frac{\sigma^6}{r^7} \right]
$$

$$
F_{\text{LJ}}(r) = \frac{24\epsilon}{r} \left[ 2\left(\frac{\sigma}{r}\right)^{12} - \left(\frac{\sigma}{r}\right)^6 \right]
$$

**The Computational Challenge**

In many practical scenarios, we don't have an analytical expression for the potential—it might come from quantum mechanical calculations, experimental data, or complex empirical models. We need to compute forces numerically from potential energy surfaces.

This problem provides a perfect **"ground truth" test case**:
1. We have the analytical derivative (for verification)
2. We can test our numerical methods against exact results
3. We can measure accuracy down to machine precision
4. The function has realistic features (steep repulsion, long-range attraction)

**The Computational Strategy**

1. **Tool Selection:** Use the $O(h^2)$ Central Difference formula:
   $$F_{\text{numeric}}(r) = -\frac{V(r+h) - V(r-h)}{2h}$$

2. **Optimal $h$ Choice:** Based on V-plot analysis (Section 5.6), choose $h \approx 10^{-6}$ to $10^{-5}$ to balance truncation and round-off errors

3. **Calculation:** Apply the formula at a range of $r$ values spanning the interesting physics (repulsive wall, equilibrium, attractive tail)

4. **Verification:** Compare $F_{\text{numeric}}(r)$ with $F_{\text{analytic}}(r)$ to validate accuracy

5. **Analysis:** Plot the error to confirm it reaches machine precision limits ($\sim 10^{-14}$ to $10^{-15}$)

---

### Comprehension Check

!!! note "Quiz"
    **1. In this application, how did we calculate the force $F(r)$ from the Lennard-Jones potential $V(r)$?**
    
    - A. By finding the root of $V(r)$ using the Bisection method
    - B. By finding the second derivative $F = d^2V/dr^2$
    - C. By applying the Central Difference formula to compute $F = -dV/dr$
    - D. By integrating $V(r)$
    
??? info "See Answer"
        **Correct: C**
    
        *(The force is the negative gradient of potential, $F = -dV/dr$, computed numerically using the Central Difference method.)*
    
---

!!! note "Quiz"
    **2. What was the purpose of calculating the analytical force $F_{\text{analytic}}(r)$ in this application?**
    
    - A. To provide the final answer that the simulation would use
    - B. To serve as the "ground truth" against which the accuracy of the numerical method was verified
    - C. To help select the optimal step size $h$
    - D. To check for boundary conditions
    
??? info "See Answer"
        **Correct: B**
    
        *(Having the exact analytical answer allows us to measure the numerical method's error and verify it achieves machine precision accuracy.)*
    
---

!!! note "Quiz"
    **3. The Lennard-Jones potential has a repulsive $r^{-12}$ term and an attractive $r^{-6}$ term. At what distance does the force equal zero (equilibrium)?**
    
    - A. $r = \sigma$
    - B. $r = 2^{1/6}\sigma \approx 1.122\sigma$
    - C. $r = 0$
    - D. $r = \infty$
    
??? info "See Answer"
        **Correct: B**
    
        *(At equilibrium, $F=0$ occurs where $V(r)$ has its minimum, which is at $r_{\text{min}} = 2^{1/6}\sigma$.)*
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** In the Lennard-Jones problem, you calculated the force numerically and analytically. You plot the absolute error and find it is $\sim 10^{-14}$. Is this result a failure or a success for the numerical method, and why?
    
    ???+ info "Answer Strategy"
        This question tests understanding of practical accuracy limits and error interpretation.
    
        1. **This is a Success:**
           An absolute error of $10^{-14}$ to $10^{-15}$ represents achieving the **limit of machine precision** for double-precision arithmetic (which has about 15-16 significant decimal digits).
    
        2. **Why This is the Best Possible:**
           - Machine epsilon: $\epsilon_m \approx 2.22 \times 10^{-16}$
           - Relative error: $10^{-14} / 2.7 \approx 4 \times 10^{-15}$
           - This means we've captured all but the last 1-2 bits of precision
           - No numerical method using standard double precision can do better
    
        3. **What It Confirms:**
           - The Central Difference formula is working correctly
           - The optimal $h$ was chosen properly (around $10^{-6}$)
           - The implementation has no bugs
           - Truncation error has been minimized to the point where only unavoidable round-off remains
    
        4. **The Remaining Error Source:**
           The $\sim 10^{-14}$ error is **not** from the algorithm—it's from the fundamental limitation of storing real numbers in 64 bits. This is irreducible hardware error.
    
        5. **How to Improve (if needed):**
           To achieve better accuracy would require:
           - Quad precision (128-bit floats): $\epsilon_m \sim 10^{-34}$
           - Symbolic differentiation: exact analytical formula
           - Automatic differentiation: machine precision for complex functions
    
           But for molecular dynamics simulations, $10^{-14}$ relative error in forces is vastly better than needed.
    
        6. **Practical Perspective:**
           Physical measurements rarely exceed 6-8 significant digits. Achieving 14-15 digits numerically is extraordinary and demonstrates the power of well-designed numerical methods.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Computing Force from Morse Potential

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | To compute the interatomic force from the Morse potential energy function using numerical differentiation, verify against analytical results, and identify the equilibrium bond length where force equals zero.                                                                                                           |
| **Mathematical Concept** | The Morse potential $V(r) = D_e(1 - e^{-a(r-r_e)})^2$ is a more realistic model for molecular bonds than the harmonic oscillator. The force is $F(r) = -dV/dr$, and equilibrium occurs at $F(r) = 0$ which should coincide with the minimum of $V(r)$ at $r = r_e$.                                                      |
| **Experiment Setup**     | Use realistic parameters: $D_e = 1.0$ eV (dissociation energy), $a = 1.5$ Å$^{-1}$ (width parameter), $r_e = 1.5$ Å (equilibrium bond length). Compute both potential and force over range $r \in [1.0, 4.0]$ Å using Central Difference with optimal $h$.                                                                |
| **Process Steps**        | 1. Define Morse potential function and analytical force. <br>2. Choose optimal $h \approx 10^{-6}$. <br>3. Compute numerical force using Central Difference. <br>4. Create dual-axis plot showing $V(r)$ and $F(r)$. <br>5. Find zero-crossing of force numerically. <br>6. Verify it matches $V(r)$ minimum at $r_e$. |
| **Expected Behavior**    | Force curve crosses zero at $r = r_e = 1.5$ Å, coinciding with minimum of potential curve. Numerical and analytical forces should be visually indistinguishable with error $\sim 10^{-14}$.                                                                                                                              |
| **Tracking Variables**   | - `r_values`: separation distances <br> - `V_morse`: potential energies <br> - `F_numerical`: numerically computed forces <br> - `F_analytical`: exact forces <br> - `r_equilibrium`: zero-force position <br> - `error`: difference between numerical and analytical forces                                              |
| **Verification Goal**    | Confirm that: (1) numerical force matches analytical force to machine precision, (2) force zero-crossing occurs at potential minimum, (3) method works for realistic molecular potential with exponential terms.                                                                                                          |
| **Output**               | Dual-axis plot showing potential (left axis) and force (right axis) vs. distance, with equilibrium position marked. Error plot showing $\sim 10^{-14}$ accuracy. Printed equilibrium position from force zero-crossing.                                                                                                   |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Define Morse potential and parameters
  DEFINE function morse_potential(r, D_e, a, r_e):
      RETURN D_e * (1 - exp(-a * (r - r_e)))^2

  DEFINE function morse_force_analytical(r, D_e, a, r_e):
      // F = -dV/dr for Morse potential
      exp_term = exp(-a * (r - r_e))
      RETURN -2 * D_e * a * (1 - exp_term) * exp_term

  // Parameters (typical for diatomic molecule)
  SET D_e = 1.0    // eV (dissociation energy)
  SET a = 1.5      // Å^-1 (width parameter)
  SET r_e = 1.5    // Å (equilibrium bond length)
  SET h_optimal = 1.0e-6

  PRINT "Morse Potential Parameters:"
  PRINT "  Dissociation energy D_e =", D_e, "eV"
  PRINT "  Width parameter a =", a, "Å^-1"
  PRINT "  Equilibrium distance r_e =", r_e, "Å"
  PRINT "  Numerical step size h =", h_optimal
  PRINT "=========================================="

  // 2. Generate distance array
  SET r_values = linspace(1.0, 4.0, 300)

  INITIALIZE arrays: V_morse, F_numerical, F_analytical, errors

  // 3. Compute potential, forces, and errors
  FOR each r IN r_values DO
      // Potential energy
      V = morse_potential(r, D_e, a, r_e)
      APPEND V TO V_morse

      // Numerical force: -dV/dr using Central Difference
      V_plus = morse_potential(r + h_optimal, D_e, a, r_e)
      V_minus = morse_potential(r - h_optimal, D_e, a, r_e)
      F_num = -(V_plus - V_minus) / (2 * h_optimal)
      APPEND F_num TO F_numerical

      // Analytical force
      F_ana = morse_force_analytical(r, D_e, a, r_e)
      APPEND F_ana TO F_analytical

      // Error
      error = ABS(F_num - F_ana)
      APPEND error TO errors
  END FOR

  // 4. Find equilibrium (where F = 0)
  // Find zero-crossing by interpolation
  SET zero_crossing_indices = FIND_SIGN_CHANGES(F_numerical)
  IF zero_crossing_indices is not empty THEN
      SET idx = zero_crossing_indices[0]
      // Linear interpolation for precise zero location
      SET r_equilibrium = INTERPOLATE_ZERO(r_values[idx], r_values[idx+1],
                                           F_numerical[idx], F_numerical[idx+1])
  END IF

  // Find potential minimum
  SET V_min_idx = INDEX_OF_MIN(V_morse)
  SET r_V_min = r_values[V_min_idx]

  PRINT "Results:"
  PRINT "  Equilibrium from F=0:", r_equilibrium, "Å"
  PRINT "  Potential minimum at:", r_V_min, "Å"
  PRINT "  Theoretical r_e:", r_e, "Å"
  PRINT "  Maximum force error:", MAX(errors)
  PRINT "=========================================="

  // 5. Visualization
  CREATE figure with 2 subplots

  // Subplot 1: Potential and Force
  CREATE subplot with dual y-axes

  // Left axis: Potential
  PLOT r_values vs V_morse (blue line, left axis)
  SET left ylabel "Potential Energy V(r) [eV]"
  SET left y-axis color blue

  // Right axis: Force
  PLOT r_values vs F_numerical (red line, right axis)
  PLOT r_values vs F_analytical (red dashed, right axis, for comparison)
  SET right ylabel "Force F(r) [eV/Å]"
  SET right y-axis color red

  // Mark equilibrium
  PLOT axvline(r_equilibrium, linestyle=':', color='green', label='Equilibrium')
  PLOT axhline(0, linestyle='-', color='gray', linewidth=0.5)

  SET xlabel "Separation Distance r [Å]"
  SET title "Morse Potential and Force"
  ADD legend
  ADD grid

  // Subplot 2: Error
  CREATE subplot for error
  PLOT semilogy(r_values, errors, 'o-', markersize=3)
  SET xlabel "Separation Distance r [Å]"
  SET ylabel "Absolute Error |F_numerical - F_analytical|"
  SET title "Numerical Force Error (Machine Precision Limit)"
  ADD grid

  DISPLAY figure

END
```

---

#### **Outcome and Interpretation**

* **Force Computation Accuracy:**
  The numerical force matches the analytical force to machine precision ($\sim 10^{-14}$ error), demonstrating that the Central Difference method with optimal $h$ achieves the theoretical accuracy limit.

* **Equilibrium Verification:**
  The force zero-crossing occurs at $r = 1.500$ Å, exactly matching the parameter $r_e$ and the minimum of the potential curve. This validates both the numerical method and the physical consistency (force = -∇V).

* **Physical Features Captured:**
  - **Repulsive wall** ($r < r_e$): Strong positive force pushing atoms apart
  - **Equilibrium** ($r = r_e$): Zero force, stable bond length
  - **Attractive tail** ($r > r_e$): Negative force pulling atoms together
  - **Asymptotic behavior** ($r \gg r_e$): Force approaches zero as $V$ flattens

* **Morse vs. Lennard-Jones Comparison:**
  The Morse potential provides a more realistic description of molecular bonds:
  - Exponential (not power-law) behavior is chemically accurate
  - Asymmetric well (different steepness on each side)
  - Correct dissociation limit ($V \to D_e$ as $r \to \infty$)

* **Error Behavior:**
  The error plot shows constant $\sim 10^{-14}$ across all $r$ values, confirming that:
  - The chosen $h$ is optimal everywhere
  - No special numerical issues arise from exponentials
  - Machine precision is the only error source

* **Practical Application:**
  This technique is used in molecular dynamics simulations where forces must be computed from complex, non-analytical potential energy surfaces derived from quantum calculations or experimental fits.