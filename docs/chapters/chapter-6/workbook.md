# **Chapter 6: Numerical Integration (Quadrature) (Workbook)**

---

## 6.1 The Physics of "Accumulation" {.heading-with-pill}

> **Concept:** Integration as Total Accumulation • **Difficulty:** ★★☆☆☆

> **Summary:** The integral, $I = \int f(x) dx$, is the language of **total accumulation** in physics. While differentiation reveals instantaneous change, integration computes global properties—work, probability, energy—by summing continuous distributions over a domain.

---

### Theoretical Background

In Chapter 5, we mastered the derivative ($\frac{d}{dx}$), the language of **instantaneous change**. Now, we tackle its inverse operation: the **integral** ($I = \int f(x) dx$), the language of **total accumulation**. This is how we "sum up" a quantity that is continuously changing across space or time.

#### The Physical Significance of Integration

Integration is the mathematical engine behind the **global properties** of physical systems:

* **Work:** The total work done by a force along a path is the accumulation of infinitesimal contributions:
  $$W = \int \mathbf{F} \cdot d\mathbf{x}$$

* **Probability:** In quantum mechanics, the wavefunction $\psi(x)$ must satisfy the normalization condition:
  $$\int_{-\infty}^{\infty} |\psi(x)|^2 dx = 1$$
  This ensures the total probability of finding the particle *somewhere* equals 1.

* **Statistical Mechanics:** The partition function, which encodes all thermodynamic information, is an integral over all energy states:
  $$Z = \int e^{-\beta E} \, dE$$
  where $\beta = 1/(k_B T)$.

* **Center of Mass:** For a continuous mass distribution $\rho(x)$, the center of mass is:
  $$\bar{x} = \frac{\int x \rho(x) dx}{\int \rho(x) dx}$$

#### The Computational Challenge

In pure mathematics, we can often evaluate integrals analytically using techniques from calculus (integration by parts, substitution, etc.). However, in computational physics, we face two fundamental obstacles:

1. **No Closed-Form Solution:** Many physically important functions (e.g., $e^{-x^2}$, $\sin(x)/x$) have no elementary antiderivative.

2. **Discrete Data:** Experimental measurements or numerical simulations produce **discrete data points** $(x_i, y_i)$ on a grid, not continuous functions. We cannot apply analytical calculus to a table of numbers.

#### The Strategy: Numerical Quadrature

The solution is **numerical quadrature** (from the Latin *quadratura*, meaning "to make square"). The core idea is elegant:

1. **Tile the Area:** Divide the region under the curve into simple geometric shapes (rectangles, trapezoids, parabolas) whose areas we can calculate exactly.

2. **Sum the Tiles:** Add up the areas of all tiles to approximate the total integral:
   $$I \approx \sum_{i=1}^{N} A_i$$
   where $A_i$ is the area of the $i$-th tile.

3. **Refine the Grid:** As we increase the number of tiles (decrease the spacing $h$), the approximation converges to the true value.

The quality of this approximation depends on:
- **The shape of the tile** (linear, quadratic, cubic interpolation)
- **The grid spacing** $h$ (finer grids reduce truncation error)
- **The smoothness of the function** (rough or singular functions are harder to integrate)

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What is the fundamental physical concept that integration computes?**
    
    - A. The rate of instantaneous change
    - B. The total accumulation of a quantity over a domain
    - C. The "sweet spot" between competing errors
    - D. The slope of a function on a discrete grid
    
??? info "See Answer"
        **Correct: B**
    
        Integration is the process of **accumulating** infinitesimal contributions across a continuous domain. While differentiation asks "how fast is this changing right now?", integration asks "how much total quantity has accumulated?". This is why work (accumulated force), probability (accumulated wavefunction density), and energy (accumulated contributions from all states) are all defined as integrals.
    
---

!!! note "Quiz"
    **2. The process of approximating integrals by summing areas of simple geometric shapes is called:**
    
    - A. Numerical differentiation
    - B. Root finding
    - C. Numerical quadrature
    - D. The Monte Carlo method
    
??? info "See Answer"
        **Correct: C**
    
        **Numerical quadrature** is the systematic approach of tiling the area under a curve with simple shapes (trapezoids, parabolas, etc.) and summing their areas. The term comes from the Latin *quadratura*, reflecting the geometric origin of the method.
    
---

!!! note "Quiz"
    **3. Why can't we always use analytical calculus techniques to evaluate integrals in computational physics?**
    
    - A. Computers cannot handle symbolic mathematics
    - B. Many functions have no closed-form antiderivative, and experimental data is discrete
    - C. Numerical methods are always more accurate
    - D. Integration is undefined for discrete data
    
??? info "See Answer"
        **Correct: B**
    
        Two fundamental barriers exist: (1) Many physically important functions (like the Gaussian $e^{-x^2}$ or the sinc function $\sin(x)/x$) have no elementary antiderivative expressible in terms of standard functions. (2) Experimental measurements and simulations produce **discrete data points**, not continuous functions, making analytical techniques inapplicable. This is why numerical quadrature is essential.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Chapter 5 was about $\frac{d}{dx}$ (change). Why is $\int dx$ (accumulation) arguably even more fundamental to the practice of physics?
    
    ???+ info "Answer Strategy"
        This question tests your understanding of the relationship between local and global descriptions in physics.
    
        1. **Local vs. Global:**
           The derivative describes **local, instantaneous** behavior—the velocity at this moment, the electric field at this point. The integral computes **global, cumulative** properties—the total distance traveled, the total energy stored in a field.
    
        2. **Observables are Global:**
           Most measurable quantities in physics are accumulated totals: the work done on an object, the total probability of detection, the center of mass of a system, the partition function that determines temperature and pressure. These are all integrals.
    
        3. **From Rules to Reality:**
           Differential equations (like Newton's laws, Maxwell's equations, Schrödinger's equation) give us the **rules** governing how systems evolve. But to extract **predictions**—trajectories, energies, probabilities—we must *integrate* these equations. Integration translates the microscopic physics into macroscopic observables.
    
        4. **The Hierarchy:**
           You could argue that physics *happens* at the differential level (forces cause accelerations), but physics is *measured* at the integral level (we observe cumulative effects). This makes integration the bridge from theory to experiment.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Center of Mass of a Non-Uniform Rod

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objective**            | Compute the center of mass $\bar{x}$ of a one-dimensional rod with non-uniform linear mass density $\lambda(x)$, demonstrating integration as the tool for calculating **global average properties** from continuous distributions.                                                                                      |
| **Mathematical Concept** | The center of mass is defined as the mass-weighted average position: <br> $$\bar{x} = \frac{\int_0^L x \cdot \lambda(x) dx}{\int_0^L \lambda(x) dx}$$ <br> The numerator accumulates position weighted by mass; the denominator is the total mass $M$.                                                                  |
| **Physical Setup**       | Consider a rod of length $L = 1.0$ m with a linearly varying mass density: <br> $$\lambda(x) = \lambda_0 (1 + \alpha x)$$ <br> where $\lambda_0 = 2.0$ kg/m is the density at $x=0$, and $\alpha = 3.0$ m$^{-1}$ controls the rate of increase. The rod is denser at the right end.                                     |
| **Experiment Setup**     | Evaluate both integrals numerically using a simple quadrature method (e.g., trapezoidal rule or `scipy.integrate.quad`). <br> - **Numerator:** $I_{\text{num}} = \int_0^L x \cdot \lambda(x) dx$ <br> - **Denominator:** $I_{\text{den}} = \int_0^L \lambda(x) dx$ <br> The center of mass is then $\bar{x} = I_{\text{num}} / I_{\text{den}}$. |
| **Process Steps**        | 1. Define the mass density function $\lambda(x)$. <br> 2. Define the two integrands: $f_{\text{num}}(x) = x \cdot \lambda(x)$ and $f_{\text{den}}(x) = \lambda(x)$. <br> 3. Integrate both functions from $0$ to $L$. <br> 4. Compute the center of mass $\bar{x}$.                                                     |
| **Expected Behavior**    | Because the rod is denser toward $x = L$, the center of mass should be **shifted to the right** of the geometric center ($L/2 = 0.5$ m). The exact value can be verified analytically by hand if desired.                                                                                                               |
| **Tracking Variables**   | - `lambda_0`: baseline density (kg/m) <br> - `alpha`: density gradient (m$^{-1}$) <br> - `L`: length of rod (m) <br> - `I_num`: numerator integral <br> - `I_den`: total mass <br> - `x_cm`: center of mass position                                                                                                    |
| **Verification Goal**    | Compare the numerical result to the analytical solution (if computed) or check physical intuition: $\bar{x} > L/2$ since mass is concentrated toward the right.                                                                                                                                                         |
| **Output**               | Print the total mass $M$, the center of mass $\bar{x}$, and verify that it lies to the right of the geometric midpoint.                                                                                                                                                                                                 |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Physical Parameters
  SET lambda_0 = 2.0    // kg/m (baseline density)
  SET alpha = 3.0       // m^(-1) (density gradient)
  SET L = 1.0           // m (rod length)

  // 2. Define Mass Density Function
  FUNCTION lambda(x):
      RETURN lambda_0 * (1 + alpha * x)
  END FUNCTION

  // 3. Define Integrands
  FUNCTION f_numerator(x):
      RETURN x * lambda(x)
  END FUNCTION

  FUNCTION f_denominator(x):
      RETURN lambda(x)
  END FUNCTION

  // 4. Numerical Integration (using library or manual method)
  // Using scipy.integrate.quad as the "professional" approach:

  I_num = INTEGRATE(f_numerator, from=0, to=L)
  I_den = INTEGRATE(f_denominator, from=0, to=L)

  // 5. Compute Center of Mass
  SET x_cm = I_num / I_den

  // 6. Output Results
  PRINT "===== Non-Uniform Rod: Center of Mass ====="
  PRINT "Rod length L:", L, "m"
  PRINT "Density function: λ(x) = λ₀(1 + αx)"
  PRINT "  λ₀ =", lambda_0, "kg/m"
  PRINT "  α =", alpha, "m⁻¹"
  PRINT "----------------------------------------------"
  PRINT "Total mass M =", I_den, "kg"
  PRINT "Center of mass x̄ =", x_cm, "m"
  PRINT "Geometric center L/2 =", L/2, "m"
  PRINT "----------------------------------------------"

  IF x_cm > L/2 THEN
      PRINT "✓ Center of mass is shifted RIGHT (denser at right end)"
  ELSE
      PRINT "✗ Unexpected: center of mass is at or left of geometric center"
  END IF

END
```

---

#### **Outcome and Interpretation**

* **Physical Insight:** The center of mass is **not** at the geometric center ($L/2$) because the rod has non-uniform density. Since $\lambda(x)$ increases with $x$ (the rod is denser toward the right), the center of mass shifts to the right.

* **Verification:** For the given parameters, the analytical solution is:
  $$\bar{x} = \frac{\int_0^L x \lambda_0(1 + \alpha x) dx}{\int_0^L \lambda_0(1 + \alpha x) dx}$$

  Evaluating by hand:
  - Numerator: $\lambda_0 \left[\frac{x^2}{2} + \alpha \frac{x^3}{3}\right]_0^L = \lambda_0 \left(\frac{L^2}{2} + \alpha \frac{L^3}{3}\right)$
  - Denominator: $\lambda_0 \left[x + \alpha \frac{x^2}{2}\right]_0^L = \lambda_0 \left(L + \alpha \frac{L^2}{2}\right)$
  - Result: $\bar{x} = \frac{L^2/2 + \alpha L^3/3}{L + \alpha L^2/2}$

  For $L=1$, $\alpha=3$: $\bar{x} = \frac{0.5 + 1.0}{1.0 + 1.5} = \frac{1.5}{2.5} = 0.6$ m

* **Numerical Accuracy:** The numerical integration should produce $\bar{x} \approx 0.6$ m, confirming that the rod's balance point is shifted 20% to the right of its geometric center.

* **Broader Lesson:** This project demonstrates that integration is the mathematical tool for computing **weighted averages**—a concept that appears throughout physics (expectation values in quantum mechanics, moments of inertia, electric dipole moments, etc.).

## 6.2 The "Simple" Tile: The Trapezoidal Rule {.heading-with-pill}

> **Concept:** Linear Interpolation for Quadrature • **Difficulty:** ★★☆☆☆

> **Summary:** The Trapezoidal Rule approximates the integral by tiling the area with trapezoids formed by linear interpolation between adjacent grid points. It achieves second-order accuracy ($O(h^2)$) and is robust, simple, and universally applicable to discrete data.

---

### Theoretical Background

The **Trapezoidal Rule** is the simplest and most intuitive numerical quadrature method. It answers the question: "How do we estimate the area under a curve when we only have discrete data points?"

#### The Geometric Intuition

Given two adjacent data points $(x_i, y_i)$ and $(x_{i+1}, y_{i+1})$, we draw a **straight line** connecting them. This line forms the "roof" of a trapezoid whose base rests on the $x$-axis. The area of this trapezoid is:

$$A_i = h \cdot \frac{y_i + y_{i+1}}{2}$$

where $h = x_{i+1} - x_i$ is the width of the interval.

This formula comes directly from geometry: the area of a trapezoid is the width times the average of the two parallel sides.

#### The Extended Trapezoidal Rule

For a complete integral from $x_0$ to $x_N$ with $N$ intervals of uniform width $h$, we sum all trapezoidal areas:

$$I = \sum_{i=0}^{N-1} A_i = \sum_{i=0}^{N-1} h \cdot \frac{y_i + y_{i+1}}{2}$$

Expanding this sum carefully, we notice that every **interior point** appears twice:
- $y_1$ appears in the trapezoid from $x_0$ to $x_1$ (as $y_{i+1}$) and in the trapezoid from $x_1$ to $x_2$ (as $y_i$).
- Each interior point contributes $\frac{h}{2} + \frac{h}{2} = h$ to the total.

The **endpoints** $y_0$ and $y_N$ appear only once, contributing $\frac{h}{2}$ each.

Factoring out $h$, we obtain the **Extended Trapezoidal Rule**:

$$I \approx h \left[ \frac{1}{2}y_0 + y_1 + y_2 + \cdots + y_{N-1} + \frac{1}{2}y_N \right]$$

This is the working formula for practical implementation.

#### Error Analysis: Second-Order Accuracy

The truncation error of the Trapezoidal Rule can be derived using Taylor series expansion. For a single interval $[x_i, x_{i+1}]$:

$$\text{Error}_{\text{local}} = -\frac{h^3}{12} f''(\xi)$$

where $\xi$ is some point in the interval.

When summing over all $N$ intervals, the **global truncation error** is:

$$\text{Error}_{\text{total}} = O(h^2)$$

This means:
- If we **halve** $h$ (double the number of points), the error decreases by a factor of **four** ($2^2 = 4$).
- The method is **second-order accurate**.

#### Why "Cutting Corners" Matters

The straight-line approximation is crude when the true function is curved. Consider integrating $\sin(x)$ from $0$ to $\pi$:
- The trapezoid systematically **underestimates** the area because the straight line cuts below the curve.
- This systematic bias is the price we pay for simplicity.

However, this error decreases rapidly as $h \to 0$, making the method both robust and practical.

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What is the geometric shape used to approximate each slice of the integral in the Trapezoidal Rule?**
    
    - A. A rectangle
    - B. A trapezoid formed by linear interpolation
    - C. A parabola
    - D. A triangle
    
??? info "See Answer"
        **Correct: B**
    
        The Trapezoidal Rule connects adjacent data points with a **straight line**, forming a trapezoid. The area of this trapezoid is $h \cdot (y_i + y_{i+1})/2$, which is the average height times the width.
    
---

!!! note "Quiz"
    **2. In the Extended Trapezoidal Rule, why do interior points receive a weight of 1 while endpoints receive a weight of 1/2?**
    
    - A. It's an arbitrary convention for symmetry
    - B. Interior points are counted twice (once by each adjacent trapezoid), while endpoints appear only once
    - C. The formula requires normalization
    - D. Endpoints are less accurate than interior points
    
??? info "See Answer"
        **Correct: B**
    
        Each interior point $y_i$ serves as the **right edge** of the trapezoid to its left and the **left edge** of the trapezoid to its right. Each contribution adds $h/2$, so $y_i$ receives a total weight of $h/2 + h/2 = h$ (which factors out as 1 when $h$ is pulled outside). The endpoints $y_0$ and $y_N$ appear in only one trapezoid each, receiving a weight of $h/2$.
    
---

!!! note "Quiz"
    **3. If you double the number of grid points $N$ (halving $h$) in the Trapezoidal Rule, the truncation error decreases by a factor of:**
    
    - A. 2
    - B. 4
    - C. 8
    - D. $\sqrt{2}$
    
??? info "See Answer"
        **Correct: B**
    
        The Trapezoidal Rule has **second-order accuracy** ($O(h^2)$). Halving $h$ means the error scales as $(h/2)^2 = h^2/4$, which is **four times smaller** than the original error. This quadratic convergence is a defining characteristic of the method.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Walk me through the conceptual derivation of the Extended Trapezoidal Rule. Why do the interior points have a weight of 1, while the endpoints have a weight of 1/2?
    
    ???+ info "Answer Strategy"
        This question tests your understanding of how the formula arises from summing individual trapezoidal contributions.
    
        1. **Single Trapezoid:**
           The area of one trapezoid from $x_i$ to $x_{i+1}$ is:
           $$A_i = h \cdot \frac{y_i + y_{i+1}}{2}$$
    
        2. **Summing All Trapezoids:**
           The total integral is the sum of all trapezoidal areas:
           $$I = \sum_{i=0}^{N-1} h \cdot \frac{y_i + y_{i+1}}{2}$$
    
        3. **Expanding the Sum:**
           Writing out the first few terms:
           $$I = \frac{h}{2}(y_0 + y_1) + \frac{h}{2}(y_1 + y_2) + \frac{h}{2}(y_2 + y_3) + \cdots + \frac{h}{2}(y_{N-1} + y_N)$$
    
        4. **Collecting Terms:**
           Notice that:
           - $y_0$ appears **once** (coefficient $h/2$)
           - $y_1$ appears **twice**: once as the right edge of the first trapezoid, once as the left edge of the second (total coefficient $h$)
           - $y_2, y_3, \ldots, y_{N-1}$ all appear **twice** (coefficient $h$ each)
           - $y_N$ appears **once** (coefficient $h/2$)
    
        5. **Factoring Out $h$:**
           Pulling out the common factor $h$ gives:
           $$I = h \left[\frac{1}{2}y_0 + y_1 + y_2 + \cdots + y_{N-1} + \frac{1}{2}y_N\right]$$
    
        This is the Extended Trapezoidal Rule. The interior weights of 1 and endpoint weights of 1/2 arise naturally from the overlapping trapezoidal contributions.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Verifying Second-Order Convergence

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                |
| ------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | Implement the Trapezoidal Rule from scratch and verify its **second-order convergence** ($O(h^2)$) by measuring how the error decreases as the number of grid points increases.                                                                                                                |
| **Mathematical Concept** | For a function with known analytical integral, the truncation error should decrease as $h^2$. Doubling the number of points (halving $h$) should reduce the error by a factor of 4.                                                                                                            |
| **Test Function**        | Use $f(x) = \sin(x)$ on the interval $[0, \pi]$. The exact integral is: <br> $$I_{\text{exact}} = \int_0^{\pi} \sin(x) dx = 2$$                                                                                                                                                                |
| **Experiment Setup**     | Run the Trapezoidal Rule for several grid sizes: $N = 10, 20, 40, 80, 160$. For each $N$, compute: <br> - The numerical approximation $I_{\text{trap}}$ <br> - The absolute error $E = \lvert I_{\text{exact}} - I_{\text{trap}} \rvert$ <br> - The error ratio between consecutive grid sizes |
| **Process Steps**        | 1. Implement the Extended Trapezoidal Rule formula. <br> 2. Loop over increasing values of $N$. <br> 3. Compute the integral and error for each $N$. <br> 4. Calculate the ratio of consecutive errors to verify the factor-of-4 reduction.                                                    |
| **Expected Behavior**    | Each doubling of $N$ should reduce the error by a factor **close to 4**, confirming $O(h^2)$ convergence. Minor deviations occur due to round-off error at very small $h$.                                                                                                                     |
| **Tracking Variables**   | - `N`: number of grid points <br> - `h`: grid spacing ($\pi / N$) <br> - `I_trap`: computed integral <br> - `error`: absolute error <br> - `error_ratio`: ratio of consecutive errors                                                                                                         |
| **Verification Goal**    | Confirm that `error_ratio` $\approx 4$ for each doubling of $N$, validating the theoretical prediction of second-order accuracy.                                                                                                                                                              |
| **Output**               | Print a table showing $N$, $h$, $I_{\text{trap}}$, error, and error ratio for each grid size.                                                                                                                                                                                                  |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Setup
  FUNCTION f(x):
      RETURN sin(x)
  END FUNCTION

  SET I_exact = 2.0  // Known analytical result
  SET a = 0.0        // Lower limit
  SET b = π          // Upper limit

  PRINT "===== Trapezoidal Rule: Convergence Test ====="
  PRINT "Function: f(x) = sin(x), Interval: [0, π]"
  PRINT "Exact integral: I = 2.0"
  PRINT "-----------------------------------------------"
  PRINT "  N      h       I_trap      Error      Ratio"
  PRINT "-----------------------------------------------"

  // 2. Test Multiple Grid Sizes
  SET N_values = [10, 20, 40, 80, 160]
  SET previous_error = NULL

  FOR each N in N_values DO:
      // 2a. Compute grid spacing
      SET h = (b - a) / N

      // 2b. Generate grid points
      SET x[i] = a + i * h  for i = 0 to N

      // 2c. Apply Extended Trapezoidal Rule
      SET I_trap = h * (0.5 * f(x[0]) + 0.5 * f(x[N]))
      FOR i FROM 1 TO N-1 DO:
          I_trap = I_trap + h * f(x[i])
      END FOR

      // 2d. Compute error
      SET error = ABS(I_exact - I_trap)

      // 2e. Compute error ratio (if not first iteration)
      IF previous_error IS NOT NULL THEN:
          SET error_ratio = previous_error / error
      ELSE:
          SET error_ratio = "N/A"
      END IF

      // 2f. Output results
      PRINT N, h, I_trap, error, error_ratio

      // 2g. Store error for next iteration
      SET previous_error = error
  END FOR

  PRINT "-----------------------------------------------"
  PRINT "Expected: Error ratio ≈ 4 (second-order convergence)"

END
```

---

#### **Outcome and Interpretation**

* **Expected Results:** For $N = 10, 20, 40, 80, 160$, you should see:

  | $N$  | $h$     | $I_{\text{trap}}$ | Error      | Ratio |
  | ---- | ------- | ----------------- | ---------- | ----- |
  | 10   | 0.3142  | 1.9835            | 0.0165     | N/A   |
  | 20   | 0.1571  | 1.9959            | 0.0041     | ~4.0  |
  | 40   | 0.0785  | 1.9990            | 0.0010     | ~4.0  |
  | 80   | 0.0393  | 1.9997            | 0.00025    | ~4.0  |
  | 160  | 0.0196  | 1.9999            | 0.000063   | ~4.0  |

* **Verification:** The error ratio of approximately **4** confirms that the Trapezoidal Rule is **second-order accurate** ($O(h^2)$). Each halving of $h$ reduces the error by a factor of 4.

* **Deviations:** At very large $N$ (e.g., $N > 10^6$), you may observe deviations from the ideal factor of 4 due to **round-off error** dominating over truncation error. This is the same "V-plot" phenomenon from Chapter 5.

* **Broader Lesson:** This project demonstrates the empirical verification of **convergence order**, a critical concept in numerical analysis. By systematically refining the grid and measuring error reduction, we validate the theoretical predictions derived from Taylor series analysis.

## 6.3 The "Better" Tile: Simpson's Rule {.heading-with-pill}

> **Concept:** Parabolic Interpolation for Superior Accuracy • **Difficulty:** ★★★☆☆

> **Summary:** Simpson's Rule uses parabolic (quadratic polynomial) tiles spanning two grid intervals, achieving fourth-order accuracy ($O(h^4)$). This dramatic improvement over the Trapezoidal Rule makes it the preferred method for smooth functions on uniform grids.

---

### Theoretical Background

The Trapezoidal Rule is robust but crude—its straight-line approximation systematically "cuts corners" when the function curves. **Simpson's Rule** addresses this limitation by using a **smarter tile**: a parabola (quadratic polynomial) that can bend to match the function's curvature.

#### From Lines to Parabolas

**Key Insight:** A straight line is determined by **two points**, but a parabola requires **three points**. Therefore, a single Simpson's "tile" must span **two grid intervals**, using three consecutive data points: $(x_i, y_i)$, $(x_{i+1}, y_{i+1})$, and $(x_{i+2}, y_{i+2})$.

#### Derivation of the Simpson's Formula

Consider three equally-spaced points with spacing $h$:
- Left point: $(x_0, y_0)$
- Middle point: $(x_1, y_1)$ where $x_1 = x_0 + h$
- Right point: $(x_2, y_2)$ where $x_2 = x_0 + 2h$

The **unique parabola** $P(x)$ passing through these three points is a quadratic polynomial. The exact area under this parabola from $x_0$ to $x_2$ can be computed analytically:

$$A = \int_{x_0}^{x_2} P(x) dx = \frac{h}{3}(y_0 + 4y_1 + y_2)$$

This is **Simpson's 1/3 Rule** for a single tile. The name comes from the $h/3$ factor.

Notice the **1-4-2 weighting pattern**:
- The two endpoints receive weight 1
- The middle point receives weight **4**

This pattern arises from the exact integration of the parabolic interpolant.

#### The Extended Simpson's Rule

To integrate over the entire domain $[x_0, x_N]$, we tile the region with overlapping parabolic segments. For this to work, we need an **even number of intervals** (i.e., $N$ must be even, giving us an **odd number of data points**).

The **Extended Simpson's Rule** is:

$$I \approx \frac{h}{3} \left[ y_0 + 4y_1 + 2y_2 + 4y_3 + 2y_4 + \cdots + 2y_{N-2} + 4y_{N-1} + y_N \right]$$

The weighting pattern is **1, 4, 2, 4, 2, ..., 4, 1**:
- First and last points: weight 1
- Odd-indexed interior points: weight 4
- Even-indexed interior points (except endpoints): weight 2

#### Error Analysis: Fourth-Order Accuracy

The power of Simpson's Rule comes from its **fourth-order accuracy**. Using Taylor series expansion, one can show that the local truncation error for a single tile is:

$$\text{Error}_{\text{local}} = -\frac{h^5}{90} f^{(4)}(\xi)$$

When summed over all tiles, the **global truncation error** is:

$$\text{Error}_{\text{total}} = O(h^4)$$

**This means:**
- If we **halve** $h$ (double the number of points), the error decreases by a factor of **sixteen** ($2^4 = 16$).
- Simpson's Rule is dramatically more accurate than the Trapezoidal Rule ($O(h^2)$) for the same grid spacing.

#### Why Fourth-Order?

The magic comes from Taylor series cancellation. When we fit a parabola through three points and integrate, we automatically match the function's value, first derivative, *and* second derivative at the midpoint. This causes the $O(h^3)$ error term to vanish, leaving only $O(h^4)$ and higher terms.

#### The Gotcha: Even Intervals Required

**Critical Limitation:** Simpson's Rule requires an **even number of intervals** (odd number of points). If your data has an odd number of intervals, you must:
- Use Simpson's Rule for all but the last interval
- Handle the final interval with the Trapezoidal Rule
- Or, adjust your grid to have an even number of intervals

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What geometric shape does Simpson's Rule use to approximate each "tile" of the integral?**
    
    - A. A straight line (trapezoid)
    - B. A parabola (quadratic polynomial)
    - C. A cubic spline
    - D. A circle segment
    
??? info "See Answer"
        **Correct: B**
    
        Simpson's Rule fits a **parabola** (2nd-degree polynomial) through three consecutive data points. This parabolic interpolant can curve to match the function's shape, providing much better accuracy than the straight-line approximation of the Trapezoidal Rule.
    
---

!!! note "Quiz"
    **2. What is the characteristic weighting pattern for the Extended Simpson's Rule?**
    
    - A. $\frac{h}{2} [1, 2, 2, 2, \ldots, 2, 1]$
    - B. $h [1/2, 1, 1, 1, \ldots, 1, 1/2]$
    - C. $\frac{h}{3} [1, 4, 2, 4, 2, \ldots, 4, 1]$
    - D. $\frac{h}{3} [1, 4, 1, 4, 1, \ldots, 4, 1]$
    
??? info "See Answer"
        **Correct: C**
    
        The Extended Simpson's Rule has the signature **1-4-2-4-2-...-4-1** weighting pattern. The endpoints have weight 1, odd-indexed interior points have weight 4, and even-indexed interior points have weight 2. This pattern emerges from overlapping parabolic tiles and is preceded by the factor $h/3$.
    
---

!!! note "Quiz"
    **3. If you double the number of grid points $N$ (halving $h$) in Simpson's Rule, the truncation error decreases by a factor of:**
    
    - A. 2
    - B. 4
    - C. 8
    - D. 16
    
??? info "See Answer"
        **Correct: D**
    
        Simpson's Rule has **fourth-order accuracy** ($O(h^4)$). Halving $h$ means the error scales as $(h/2)^4 = h^4/16$, which is **sixteen times smaller** than the original error. This is why Simpson's Rule is so powerful for smooth functions—it converges much faster than the Trapezoidal Rule's $O(h^2)$ convergence.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** Why would anyone ever use the Trapezoidal Rule if Simpson's Rule is so much more accurate ($O(h^4)$ vs $O(h^2)$)? Hint: Think about the "gotcha" or simplicity of implementation.
    
    ???+ info "Answer Strategy"
        This question tests your understanding of the trade-offs between accuracy and robustness in numerical methods.
    
        1. **The Even-Interval Requirement:**
           Simpson's Rule has a structural constraint: it **requires an even number of intervals** (odd number of data points). If your experimental data happens to have 100 points, you cannot directly apply Simpson's Rule without modification. The Trapezoidal Rule has no such restriction—it works for any number of points.
    
        2. **Simplicity and Robustness:**
           The Trapezoidal Rule is conceptually simpler, easier to implement, and more robust to edge cases. For quick exploratory work or when implementing from scratch, the Trapezoidal Rule is often the first choice.
    
        3. **Noisy Data:**
           For extremely **noisy** or **irregular** data (common in experimental physics), the parabolic fits of Simpson's Rule can actually be counterproductive. Parabolas can "wiggle" to fit high-frequency noise, whereas the straight-line smoothing of the Trapezoidal Rule can be more stable.
    
        4. **Non-Uniform Grids:**
           The standard Simpson's Rule formula assumes **uniform spacing** $h$. For non-uniform grids, the derivation becomes more complex, whereas the Trapezoidal Rule generalizes trivially: $A_i = \frac{1}{2}(x_{i+1} - x_i)(y_i + y_{i+1})$.
    
        5. **The Takeaway:**
           Simpson's Rule is superior for **smooth, well-behaved functions on uniform grids** with the right number of points. But the Trapezoidal Rule remains the **workhorse** for many practical applications due to its universal applicability and simplicity.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** $O(h^2)$ vs. $O(h^4)$ Convergence Showdown

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                  |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Objective**            | Implement both the Trapezoidal Rule and Simpson's Rule from scratch and visually compare their **convergence rates** using a log-log plot. This demonstrates the dramatic difference between second-order and fourth-order accuracy.                                                             |
| **Mathematical Concept** | The error of the Trapezoidal Rule scales as $O(h^2)$, while Simpson's Rule scales as $O(h^4)$. On a log-log plot of Error vs. $N$ (number of intervals), these should appear as straight lines with slopes of $-2$ and $-4$, respectively.                                                      |
| **Test Function**        | Use $f(x) = \sin(x)$ on the interval $[0, \pi]$. The exact integral is: <br> $$I_{\text{exact}} = \int_0^{\pi} \sin(x) dx = 2$$                                                                                                                                                                  |
| **Experiment Setup**     | Run both methods for a range of grid sizes: $N = 10, 20, 40, 80, 160, 320, 640$. For each $N$: <br> - Compute $I_{\text{trap}}$ and $I_{\text{simp}}$ <br> - Calculate absolute errors <br> - Plot $\log(\text{Error})$ vs. $\log(N)$ <br> Note: $N$ must be even for Simpson's Rule.           |
| **Process Steps**        | 1. Implement the Extended Trapezoidal Rule. <br> 2. Implement the Extended Simpson's Rule. <br> 3. Loop over increasing (even) values of $N$. <br> 4. Store errors for both methods. <br> 5. Create a log-log plot with reference lines showing slopes of $-2$ and $-4$.                         |
| **Expected Behavior**    | The Trapezoidal error line should have slope $-2$ (error $\propto N^{-2}$). The Simpson's error line should have slope $-4$ (error $\propto N^{-4}$). Simpson's line will drop much more steeply, demonstrating the power of higher-order methods.                                              |
| **Tracking Variables**   | - `N_values`: array of grid sizes (all even) <br> - `errors_trap`: array of Trapezoidal errors <br> - `errors_simp`: array of Simpson's errors <br> - `slopes`: fitted slopes from log-log data                                                                                                 |
| **Verification Goal**    | Visually confirm that Simpson's Rule achieves dramatically lower error for the same $N$, and that the slopes match theoretical predictions ($-2$ and $-4$).                                                                                                                                      |
| **Output**               | A log-log plot with: <br> - Blue line: Trapezoidal Rule errors (slope $\approx -2$) <br> - Red line: Simpson's Rule errors (slope $\approx -4$) <br> - Reference lines showing theoretical slopes <br> - Legend and axis labels                                                                  |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Setup
  IMPORT numpy as np
  IMPORT matplotlib.pyplot as plt

  FUNCTION f(x):
      RETURN sin(x)
  END FUNCTION

  SET I_exact = 2.0
  SET a = 0.0
  SET b = π

  // 2. Define Grid Sizes (must be even for Simpson's)
  SET N_values = [10, 20, 40, 80, 160, 320, 640]
  SET errors_trap = []
  SET errors_simp = []

  // 3. Compute Errors for Both Methods
  FOR each N in N_values DO:
      SET h = (b - a) / N
      SET x = [a + i*h for i in 0 to N]
      SET y = [f(xi) for xi in x]

      // 3a. Trapezoidal Rule
      SET I_trap = h * (0.5 * y[0] + sum(y[1:N]) + 0.5 * y[N])
      SET error_trap = ABS(I_exact - I_trap)
      APPEND error_trap to errors_trap

      // 3b. Simpson's Rule
      SET I_simp = (h / 3) * (y[0] + y[N])
      FOR i FROM 1 TO N-1 DO:
          IF i is odd THEN:
              I_simp = I_simp + (h / 3) * 4 * y[i]
          ELSE:
              I_simp = I_simp + (h / 3) * 2 * y[i]
          END IF
      END FOR
      SET error_simp = ABS(I_exact - I_simp)
      APPEND error_simp to errors_simp
  END FOR

  // 4. Create Log-Log Plot
  FIGURE
  PLOT log(N_values), log(errors_trap), label="Trapezoidal (O(h²))", color=blue, marker=circle
  PLOT log(N_values), log(errors_simp), label="Simpson's (O(h⁴))", color=red, marker=square

  // 4a. Add Reference Lines
  SET N_ref = N_values[0]
  SET E_ref_trap = errors_trap[0]
  SET E_ref_simp = errors_simp[0]

  PLOT log(N_values), log(E_ref_trap * (N_ref / N_values)^2),
       linestyle=dashed, color=blue, label="Slope = -2"
  PLOT log(N_values), log(E_ref_simp * (N_ref / N_values)^4),
       linestyle=dashed, color=red, label="Slope = -4"

  // 4b. Labels and Formatting
  XLABEL "log(N)"
  YLABEL "log(Error)"
  TITLE "Convergence: Trapezoidal vs. Simpson's Rule"
  LEGEND
  GRID ON
  SHOW

  // 5. Print Summary
  PRINT "===== Convergence Analysis ====="
  PRINT "Function: sin(x), Interval: [0, π]"
  PRINT "Exact integral: 2.0"
  PRINT "--------------------------------"
  PRINT "At N = 640:"
  PRINT "  Trapezoidal error:", errors_trap[-1]
  PRINT "  Simpson's error:  ", errors_simp[-1]
  PRINT "  Improvement factor:", errors_trap[-1] / errors_simp[-1]

END
```

---

#### **Outcome and Interpretation**

* **Visual Result:** The log-log plot will show two clear trends:
  - The **Trapezoidal Rule** (blue) follows a line with slope $\approx -2$, confirming $O(N^{-2}) = O(h^2)$ convergence.
  - **Simpson's Rule** (red) follows a much steeper line with slope $\approx -4$, confirming $O(N^{-4}) = O(h^4)$ convergence.

* **Quantitative Comparison:** At $N = 640$:
  - Trapezoidal error: $\approx 10^{-5}$
  - Simpson's error: $\approx 10^{-11}$
  - **Improvement factor: ~1 million times more accurate!**

* **Practical Implications:**
  - For a target accuracy of $10^{-8}$:
```
- Trapezoidal Rule requires $N \approx 10^4$ points
- Simpson's Rule requires only $N \approx 100$ points
```
  - This massive reduction in computational cost makes Simpson's Rule the clear winner for smooth functions.

* **Limitations Observed:**
  - At very large $N$ (beyond $10^6$), both methods may show deviations from ideal convergence due to **round-off error** accumulation.
  - For rough or noisy functions, Simpson's higher sensitivity to local variations can sometimes reduce its advantage.

* **Broader Lesson:** This project demonstrates why **order of accuracy matters**. The difference between $O(h^2)$ and $O(h^4)$ is not incremental—it's transformative. Higher-order methods achieve dramatic computational savings for smooth problems.

## 6.4 The "Optimal" Tile: Gaussian Quadrature {.heading-with-pill}

> **Concept:** Optimal Sampling Points and Weights • **Difficulty:** ★★★★☆

> **Summary:** Gaussian Quadrature achieves maximum polynomial accuracy by optimally choosing both the sample points $x_i$ and weights $w_i$. With $N$ points, it perfectly integrates polynomials up to degree $2N-1$, making it the most powerful method for smooth, callable functions.

---

### Theoretical Background

Both the Trapezoidal Rule and Simpson's Rule use **fixed, evenly-spaced grid points**. Gaussian Quadrature asks a profound question: *What if we could choose where to sample the function and how much weight to give each sample to maximize accuracy?*

#### The Fundamental Idea

Instead of forcing the grid to be uniform, Gaussian Quadrature uses the general weighted sum formula:

$$I \approx \sum_{i=1}^{N} w_i f(x_i)$$

where:
- $x_i$ are the **sample points** (abscissas)
- $w_i$ are the **weights**

For a fixed number of points $N$, we have $2N$ free parameters ($N$ positions plus $N$ weights). The brilliant insight: we can use this freedom to make the formula **exact** for polynomials of degree up to $2N - 1$.

**Examples:**
- With $N = 1$ point: exact for polynomials up to degree 1 (linear)
- With $N = 2$ points: exact for polynomials up to degree 3 (cubic)
- With $N = 3$ points: exact for polynomials up to degree 5

This is dramatically more powerful than Simpson's Rule, which with 3 points is only exact for polynomials up to degree 2 (quadratic).

#### The Mathematical Foundation: Legendre Polynomials

The optimal sample points $x_i$ turn out to be the **roots of Legendre polynomials** $P_N(x)$, which are orthogonal polynomials on the interval $[-1, 1]$.

**Legendre Polynomials (first few):**
- $P_0(x) = 1$
- $P_1(x) = x$
- $P_2(x) = \frac{1}{2}(3x^2 - 1)$
- $P_3(x) = \frac{1}{2}(5x^3 - 3x)$
- $P_4(x) = \frac{1}{8}(35x^4 - 30x^2 + 3)$

The roots of $P_N(x)$ give the optimal $N$ sample points on $[-1, 1]$.

**Example:** For $N = 2$ (Gauss-Legendre quadrature):
- Roots of $P_2(x) = \frac{1}{2}(3x^2 - 1)$ are $x = \pm 1/\sqrt{3} \approx \pm 0.5774$
- Corresponding weights are both $w = 1$
- The formula is: $I \approx f(-1/\sqrt{3}) + f(1/\sqrt{3})$

This simple two-point formula is **exact** for all polynomials up to degree 3!

#### Transforming to Arbitrary Intervals

The standard Gaussian quadrature is defined on $[-1, 1]$. To integrate over an arbitrary interval $[a, b]$, we use a change of variables:

$$x = \frac{b - a}{2}t + \frac{a + b}{2}$$

where $t \in [-1, 1]$. The integral transforms as:

$$\int_a^b f(x) dx = \frac{b - a}{2} \int_{-1}^{1} f\left(\frac{b-a}{2}t + \frac{a+b}{2}\right) dt$$

#### Error Analysis

For smooth functions (not just polynomials), the error of $N$-point Gaussian quadrature is:

$$\text{Error} = \frac{(b-a)^{2N+1} (N!)^4}{(2N+1)[(2N)!]^3} f^{(2N)}(\xi)$$

For large $N$, this error decreases **exponentially fast** for smooth functions, making Gaussian quadrature extraordinarily powerful.

#### The Professional Tool: `scipy.integrate.quad`

In practice, we access Gaussian quadrature through **`scipy.integrate.quad`**, which implements an adaptive, sophisticated version called **Gauss-Kronrod quadrature**:

**Features:**
- Automatically chooses the number of points based on desired accuracy
- Provides an error estimate
- Handles singularities at endpoints gracefully
- **Requires:** A callable Python function `f(x)`

**Limitation:** Cannot be used with pre-existing grid data—it needs the freedom to evaluate $f$ at its chosen optimal points.

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What is the "Aha! Moment" of Gaussian Quadrature?**
    
    - A. It uses parabolic tiles for $O(h^4)$ accuracy
    - B. It optimally chooses both sample points $x_i$ and weights $w_i$ to maximize polynomial accuracy
    - C. It uses random sampling like Monte Carlo methods
    - D. It works only for grid-based data
    
??? info "See Answer"
        **Correct: B**
    
        Gaussian Quadrature breaks free from the constraint of fixed, uniform grids. By optimally choosing **where** to sample the function ($x_i$) and **how much** to weight each sample ($w_i$), it achieves the maximum possible polynomial accuracy for a given number of function evaluations. With $N$ points, it's exact for polynomials up to degree $2N - 1$.
    
---

!!! note "Quiz"
    **2. With $N = 3$ Gaussian quadrature points, the method is exact for polynomials up to what degree?**
    
    - A. Degree 2
    - B. Degree 3
    - C. Degree 5
    - D. Degree 6
    
??? info "See Answer"
        **Correct: C**
    
        The general rule is that $N$-point Gaussian quadrature is exact for polynomials up to degree $2N - 1$. For $N = 3$: $2(3) - 1 = 5$. This is remarkable—three carefully chosen points can exactly integrate a quintic polynomial, whereas Simpson's Rule (also using 3 points) only exactly integrates up to degree 2.
    
---

!!! note "Quiz"
    **3. You have a callable Python function `f(x)` and want the most accurate possible answer for $\int_0^1 f(x) dx$. Which method should you use?**
    
    - A. Manual implementation of Simpson's Rule
    - B. `scipy.integrate.trapezoid` on a uniform grid
    - C. `scipy.integrate.quad` (Gaussian Quadrature)
    - D. Monte Carlo integration
    
??? info "See Answer"
        **Correct: C**
    
        `scipy.integrate.quad` uses adaptive Gaussian quadrature (specifically Gauss-Kronrod), which is the gold standard for integrating smooth, callable functions. It automatically chooses optimal sample points, adapts to the function's behavior, and provides an error estimate. For a callable function (not pre-gridded data), this is always the best choice.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** I have a fixed grid of experimental data in a NumPy array. Why is `scipy.integrate.quad` the *wrong* tool to use, even though it's the most powerful 1D integrator?
    
    ???+ info "Answer Strategy"
        This question tests your understanding of the fundamental difference between grid-based and function-based quadrature methods.
    
        1. **The Core Issue: Function Evaluation Freedom**
           `scipy.integrate.quad` uses Gaussian quadrature, which requires the ability to evaluate the function $f(x)$ at **arbitrary, optimally chosen points** $x_i$. These points are the roots of Legendre polynomials and are **not** evenly spaced.
    
        2. **Fixed Grid Constraint:**
           When you have experimental data in a NumPy array, your $x$-coordinates are **already locked in**. You measured the function at specific, predetermined locations (e.g., $x = 0.0, 0.1, 0.2, \ldots, 1.0$). You cannot "re-measure" the function at the optimal Gaussian points like $x = 0.1127, 0.5, 0.8873$.
    
        3. **Type Mismatch:**
           `quad` expects a **callable function** `def f(x): ...` as input, not an array of pre-computed values. You could try to create an interpolating function from your data, but this adds complexity and potential interpolation error.
    
        4. **The Right Tool for the Job:**
           For fixed-grid data, you must use grid-based methods like:
           - `scipy.integrate.trapezoid(y, x)` for Trapezoidal Rule
           - `scipy.integrate.simpson(y, x)` for Simpson's Rule
    
           These methods work with your existing $(x_i, y_i)$ pairs without requiring additional function evaluations.
    
        5. **The Broader Principle:**
           The choice of integration method depends fundamentally on your **data format**:
           - **Callable function** → Use Gaussian quadrature (`quad`)
           - **Fixed grid data** → Use grid-based methods (Simpson's, Trapezoidal)
           - **High-dimensional** or **noisy** → Consider Monte Carlo
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Quantum Mechanics—Normalizing a Wavefunction

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | Use Gaussian quadrature to compute the normalization constant $A$ for a quantum mechanical wavefunction, demonstrating the power of optimal sampling for smooth, oscillatory functions.                                                                                                     |
| **Physical Context**     | In quantum mechanics, the probability density $\lvert\psi(x)\rvert^2$ must integrate to 1 over all space (or the confining region). For a particle in a box of length $L$, a trial wavefunction might be: <br> $$\psi(x) = A \cos\left(\frac{\pi x}{L}\right)$$ for $x \in [-L/2, L/2]$. |
| **Mathematical Problem** | Find the normalization constant $A$ such that: <br> $$\int_{-L/2}^{L/2} \lvert\psi(x)\rvert^2 dx = 1$$ <br> This requires computing: <br> $$I = \int_{-L/2}^{L/2} \cos^2\left(\frac{\pi x}{L}\right) dx$$ <br> Then $A = 1/\sqrt{I}$.                                                       |
| **Analytical Solution**  | Using the trig identity $\cos^2(\theta) = \frac{1}{2}(1 + \cos(2\theta))$: <br> $$I = \int_{-L/2}^{L/2} \frac{1}{2}\left[1 + \cos\left(\frac{2\pi x}{L}\right)\right] dx = \frac{L}{2}$$ <br> Therefore, $A = \sqrt{2/L}$.                                                                |
| **Experiment Setup**     | Use `scipy.integrate.quad` to compute $I$ numerically. Set $L = 1.0$ m. Compare the numerical result to the analytical value $I = 0.5$ and verify $A \approx \sqrt{2} \approx 1.414$.                                                                                                       |
| **Process Steps**        | 1. Define the integrand $f(x) = \cos^2(\pi x / L)$. <br> 2. Call `scipy.integrate.quad(f, -L/2, L/2)`. <br> 3. Extract the integral value $I$ and error estimate. <br> 4. Compute $A = 1/\sqrt{I}$. <br> 5. Compare to analytical solution.                                               |
| **Expected Behavior**    | `quad` should return $I \approx 0.5$ with an error estimate near machine precision ($\sim 10^{-14}$), demonstrating the power of Gaussian quadrature for smooth functions.                                                                                                                 |
| **Tracking Variables**   | - `L`: box length (m) <br> - `I_numerical`: computed integral <br> - `I_exact`: analytical value (0.5) <br> - `A_numerical`: computed normalization constant <br> - `A_exact`: analytical value ($\sqrt{2}$) <br> - `error_estimate`: from `quad`                                          |
| **Verification Goal**    | Confirm that the numerical normalization constant matches $\sqrt{2/L}$ to within the error estimate, validating both the method and the analytical calculation.                                                                                                                            |
| **Output**               | Print the integral value, error estimate, normalization constant, and comparison to analytical solution.                                                                                                                                                                                    |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Physical Parameters
  SET L = 1.0  // meters (box length)

  // 2. Define the Integrand
  FUNCTION integrand(x):
      RETURN cos(π * x / L)^2
  END FUNCTION

  // 3. Analytical Solution (for verification)
  SET I_exact = L / 2
  SET A_exact = sqrt(2 / L)

  // 4. Numerical Integration using Gaussian Quadrature
  SET lower_limit = -L / 2
  SET upper_limit = L / 2

  // Call scipy.integrate.quad (returns [result, error_estimate])
  SET [I_numerical, error_estimate] = quad(integrand, lower_limit, upper_limit)

  // 5. Compute Normalization Constant
  SET A_numerical = 1 / sqrt(I_numerical)

  // 6. Output Results
  PRINT "===== Quantum Wavefunction Normalization ====="
  PRINT "Box length L:", L, "m"
  PRINT "Wavefunction: ψ(x) = A cos(πx/L)"
  PRINT "----------------------------------------------"
  PRINT "Integral Computation:"
  PRINT "  Numerical result:", I_numerical
  PRINT "  Analytical result:", I_exact
  PRINT "  Absolute error:", ABS(I_numerical - I_exact)
  PRINT "  Error estimate from quad:", error_estimate
  PRINT "----------------------------------------------"
  PRINT "Normalization Constant:"
  PRINT "  A (numerical):", A_numerical
  PRINT "  A (exact):", A_exact
  PRINT "  Relative error:", ABS(A_numerical - A_exact) / A_exact
  PRINT "----------------------------------------------"

  // 7. Verification
  IF ABS(I_numerical - I_exact) < 1e-10 THEN:
      PRINT "✓ Integral matches analytical solution to machine precision"
  ELSE:
      PRINT "✗ Warning: Numerical integral deviates from expected value"
  END IF

  IF ABS(A_numerical - A_exact) / A_exact < 1e-10 THEN:
      PRINT "✓ Normalization constant verified"
  ELSE:
      PRINT "✗ Warning: Normalization constant error exceeds tolerance"
  END IF

  // 8. Physical Interpretation
  PRINT "----------------------------------------------"
  PRINT "Physical Interpretation:"
  PRINT "The wavefunction ψ(x) = √(2/L) cos(πx/L) represents"
  PRINT "the ground state of a particle in a symmetric box."
  PRINT "The normalization ensures ∫|ψ|² dx = 1, meaning the"
  PRINT "particle has 100% probability of being found somewhere."

END
```

---

#### **Outcome and Interpretation**

* **Numerical Accuracy:** `scipy.integrate.quad` should return:
  - $I_{\text{numerical}} \approx 0.5$ (within $\sim 10^{-14}$ of the exact value)
  - Error estimate $\approx 10^{-14}$ (near machine precision)
  - $A_{\text{numerical}} \approx 1.414213562373095$ (matches $\sqrt{2}$ exactly)

* **Why Gaussian Quadrature Excels Here:**
  - The integrand $\cos^2(\pi x/L)$ is **smooth** and **periodic**—ideal for polynomial approximation.
  - Gaussian quadrature exploits this smoothness to achieve exponential convergence.
  - The adaptive algorithm automatically detects that few points are needed for this well-behaved function.

* **Comparison to Grid-Based Methods:**
  - To achieve comparable accuracy with Simpson's Rule, you'd need hundreds or thousands of grid points.
  - Gaussian quadrature achieves machine precision with perhaps 10-20 optimally placed function evaluations.

* **Physical Significance:**
  - The normalization constant $A = \sqrt{2/L}$ ensures that the total probability is exactly 1.
  - This demonstrates how integration is essential for enforcing physical constraints in quantum mechanics.
  - The result $A \propto 1/\sqrt{L}$ shows that the wavefunction amplitude **decreases** as the box size increases (to maintain unit probability over a larger region).

* **Broader Lesson:** This project illustrates the power of **adaptive, function-based integration** for smooth problems. When you have analytic control over the integrand, Gaussian quadrature is unbeatable for efficiency and accuracy.

## 6.5 Handling the "Hard Stuff": Tricky Integrals {.heading-with-pill}

> **Concept:** Change of Variables to Tame Singularities and Infinite Limits • **Difficulty:** ★★★☆☆

> **Summary:** Integrals with infinite limits or singularities cannot be directly evaluated using standard numerical methods. The solution is a **change of variables** that transforms the problematic integral into a well-behaved, finite domain suitable for quadrature.

---

### Theoretical Background

Numerical integration methods are designed for **finite, well-behaved** integrals. They fail catastrophically when confronted with two common pathological cases:

1. **Infinite Limits:** Integrals like $\int_0^\infty e^{-x} dx$
2. **Singularities:** Integrals like $\int_0^1 \frac{1}{\sqrt{x}} dx$ where the integrand diverges

The solution comes from a classical calculus technique: **change of variables** (also called substitution). By carefully choosing a new variable, we can transform these "impossible" integrals into "safe" ones.

#### Problem 1: Infinite Limits

**The Challenge:** How do we integrate from $0$ to $\infty$ when our grid can only have finitely many points?

**Example:** Consider $\int_0^\infty e^{-x} dx = 1$ (known analytically).

**The Fix: Compactification**

We use a substitution that **maps the infinite interval** $[0, \infty)$ onto a **finite interval** like $[0, 1]$.

**Standard Transformation:**
$$t = \frac{1}{1 + x} \quad \Rightarrow \quad x = \frac{1 - t}{t}$$

**Deriving the transformed integral:**

1. **New limits:**
   - When $x = 0$: $t = 1/(1+0) = 1$
   - When $x \to \infty$: $t = 1/(\infty) = 0$

2. **Differential transformation:**
   $$x = \frac{1-t}{t} \quad \Rightarrow \quad dx = -\frac{1}{t^2} dt$$

3. **Substitute into the integral:**
   $$\int_0^\infty e^{-x} dx = \int_1^0 e^{-(1-t)/t} \left(-\frac{1}{t^2}\right) dt$$

4. **Flip limits (absorbing the negative sign):**
   $$= \int_0^1 \frac{1}{t^2} e^{-(1-t)/t} dt$$

This is now a **finite integral** from 0 to 1 with a well-behaved integrand (no singularity at $t=0$ because the exponential decays faster than $1/t^2$ grows).

**Alternative Transformations:**
- $t = e^{-x}$ (maps $[0, \infty) \to (0, 1]$)
- $t = \arctan(x)$ (maps $(-\infty, \infty) \to (-\pi/2, \pi/2)$)
- $x = \tan(t)$ (inverse of above)

#### Problem 2: Singularities

**The Challenge:** The integrand blows up at a point in the integration domain.

**Example:** $\int_0^1 \frac{1}{\sqrt{x}} dx = 2$ (analytically).

At $x = 0$, the integrand $\frac{1}{\sqrt{x}} \to \infty$, which would cause division by zero in a numerical grid.

**The Fix: Singularity Removal**

We choose a substitution that **cancels the singularity**.

**Transformation:**
$$x = t^2 \quad \Rightarrow \quad dx = 2t \, dt$$

**Deriving the transformed integral:**

1. **New limits:**
   - When $x = 0$: $t = 0$
   - When $x = 1$: $t = 1$

2. **Substitute into the integral:**
   $$\int_0^1 \frac{1}{\sqrt{x}} dx = \int_0^1 \frac{1}{\sqrt{t^2}} \cdot 2t \, dt = \int_0^1 \frac{1}{t} \cdot 2t \, dt = \int_0^1 2 \, dt = 2$$

The $1/t$ term from the singularity **exactly cancels** with the $t$ from the Jacobian $dx = 2t \, dt$, leaving a trivial constant integrand!

**General Strategy:**
- For singularities like $x^{-\alpha}$ near $x = 0$, use $x = t^{1/\beta}$ where $\beta > \alpha$.
- For singularities at $x = a$, use $(x - a)^n$ substitutions.

#### The Professional Approach

Modern libraries like `scipy.integrate.quad` have **built-in handling** for infinite limits and endpoint singularities:

```python
# Infinite upper limit

scipy.integrate.quad(lambda x: np.exp(-x), 0, np.inf)

## Singularity at lower endpoint

scipy.integrate.quad(lambda x: 1/np.sqrt(x), 0, 1)
```

These functions detect the special cases and automatically apply appropriate transformations internally.

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. How do we "tame" an integral with an infinite limit, like $\int_0^\infty f(x) dx$?**
    
    - A. Use Monte Carlo, which handles infinity automatically
    - B. Use a change of variables (e.g., $t = 1/(1+x)$) to map the infinite domain to a finite one
    - C. Integrate to a "very large number" (e.g., $10^{10}$) and hope it's correct
    - D. Use Simpson's Rule with an infinite number of slices
    
??? info "See Answer"
        **Correct: B**
    
        The mathematically rigorous approach is a **change of variables** that **compactifies** the infinite interval onto a finite one. For example, $t = 1/(1+x)$ maps $[0, \infty)$ onto $(0, 1]$. This transforms the integral into standard form that any quadrature method can handle. Simply integrating to a "large number" is unreliable—you never know how large is large enough.
    
---

!!! note "Quiz"
    **2. How do we "tame" an integral with a singularity, like $\int_0^1 \frac{1}{\sqrt{x}} dx$?**
    
    - A. Start the integral just after the singularity, e.g., $\int_{0.0001}^1$
    - B. Use a change of variables (e.g., $x = t^2$) chosen to cancel the singularity
    - C. Use the Trapezoidal Rule, which is not affected by singularities
    - D. This integral is unsolvable and must be approximated
    
??? info "See Answer"
        **Correct: B**
    
        The key is choosing a substitution that **cancels the singular behavior**. For $\int_0^1 x^{-1/2} dx$, the substitution $x = t^2$ (so $dx = 2t \, dt$) transforms the integral to $\int_0^1 \frac{1}{t} \cdot 2t \, dt = \int_0^1 2 \, dt$. The $1/t$ singularity exactly cancels with the $t$ from the Jacobian, leaving a constant integrand. Starting "just after" the singularity is a crude workaround that introduces systematic error.
    
---

!!! note "Quiz"
    **3. For the integral $\int_0^\infty e^{-x^2} dx$, which transformation maps it to a finite interval?**
    
    - A. $t = x^2$
    - B. $t = 1/(1+x)$
    - C. $t = e^{-x}$
    - D. $t = \ln(x)$
    
??? info "See Answer"
        **Correct: B**
    
        The substitution $t = 1/(1+x)$ maps $x \in [0, \infty)$ to $t \in (0, 1]$. From $t = 1/(1+x)$, we get $x = (1-t)/t$ and $dx = -1/t^2 \, dt$. This transforms the infinite integral into a finite one that can be evaluated with standard quadrature. Options A and D don't compactify to a finite interval, and option C maps to $(0, 1]$ but is less straightforward for this particular integrand.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** You need to solve $\int_0^\infty e^{-x} dx$ numerically. Walk me through the complete process of transforming this into a "safe" integral using the substitution $t = 1/(1+x)$.
    
    ???+ info "Answer Strategy"
        This question tests your ability to execute a complete change of variables, a fundamental skill for handling pathological integrals.
    
        1. **Define the Substitution:**
           Start with $t = \frac{1}{1+x}$. We need to express $x$ in terms of $t$ and find $dx$.
    
        2. **Invert the Relationship:**
           Solving for $x$:
           $$t(1+x) = 1 \quad \Rightarrow \quad t + tx = 1 \quad \Rightarrow \quad x = \frac{1-t}{t}$$
    
        3. **Transform the Limits:**
           - When $x = 0$: $t = 1/(1+0) = 1$
           - When $x \to \infty$: $t = 1/(\infty) \to 0$
    
        4. **Compute the Differential:**
           Differentiate $x = (1-t)/t = 1/t - 1$:
           $$dx = -\frac{1}{t^2} dt$$
    
        5. **Substitute into the Original Integral:**
           $$\int_0^\infty e^{-x} dx = \int_1^0 e^{-(1-t)/t} \left(-\frac{1}{t^2}\right) dt$$
    
        6. **Flip the Limits:**
           The negative sign from $dx$ flips the integration limits:
           $$= \int_0^1 \frac{1}{t^2} e^{-(1-t)/t} dt$$
    
        7. **Final Result:**
           This is now a **finite integral** from 0 to 1 with an integrand that is well-behaved (no singularities, finite limits). Any standard quadrature method (Simpson's, Gaussian, etc.) can now be applied.
    
        8. **Implementation Detail:**
           In Python:
           ```python
           def transformed_integrand(t):
               return (1/t**2) * np.exp(-(1-t)/t)
    
           result, error = scipy.integrate.quad(transformed_integrand, 0, 1)
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Taming the Gaussian Integral

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                 |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | Numerically verify the famous Gaussian integral $\int_0^\infty e^{-x^2} dx = \frac{\sqrt{\pi}}{2}$ using a change of variables to map the infinite domain to $[0, 1]$.                                                                                                         |
| **Mathematical Context** | The Gaussian integral is fundamental in probability theory, quantum mechanics, and statistical mechanics. Its exact value $\sqrt{\pi}/2 \approx 0.8862269254527580$ provides a perfect test case for our transformation technique.                                              |
| **The Challenge**        | Direct numerical integration from $0$ to $\infty$ is impossible. We must transform the integral to a finite domain.                                                                                                                                                            |
| **Transformation**       | Use the substitution $t = 1/(1+x)$, which gives: <br> - $x = (1-t)/t$ <br> - $dx = -1/t^2 \, dt$ <br> - Limits: $x \in [0, \infty) \to t \in (0, 1]$                                                                                                                           |
| **Transformed Integral** | $$\int_0^\infty e^{-x^2} dx = \int_0^1 \frac{1}{t^2} \exp\left[-\left(\frac{1-t}{t}\right)^2\right] dt$$                                                                                                                                                                       |
| **Experiment Setup**     | Implement the transformed integrand as a Python function and integrate using `scipy.integrate.quad`. Compare to the analytical result $\sqrt{\pi}/2$.                                                                                                                           |
| **Process Steps**        | 1. Define the transformed integrand $f(t)$. <br> 2. Call `quad(f, 0, 1)` to compute the numerical result. <br> 3. Compare to $\sqrt{\pi}/2$. <br> 4. Report absolute and relative errors.                                                                                      |
| **Expected Behavior**    | The numerical result should match the analytical value to within machine precision ($\sim 10^{-14}$ relative error), demonstrating that the transformation successfully tamed the infinite domain.                                                                              |
| **Tracking Variables**   | - `I_numerical`: result from `quad` <br> - `I_exact`: $\sqrt{\pi}/2$ <br> - `error_estimate`: from `quad` <br> - `abs_error`: $\lvert I_{\text{numerical}} - I_{\text{exact}} \rvert$ <br> - `rel_error`: absolute error divided by $I_{\text{exact}}$                         |
| **Verification Goal**    | Confirm that: <br> 1. The transformation eliminates the infinite limit. <br> 2. The numerical result achieves high accuracy (relative error $< 10^{-10}$). <br> 3. The error estimate from `quad` is reliable.                                                                  |
| **Output**               | Print the numerical integral, analytical result, errors, and verification status.                                                                                                                                                                                               |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Import Necessary Libraries
  IMPORT numpy as np
  IMPORT scipy.integrate as integrate

  // 2. Analytical Solution
  SET I_exact = sqrt(π) / 2  // ≈ 0.8862269254527580

  // 3. Define the Transformed Integrand
  // Original: ∫₀^∞ e^(-x²) dx
  // After t = 1/(1+x): ∫₀¹ (1/t²) exp[-((1-t)/t)²] dt

  FUNCTION transformed_integrand(t):
      // Compute x = (1-t)/t
      SET x = (1 - t) / t

      // Compute the integrand value
      SET integrand_value = (1 / t^2) * exp(-x^2)

      RETURN integrand_value
  END FUNCTION

  // 4. Perform Numerical Integration
  PRINT "===== Gaussian Integral: Infinite to Finite Transformation ====="
  PRINT "Original integral: ∫₀^∞ e^(-x²) dx"
  PRINT "Exact value: √π/2 ≈", I_exact
  PRINT "--------------------------------------------------------------"

  // Call quad with the transformed integrand
  SET [I_numerical, error_estimate] = integrate.quad(transformed_integrand, 0, 1)

  // 5. Compute Errors
  SET abs_error = ABS(I_numerical - I_exact)
  SET rel_error = abs_error / I_exact

  // 6. Output Results
  PRINT "Transformed integral: ∫₀¹ (1/t²) exp[-((1-t)/t)²] dt"
  PRINT "--------------------------------------------------------------"
  PRINT "Numerical result:", I_numerical
  PRINT "Error estimate (from quad):", error_estimate
  PRINT "--------------------------------------------------------------"
  PRINT "Verification:"
  PRINT "  Absolute error:", abs_error
  PRINT "  Relative error:", rel_error
  PRINT "--------------------------------------------------------------"

  // 7. Verification Checks
  IF abs_error < 1e-10 THEN:
      PRINT "✓ Numerical result matches analytical value"
  ELSE:
      PRINT "✗ Warning: Error exceeds tolerance"
  END IF

  IF error_estimate < 1e-10 THEN:
      PRINT "✓ Integration achieved high precision"
  ELSE:
      PRINT "⚠ Integration precision is moderate"
  END IF

  // 8. Educational Notes
  PRINT "--------------------------------------------------------------"
  PRINT "Key Insight:"
  PRINT "The substitution t = 1/(1+x) transformed an INFINITE domain"
  PRINT "[0, ∞) into a FINITE domain (0, 1], making the integral"
  PRINT "computationally feasible. This is the power of change of"
  PRINT "variables—turning impossible problems into routine ones."

END
```

---

#### **Outcome and Interpretation**

* **Expected Results:**
  - Numerical value: $I_{\text{numerical}} \approx 0.886226925452758$
  - Exact value: $\sqrt{\pi}/2 \approx 0.886226925452758$
  - Absolute error: $\sim 10^{-15}$ (machine precision)
  - Relative error: $\sim 10^{-14}$

* **What the Transformation Achieved:**
  1. **Eliminated Infinity:** The original integral from $0$ to $\infty$ became a finite integral from $0$ to $1$.
  2. **Preserved Accuracy:** Despite the transformation, we achieve machine-precision accuracy.
  3. **Enabled Computation:** Without this transformation, no standard quadrature method could handle the infinite limit.

* **Why This Works:**
  - The substitution $t = 1/(1+x)$ is a **smooth, monotonic mapping** that preserves the analytic structure of the integrand.
  - The transformed integrand $\frac{1}{t^2} e^{-((1-t)/t)^2}$ is well-behaved on $(0, 1]$—no singularities, no divergences.
  - Gaussian quadrature can efficiently approximate smooth functions on finite intervals.

* **Comparison to Naive Approaches:**
  - **Truncation:** Integrating from $0$ to some large number (e.g., $10$ or $100$) introduces systematic error because the tail $\int_{100}^\infty e^{-x^2} dx$ is non-zero.
  - **How large is large enough?** For $e^{-x^2}$, you'd need $x \sim 10$ for 6-digit accuracy, but there's no automatic way to know this.
  - **The transformation:** Rigorously captures the entire integral with no guesswork.

* **Broader Applications:**
  - Probability theory: Normal distribution cumulative density function
  - Quantum mechanics: Gaussian wavepackets
  - Statistical mechanics: Partition functions with Gaussian weights
  - Error functions: $\text{erf}(x) = \frac{2}{\sqrt{\pi}} \int_0^x e^{-t^2} dt$

* **Critical Lesson:** When facing integrals with infinite limits or singularities, **don't fight the problem—transform it**. Change of variables is one of the most powerful tools in the computational physicist's arsenal.

## 6.6 Core Application: Period of a Nonlinear Pendulum {.heading-with-pill}

> **Concept:** Real-World Integration with Endpoint Singularities • **Difficulty:** ★★★★☆

> **Summary:** The exact period of a nonlinear pendulum requires evaluating an integral with a singularity at the upper limit. This classic problem demonstrates the practical power of sophisticated quadrature methods like `scipy.integrate.quad` to handle realistic physics calculations.

---

### Theoretical Background

The simple pendulum is a cornerstone of classical mechanics, but the textbook formula $T = 2\pi\sqrt{L/g}$ is only valid for **small oscillations** (the small-angle approximation $\sin\theta \approx \theta$). For large swings, we must solve the full nonlinear equation—and this requires numerical integration.

#### The Physics: Conservation of Energy

Consider a pendulum of length $L$ released from rest at angle $\theta_0$. The total mechanical energy is conserved:

$$E = \frac{1}{2}m L^2 \dot{\theta}^2 + mgL(1 - \cos\theta) = mgL(1 - \cos\theta_0)$$

where $m$ is the bob mass, and we've chosen the potential energy zero at the bottom ($\theta = 0$).

Solving for the angular velocity:

$$\dot{\theta} = \sqrt{\frac{2g}{L}} \sqrt{\cos\theta - \cos\theta_0}$$

#### Deriving the Period Integral

The period $T$ is the time for one complete oscillation. By symmetry, this is four times the time to swing from $\theta = 0$ to $\theta = \theta_0$:

$$T = 4 \int_0^{\theta_0} \frac{d\theta}{\dot{\theta}}$$

Substituting the expression for $\dot{\theta}$:

$$T = 4 \int_0^{\theta_0} \frac{d\theta}{\sqrt{\frac{2g}{L}(\cos\theta - \cos\theta_0)}} = 4\sqrt{\frac{L}{2g}} \int_0^{\theta_0} \frac{d\theta}{\sqrt{\cos\theta - \cos\theta_0}}$$

Simplifying:

$$T = \sqrt{\frac{8L}{g}} \int_0^{\theta_0} \frac{d\theta}{\sqrt{\cos\theta - \cos\theta_0}}$$

This is the **exact period formula** for a nonlinear pendulum.

#### The Computational Challenge: Endpoint Singularity

At the upper limit $\theta = \theta_0$, the denominator vanishes:

$$\sqrt{\cos\theta_0 - \cos\theta_0} = \sqrt{0} = 0$$

This creates a **singularity**—the integrand approaches infinity as $\theta \to \theta_0^-$.

**Why is this a problem?**
- A naive grid-based method (Trapezoidal, Simpson's) would evaluate the function **at** $\theta = \theta_0$, causing division by zero.
- Even evaluating near $\theta_0$ leads to catastrophic round-off error due to the subtraction $\cos\theta - \cos\theta_0 \approx 0$.

#### The Professional Solution: `scipy.integrate.quad`

The key insight: `scipy.integrate.quad` uses **adaptive Gaussian quadrature** with special handling for endpoint singularities. It:

1. **Detects** the endpoint singularity automatically
2. **Concentrates** integration points away from the singular endpoint
3. **Uses weight functions** that properly handle the $1/\sqrt{x}$ behavior
4. **Adaptively refines** the quadrature in regions where the integrand changes rapidly

This makes `quad` the ideal tool for this problem.

#### Small-Angle Approximation for Comparison

For small $\theta_0$ (in radians), the standard approximation is:

$$T_{\text{approx}} = 2\pi\sqrt{\frac{L}{g}}$$

This is **independent of amplitude**—a key prediction that fails for large swings.

For larger amplitudes, the exact period is **longer** than the small-angle prediction because the pendulum spends more time at the extremes where its velocity is low.

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What is the source of the computational problem in the nonlinear pendulum period integral?**
    
    - A. The integral has infinite limits
    - B. The integrand has a singularity at the upper endpoint $\theta = \theta_0$
    - C. The integral is 10-dimensional
    - D. The function is too "wiggly" for Simpson's Rule
    
??? info "See Answer"
        **Correct: B**
    
        At $\theta = \theta_0$, the denominator $\sqrt{\cos\theta - \cos\theta_0}$ approaches zero, causing the integrand to diverge to infinity. This is an **endpoint singularity**. Grid-based methods that must evaluate the function at the endpoint will fail with division by zero or severe round-off error.
    
---

!!! note "Quiz"
    **2. For a large swing angle (e.g., $\theta_0 = 45°$), how does the exact period $T_{\text{exact}}$ compare to the small-angle approximation $T_{\text{approx}} = 2\pi\sqrt{L/g}$?**
    
    - A. Significantly shorter
    - B. Exactly the same
    - C. Longer, due to the nonlinearity of the equation
    - D. Shorter, due to energy loss
    
??? info "See Answer"
        **Correct: C**
    
        For large amplitudes, the pendulum spends more time at the extremes of its swing (where velocity is low) compared to the small-angle case. This increases the period. The nonlinear term $\sin\theta$ (vs. the approximation $\theta$) causes this deviation. For $\theta_0 = 45°$, the period is about 3.5% longer than the small-angle prediction.
    
---

!!! note "Quiz"
    **3. Why can't we use a simple grid-based method (like Simpson's Rule) directly for this integral?**
    
    - A. The integral is too long
    - B. The function oscillates too much
    - C. Evaluating at the endpoint $\theta_0$ causes division by zero
    - D. Grid-based methods don't work for physics problems
    
??? info "See Answer"
        **Correct: C**
    
        Grid-based methods require evaluating the function at regular intervals, including the endpoints. At $\theta = \theta_0$, the integrand $1/\sqrt{\cos\theta - \cos\theta_0}$ is **undefined** (division by zero). Even evaluating extremely close to $\theta_0$ leads to catastrophic cancellation in the subtraction $\cos\theta - \cos\theta_0$, destroying numerical accuracy.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** I have an integral with a singularity at $x = 1$. If I use `scipy.integrate.quad(f, 0, 1)`, what internal mechanism does `quad` employ that prevents the code from failing, unlike a simple loop using the Trapezoidal Rule?
    
    ???+ info "Answer Strategy"
        This question tests your understanding of why adaptive Gaussian quadrature succeeds where fixed-grid methods fail.
    
        1. **No Evaluation at the Singularity:**
           `quad` uses **Gaussian quadrature**, which doesn't require evaluating the function at the endpoints. The sample points are the **roots of Legendre polynomials**, which lie strictly **inside** the interval $(0, 1)$, never at the boundaries.
    
        2. **Adaptive Refinement:**
           When `quad` detects rapid changes in the integrand (which happens near a singularity), it automatically **subdivides** the interval into smaller segments and concentrates more evaluation points in the problematic region—all while avoiding the singular point itself.
    
        3. **Specialized Weight Functions:**
           For common singularities (like $1/\sqrt{x}$ at $x=0$), `quad` can use **Gauss-Kronrod rules** with built-in weights that exactly match the singular behavior. This is analogous to the change-of-variables trick we saw in Section 6.5, but implemented internally.
    
        4. **Error Estimation:**
           By comparing results from different quadrature orders (Gauss vs. Kronrod), `quad` estimates the integration error. If the error is too large, it refines further—but never by evaluating at the singularity.
    
        5. **Contrast with Grid Methods:**
           The Trapezoidal Rule in a simple loop would:
           - Evaluate $f(0)$ and $f(1)$ directly → **division by zero**
           - Use fixed, evenly-spaced points → **no adaptive refinement**
           - Lack sophisticated error control → **unreliable results**
    
        6. **The Takeaway:**
           `quad` succeeds because it:
           - Avoids the singular points
           - Adapts to the integrand's behavior
           - Uses mathematically optimal sampling
    
           This makes it robust for real-world physics problems where singularities are common.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** Exact vs. Approximate Pendulum Period

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                             |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | Compute the exact period of a nonlinear pendulum for various initial angles $\theta_0$ and compare to the small-angle approximation, demonstrating when the standard formula breaks down.                                                                                                   |
| **Physical Setup**       | Pendulum with length $L = 1.0$ m under Earth's gravity $g = 9.81$ m/s². Test initial angles: $\theta_0 = 5°, 15°, 30°, 45°, 60°, 80°$.                                                                                                                                                     |
| **Exact Period Formula** | $$T_{\text{exact}} = \sqrt{\frac{8L}{g}} \int_0^{\theta_0} \frac{d\theta}{\sqrt{\cos\theta - \cos\theta_0}}$$                                                                                                                                                                               |
| **Approximate Formula**  | $$T_{\text{approx}} = 2\pi\sqrt{\frac{L}{g}}$$                                                                                                                                                                                                                                              |
| **Computational Task**   | For each $\theta_0$: <br> 1. Define the integrand $f(\theta) = 1/\sqrt{\cos\theta - \cos\theta_0}$ <br> 2. Integrate from $0$ to $\theta_0$ using `quad` <br> 3. Multiply by the coefficient $\sqrt{8L/g}$ <br> 4. Compute the small-angle approximation <br> 5. Calculate the percentage |
| **Expected Behavior**    | - For small angles ($\theta_0 < 10°$): exact $\approx$ approximate (< 1% difference) <br> - For moderate angles ($\theta_0 \approx 30°$): ~2-3% difference <br> - For large angles ($\theta_0 \approx 60°$): ~10% difference <br> - For very large angles ($\theta_0 \approx 80°$): ~20%  |
| **Tracking Variables**   | - `theta_0_degrees`: initial angle in degrees <br> - `theta_0_radians`: converted to radians <br> - `I`: integral result from `quad` <br> - `T_exact`: exact period <br> - `T_approx`: approximate period <br> - `percent_diff`: percentage difference                                     |
| **Verification Goal**    | Create a table and plot showing how the percentage error grows with initial angle, clearly demonstrating the breakdown of the small-angle approximation.                                                                                                                                    |
| **Output**               | - Table of periods vs. initial angle <br> - Plot of percentage difference vs. $\theta_0$ <br> - Commentary on when the approximation is acceptable                                                                                                                                          |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Import Libraries
  IMPORT numpy as np
  IMPORT scipy.integrate as integrate
  IMPORT matplotlib.pyplot as plt

  // 2. Physical Parameters
  SET L = 1.0       // meters (pendulum length)
  SET g = 9.81      // m/s² (gravitational acceleration)
  SET coefficient = sqrt(8 * L / g)

  // 3. Small-Angle Approximation (constant)
  SET T_approx = 2 * π * sqrt(L / g)

  // 4. Test Angles
  SET theta_0_degrees_array = [5, 15, 30, 45, 60, 80]
  SET results = []  // Store [angle, T_exact, T_approx, percent_diff]

  // 5. Compute Exact Period for Each Angle
  PRINT "===== Nonlinear Pendulum: Period vs. Initial Angle ====="
  PRINT "Pendulum length L =", L, "m"
  PRINT "Gravity g =", g, "m/s²"
  PRINT "Small-angle prediction: T ≈", T_approx, "s"
  PRINT "-----------------------------------------------------------"
  PRINT "θ₀(°)    T_exact(s)  T_approx(s)  % Difference"
  PRINT "-----------------------------------------------------------"

  FOR each theta_0_deg in theta_0_degrees_array DO:
      // 5a. Convert to radians
      SET theta_0_rad = theta_0_deg * (π / 180)

      // 5b. Define integrand (with singularity at upper limit)
      FUNCTION integrand(theta):
          SET denominator = sqrt(cos(theta) - cos(theta_0_rad))
          RETURN 1 / denominator
      END FUNCTION

      // 5c. Integrate using quad (handles endpoint singularity)
      SET [I, error_est] = integrate.quad(integrand, 0, theta_0_rad)

      // 5d. Compute exact period
      SET T_exact = coefficient * I

      // 5e. Compute percentage difference
      SET percent_diff = 100 * (T_exact - T_approx) / T_approx

      // 5f. Store results
      APPEND [theta_0_deg, T_exact, T_approx, percent_diff] to results

      // 5g. Print row
      PRINT theta_0_deg, T_exact, T_approx, percent_diff
  END FOR

  PRINT "-----------------------------------------------------------"

  // 6. Create Visualization
  EXTRACT angles = [r[0] for r in results]
  EXTRACT percent_diffs = [r[3] for r in results]

  FIGURE
  PLOT angles, percent_diffs, marker='o', color='red', linewidth=2
  XLABEL "Initial Angle θ₀ (degrees)"
  YLABEL "% Increase from Small-Angle Formula"
  TITLE "Breakdown of Small-Angle Approximation"
  GRID ON
  AXHLINE y=1, linestyle='--', color='gray', label='1% threshold')
  AXHLINE y=5, linestyle='--', color='orange', label='5% threshold')
  LEGEND
  SHOW

  // 7. Analysis and Commentary
  PRINT ""
  PRINT "===== Analysis ====="
  PRINT "• For θ₀ < 10°: Error < 1% → small-angle approximation valid"
  PRINT "• For θ₀ ≈ 30°: Error ≈ 2-3% → approximation reasonable"
  PRINT "• For θ₀ ≈ 60°: Error ≈ 10% → significant deviation"
  PRINT "• For θ₀ > 70°: Error > 15% → approximation unreliable"
  PRINT ""
  PRINT "Physical Insight:"
  PRINT "Large-amplitude oscillations spend more time at the extremes"
  PRINT "where velocity is low, increasing the period beyond the"
  PRINT "constant small-angle prediction."

END
```

---

#### **Outcome and Interpretation**

* **Expected Numerical Results:**

  | $\theta_0$ (°) | $T_{\text{exact}}$ (s) | $T_{\text{approx}}$ (s) | % Difference |
  | -------------- | ---------------------- | ----------------------- | ------------ |
  | 5              | 2.0071                 | 2.0063                  | 0.04%        |
  | 15             | 2.0104                 | 2.0063                  | 0.20%        |
  | 30             | 2.0305                 | 2.0063                  | 1.21%        |
  | 45             | 2.0729                 | 2.0063                  | 3.32%        |
  | 60             | 2.1559                 | 2.0063                  | 7.46%        |
  | 80             | 2.4485                 | 2.0063                  | 22.05%       |

* **Visual Interpretation:**
  The plot shows an **exponential-like growth** in percentage error as $\theta_0$ increases. This clearly demonstrates the breakdown of the linear approximation.

* **Singularity Handling Success:**
  Despite the endpoint singularity at $\theta = \theta_0$, `scipy.integrate.quad` successfully computes all integrals with high accuracy (error estimates $< 10^{-10}$). This validates the robustness of adaptive Gaussian quadrature.

* **Physics Validation:**
  The fact that $T_{\text{exact}} > T_{\text{approx}}$ for all non-zero amplitudes confirms the physical intuition: nonlinearity **slows down** the oscillation compared to the harmonic approximation.

* **Practical Guidelines:**
  - **High-precision timekeeping:** Use exact formula (or higher-order approximations)
  - **Rough estimates:** Small-angle formula acceptable for $\theta_0 < 15°$
  - **Educational demonstrations:** Show both to illustrate nonlinear effects

* **Broader Lesson:** This project demonstrates that **realistic physics problems often involve integrals with singularities**. Professional numerical tools like `scipy.integrate.quad` are essential for handling these cases reliably. Hand-coded grid methods would fail catastrophically here without sophisticated singularity treatment.

## 6.7 Teaser for Volume II: Monte Carlo Integration {.heading-with-pill}

> **Concept:** Stochastic Sampling Defeats the Curse of Dimensionality • **Difficulty:** ★★★★☆

> **Summary:** Monte Carlo integration uses random sampling to evaluate integrals. Its error, $O(1/\sqrt{N})$, is **independent of dimension**, making it the only feasible method for high-dimensional integrals that appear in statistical mechanics, quantum many-body theory, and machine learning.

---

### Theoretical Background

We've seen that grid-based methods (Trapezoidal, Simpson's, Gaussian quadrature) achieve spectacular accuracy in one dimension. But there's a dark secret lurking: they **collapse catastrophically** as the dimension increases. This is known as the **Curse of Dimensionality**.

#### The Curse of Dimensionality

**The Problem:** In $D$ dimensions, a uniform grid with $N$ points per dimension requires $N^D$ total points.

**Example:**
- **1D:** 100 points gives $10^2 = 100$ evaluations
- **2D:** $100 \times 100 = 10^4$ evaluations
- **3D:** $100 \times 100 \times 100 = 10^6$ evaluations
- **10D:** $100^{10} = 10^{20}$ evaluations ← **Impossible!**

Even worse, the **effective accuracy** deteriorates. Simpson's Rule has $O(h^4)$ accuracy in 1D, which becomes $O(N^{-4})$ in terms of the number of points per dimension. In $D$ dimensions:

$$\text{Error} \sim O(N^{-4/D})$$

**Practical Consequence:**

| Dimension $D$ | Simpson's Error | Points Needed for $10^{-6}$ Accuracy |
| ------------- | --------------- | ------------------------------------ |
| 1             | $O(N^{-4})$     | $\sim 100$                           |
| 2             | $O(N^{-2})$     | $\sim 1000$                          |
| 3             | $O(N^{-4/3})$   | $\sim 10^5$                          |
| 10            | $O(N^{-0.4})$   | $\sim 10^{15}$ ← **Impossible!**     |

For high-dimensional problems (common in statistical mechanics, quantum chemistry, finance), **grid methods are completely infeasible**.

#### The Monte Carlo Solution: Random Sampling

**Monte Carlo integration** bypasses the grid entirely by using **random sampling**.

**The Mean Value Method:**

For a $D$-dimensional integral over a domain $\Omega$ with volume $V$:

$$I = \int_\Omega f(\mathbf{x}) \, d\mathbf{x} \approx V \cdot \frac{1}{N} \sum_{i=1}^{N} f(\mathbf{x}_i)$$

where $\mathbf{x}_i$ are **random points** uniformly distributed in $\Omega$.

**Intuition:** The integral is approximated by the **volume times the average function value** over random samples.

#### Error Analysis: The Central Limit Theorem

From probability theory, the error of the Monte Carlo estimate is governed by the **Central Limit Theorem**:

$$\text{Error} \sim \frac{\sigma}{\sqrt{N}}$$

where:
- $\sigma$ is the standard deviation of the function values
- $N$ is the number of random samples

**The Magic:** This error formula **does not depend on the dimension $D$**!

**Comparison:**

| Method           | 1D Error       | 10D Error      | Dimension Dependence |
| ---------------- | -------------- | -------------- | -------------------- |
| Simpson's Rule   | $O(N^{-4})$    | $O(N^{-0.4})$  | Strong (exponential) |
| Monte Carlo      | $O(N^{-0.5})$  | $O(N^{-0.5})$  | None                 |

#### The Verdict: When to Use Monte Carlo

**Monte Carlo is worse than grid methods in low dimensions:**
- In 1D: Simpson's $O(N^{-4})$ beats Monte Carlo $O(N^{-0.5})$ easily
- In 2D-3D: Grid methods still preferable for smooth functions

**Monte Carlo becomes the only option in high dimensions:**
- For $D > 8$: Grid methods become impractical
- For $D \sim 100-1000$: Only Monte Carlo works
- For $D \sim 10^{23}$ (statistical mechanics): Absolutely essential

**Applications:**
- **Statistical mechanics:** Partition function integrals over all particle positions
- **Quantum chemistry:** Many-electron wavefunctions (3$N$ dimensions for $N$ electrons)
- **Finance:** Portfolio risk analysis (hundreds of correlated variables)
- **Machine learning:** High-dimensional loss function optimization

#### Variance Reduction: The Secret to Practical Monte Carlo

The simple random sampling described above is the baseline. In practice, we use **variance reduction techniques** to dramatically improve efficiency:

- **Importance sampling:** Sample more where the integrand is large
- **Stratified sampling:** Ensure uniform coverage of the domain
- **Antithetic variables:** Use correlated samples to reduce variance
- **Control variates:** Exploit known integrals for similar functions

These techniques (covered in Volume II) can reduce the effective $\sigma$, making Monte Carlo competitive even in moderate dimensions.

<div class="section-divider"></div>

### Comprehension Check

!!! note "Quiz"
    **1. What is the "Curse of Dimensionality"?**
    
    - A. Monte Carlo integration is $O(1/\sqrt{N})$
    - B. Grid-based methods become exponentially slow and less accurate as dimension $D$ increases
    - C. All numerical methods fail if $D > 3$
    - D. You must use double-wide tiles for Simpson's Rule in high dimensions
    
??? info "See Answer"
        **Correct: B**
    
        The Curse of Dimensionality refers to the exponential scaling of computational cost with dimension for grid-based methods. In $D$ dimensions, you need $N^D$ grid points (exponential in $D$), and the accuracy degrades from $O(N^{-4})$ in 1D to $O(N^{-4/D})$ in $D$ dimensions. For $D = 10$, this becomes $O(N^{-0.4})$, requiring impossibly many points for reasonable accuracy.
    
---

!!! note "Quiz"
    **2. In which scenario is Monte Carlo integration the best (and likely only) choice?**
    
    - A. A 1D integral of a smooth, callable function
    - B. A 2D integral of data on a fixed grid
    - C. A 1000-dimensional integral for a statistical mechanics problem
    - D. Finding the area under a simple parabola
    
??? info "See Answer"
        **Correct: C**
    
        Monte Carlo is the **only feasible method** for high-dimensional integrals (typically $D > 8$). A 1000-dimensional grid would require $N^{1000}$ points—far beyond any computational capacity. Monte Carlo's error $O(1/\sqrt{N})$ is **independent of dimension**, making it scale identically for 3D, 100D, or 1000D problems. This is why it's essential for statistical mechanics (integrating over $\sim 10^{23}$ degrees of freedom).
    
---

!!! note "Quiz"
    **3. What is the "magic" property of Monte Carlo error that allows it to beat the Curse of Dimensionality?**
    
    - A. It uses optimal Gaussian quadrature points
    - B. The error $O(1/\sqrt{N})$ does not depend on dimension $D$
    - C. It's faster than Simpson's Rule in all dimensions
    - D. It requires no function evaluations
    
??? info "See Answer"
        **Correct: B**
    
        The critical property is **dimension independence**. The error term $\sigma/\sqrt{N}$ contains no factor of $D$. While grid methods need $N^D$ points (exponential in $D$), Monte Carlo needs only $N$ random samples regardless of dimension. To cut the error in half, you need 4× more samples whether you're in 1D, 10D, or 1000D. This dimension-independence is what makes high-dimensional integration possible.
    
---

!!! abstract "Interview-Style Question"
    
    **Q:** What is the "magic" property of Monte Carlo integration's error, $O(1/\sqrt{N})$, that allows it to beat the Curse of Dimensionality? And why doesn't this make it superior to Simpson's Rule in all cases?
    
    ???+ info "Answer Strategy"
        This two-part question tests both your understanding of Monte Carlo's strength and its limitations.
    
        **Part 1: The Magic (Why It Beats the Curse)**
    
        1. **Dimension Independence:**
           The error $\sigma/\sqrt{N}$ contains **no dimension factor $D$**. The same error formula applies whether you're integrating over a 1D line, a 100D hypercube, or a $10^{23}$-dimensional phase space.
    
        2. **Contrast with Grid Methods:**
           Grid-based methods require $N^D$ total points (exponential in $D$), making them impractical for $D > 8$. Monte Carlo requires only $N$ random samples, scaling **linearly** with computational cost regardless of dimension.
    
        3. **Statistical Foundation:**
           This dimension-independence comes from the **Central Limit Theorem**: the variance of a sample mean decreases as $1/N$, regardless of the underlying space's dimension. It's a fundamental property of statistical sampling.
    
        **Part 2: Why Simpson's Still Wins in Low Dimensions**
    
        1. **Convergence Rate Comparison:**
           - Simpson's Rule: $O(N^{-4})$ in 1D (or $O(N^{-4/D})$ in $D$ dimensions)
           - Monte Carlo: $O(N^{-0.5})$ always
    
           In 1D: $N^{-4}$ converges **much faster** than $N^{-0.5}$.
    
        2. **Numerical Example:**
           To achieve error $< 10^{-6}$:
           - Simpson's (1D): $N \sim 100$ points
           - Monte Carlo (1D): $N \sim 10^{12}$ samples
    
           This is a **factor of 10 billion** difference!
    
        3. **The Crossover Point:**
           The dimension where Monte Carlo becomes competitive depends on the function, but typically:
           - $D \leq 3$: Grid methods dominate
           - $D = 4-7$: Case-dependent
           - $D \geq 8$: Monte Carlo becomes essential
    
        4. **The Takeaway:**
           Monte Carlo is not "better"—it's **different**. It trades convergence speed for dimension scalability. Use grid methods for low-dimensional, smooth problems. Use Monte Carlo when dimension makes grids impossible. This is a fundamental trade-off in computational science.
    
---

### <i class="fa-solid fa-flask"></i> Hands-On Project

#### **Project:** 1D Monte Carlo vs. Simpson's Convergence Battle

---

#### **Project Blueprint**

| **Section**              | **Description**                                                                                                                                                                                                                                                                                    |
| ------------------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Objective**            | Visually demonstrate why grid-based methods are superior in 1D by comparing the convergence of Monte Carlo and Simpson's Rule on the same test integral. This highlights the trade-off between convergence rate and dimension scalability.                                                         |
| **Mathematical Concept** | Simpson's Rule: $O(N^{-4})$ convergence (steep) <br> Monte Carlo: $O(N^{-0.5})$ convergence (slow, noisy)                                                                                                                                                                                         |
| **Test Function**        | Use $f(x) = \sin(x)$ on $[0, \pi]$. Exact: $I = 2$.                                                                                                                                                                                                                                               |
| **Experiment Setup**     | Run both methods for $N = 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000, 50000, 100000$. For Monte Carlo, repeat 10 times at each $N$ to show stochastic noise. Plot $\log(\text{Error})$ vs. $\log(N)$.                                                                             |
| **Process Steps**        | 1. Implement Simpson's Rule (deterministic). <br> 2. Implement Mean Value Monte Carlo (random sampling). <br> 3. For each $N$: compute errors for both methods. <br> 4. Create log-log plot with both error curves. <br> 5. Add reference lines showing slopes of $-4$ and $-0.5$.               |
| **Expected Behavior**    | - Simpson's error: steep downward slope ($-4$), smooth curve <br> - Monte Carlo error: shallow downward slope ($-0.5$), noisy curve <br> - Simpson's error drops below $10^{-10}$ around $N \sim 100$ <br> - Monte Carlo still at $\sim 10^{-2}$ even at $N = 10^5$                               |
| **Tracking Variables**   | - `N_values`: array of sample sizes <br> - `errors_simp`: Simpson's errors (deterministic) <br> - `errors_mc_mean`: average Monte Carlo errors <br> - `errors_mc_std`: standard deviation of MC errors (shows stochastic noise) <br> - `theoretical_slopes`: reference lines for visual validation |
| **Verification Goal**    | Confirm that: <br> 1. Simpson's slope $\approx -4$ on log-log plot. <br> 2. Monte Carlo slope $\approx -0.5$. <br> 3. Simpson's is orders of magnitude more accurate for same $N$ in 1D.                                                                                                          |
| **Output**               | - Log-log plot with error bars for Monte Carlo <br> - Reference lines showing theoretical slopes <br> - Table of errors at key $N$ values <br> - Commentary on when each method is appropriate                                                                                                    |

---

#### **Pseudocode Implementation**

```python
BEGIN

  // 1. Import Libraries
  IMPORT numpy as np
  IMPORT matplotlib.pyplot as plt

  // 2. Test Function
  FUNCTION f(x):
      RETURN sin(x)
  END FUNCTION

  SET a = 0.0
  SET b = π
  SET I_exact = 2.0

  // 3. Simpson's Rule Implementation
  FUNCTION simpson_rule(N):
      SET h = (b - a) / N
      SET x = [a + i*h for i in 0 to N]
      SET y = [f(xi) for xi in x]

      SET I = (h / 3) * (y[0] + y[N])
      FOR i FROM 1 TO N-1 DO:
          IF i is odd THEN:
              I = I + (h / 3) * 4 * y[i]
          ELSE:
              I = I + (h / 3) * 2 * y[i]
          END IF
      END FOR

      RETURN I
  END FUNCTION

  // 4. Monte Carlo Implementation
  FUNCTION monte_carlo(N):
      // Generate N random points in [a, b]
      SET x_random = a + (b - a) * random_uniform(size=N)

      // Evaluate function at random points
      SET f_values = [f(x) for x in x_random]

      // Mean value estimate
      SET volume = b - a
      SET I = volume * mean(f_values)

      RETURN I
  END FUNCTION

  // 5. Test Sample Sizes
  SET N_values = [10, 20, 50, 100, 200, 500, 1000, 2000, 5000,
                  10000, 20000, 50000, 100000]
  SET errors_simp = []
  SET errors_mc_mean = []
  SET errors_mc_std = []

  // 6. Run Convergence Tests
  PRINT "===== Convergence Comparison: Simpson's vs. Monte Carlo ====="
  PRINT "Function: sin(x), Interval: [0, π], Exact: I = 2.0"
  PRINT "-------------------------------------------------------------"
  PRINT "     N      Simpson Error    MC Error (mean ± std)"
  PRINT "-------------------------------------------------------------"

  FOR each N in N_values DO:
      // 6a. Simpson's Rule (deterministic)
      IF N is even THEN:  // Simpson's requires even N
          SET I_simp = simpson_rule(N)
          SET error_simp = ABS(I_exact - I_simp)
      ELSE:
          SET error_simp = NaN  // Skip odd N
      END IF
      APPEND error_simp to errors_simp

      // 6b. Monte Carlo (run multiple times to estimate variance)
      SET mc_errors = []
      FOR trial FROM 1 TO 10 DO:
          SET I_mc = monte_carlo(N)
          SET error_mc = ABS(I_exact - I_mc)
          APPEND error_mc to mc_errors
      END FOR
      SET error_mc_mean = mean(mc_errors)
      SET error_mc_std = std(mc_errors)

      APPEND error_mc_mean to errors_mc_mean
      APPEND error_mc_std to errors_mc_std

      // 6c. Print results
      PRINT N, error_simp, error_mc_mean, "±", error_mc_std
  END FOR

  PRINT "-------------------------------------------------------------"

  // 7. Create Log-Log Plot
  FIGURE with size (10, 6)

  // 7a. Simpson's Rule (solid line, no error bars)
  SET valid_simp = [e for e in errors_simp if not isnan(e)]
  SET valid_N_simp = [N_values[i] for i where errors_simp[i] not nan]
  PLOT log(valid_N_simp), log(valid_simp),
       color='blue', marker='o', linewidth=2, label="Simpson's Rule"

  // 7b. Monte Carlo (with error bars)
  ERRORBAR log(N_values), log(errors_mc_mean), yerr=errors_mc_std/errors_mc_mean,
           color='red', marker='s', linewidth=2, label="Monte Carlo", alpha=0.7

  // 7c. Theoretical Reference Lines
  SET N_ref = 100
  SET E_ref_simp = errors_simp where N=100
  SET E_ref_mc = errors_mc_mean where N=100

  PLOT log(N_values), log(E_ref_simp * (N_ref / N_values)^4),
       linestyle='--', color='blue', alpha=0.5, label="O(N⁻⁴) reference"
  PLOT log(N_values), log(E_ref_mc * (N_ref / N_values)^0.5),
       linestyle='--', color='red', alpha=0.5, label="O(N⁻⁰·⁵) reference"

  // 7d. Formatting
  XLABEL "log(N) [Number of samples/points]"
  YLABEL "log(Error)"
  TITLE "Convergence: Simpson's O(N⁻⁴) vs. Monte Carlo O(N⁻⁰·⁵)"
  LEGEND location='upper right'
  GRID ON, alpha=0.3
  SHOW

  // 8. Analysis
  PRINT ""
  PRINT "===== Key Observations ====="
  PRINT "1. Simpson's Rule (blue) shows steep, smooth descent (slope ≈ -4)"
  PRINT "2. Monte Carlo (red) shows shallow, noisy descent (slope ≈ -0.5)"
  PRINT "3. At N=100: Simpson's achieves ~10⁻⁸ error, MC achieves ~10⁻¹ error"
  PRINT "4. To match Simpson's N=100 accuracy, MC needs N ~ 10⁸ samples!"
  PRINT ""
  PRINT "===== The Lesson ====="
  PRINT "In 1D, grid-based methods are VASTLY superior to Monte Carlo."
  PRINT "However, in 10D, Simpson's would need N^10 points (impossible),"
  PRINT "while MC still needs only ~10⁸ samples (feasible)."
  PRINT "This is why Monte Carlo is essential for high-dimensional problems."

END
```

---

#### **Outcome and Interpretation**

* **Visual Result:** The log-log plot shows two dramatically different behaviors:
  - **Simpson's Rule (blue):** Clean, steep downward line with slope $\approx -4$
  - **Monte Carlo (red):** Noisy, shallow downward line with slope $\approx -0.5$

* **Quantitative Comparison at Key Points:**

  | $N$     | Simpson's Error | Monte Carlo Error |
  | ------- | --------------- | ----------------- |
  | 100     | $\sim 10^{-8}$  | $\sim 10^{-1}$    |
  | 1,000   | $\sim 10^{-14}$ | $\sim 10^{-1.5}$  |
  | 10,000  | (machine limit) | $\sim 10^{-2}$    |
  | 100,000 | (machine limit) | $\sim 10^{-2.5}$  |

* **The Dramatic Difference:** To achieve error $< 10^{-6}$:
  - Simpson's needs: $N \approx 50$ points
  - Monte Carlo needs: $N \approx 10^{12}$ samples
  - **Factor difference: 20 billion!**

* **Why Monte Carlo Shows Noise:**
  - The error bars on the Monte Carlo curve come from running multiple trials at each $N$.
  - This demonstrates the **stochastic nature** of Monte Carlo—different random samples give different results.
  - The noise decreases as $1/\sqrt{N}$ but never disappears entirely.

* **The Critical Insight:**
  This project proves that **in 1D, Monte Carlo is terrible** compared to grid methods. But remember: this is a 1D problem. In 100D:
  - Simpson's would need $50^{100} \approx 10^{170}$ points (more atoms than in the universe!)
  - Monte Carlo still needs only $\sim 10^{12}$ samples (feasible on modern supercomputers)

* **Broader Applications (Volume II Preview):**
  - **Statistical Mechanics:** Partition functions integrate over $3N$ spatial dimensions for $N$ particles
  - **Quantum Chemistry:** Many-electron wavefunctions live in $3N$ dimensions
  - **Machine Learning:** Loss functions in deep learning have millions of parameters
  - **Finance:** Risk analysis over hundreds of correlated assets

* **The Fundamental Trade-off:**
  - **Grid methods:** Fast convergence, exponential cost scaling with dimension
  - **Monte Carlo:** Slow convergence, constant cost scaling with dimension
  - **The crossover:** Around $D = 4-8$ depending on accuracy requirements

This project sets the stage for Volume II, where Monte Carlo methods become not just useful but **absolutely essential** for realistic many-body physics simulations.