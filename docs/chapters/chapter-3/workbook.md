# **Chapter 3: Root Finding (Workbook)**

---

> **Summary:** This workbook bridges the gap between pure algebra and numerical approximation. We move from "solving for $x$" to "approximating $x$" through iterative refinement. We will analyze the absolute safety of **Bisection**, the aggressive speed of **Newton-Raphson**, and the practical balance of the **Secant Method**. By the end, you will be able to diagnose convergence failures and select the robust stopping criteria required for scientific-grade solvers.

---

## **3.1 Bracketing: The Safety First Approach** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** The Intermediate Value Theorem
> 
> **Summary:** If a continuous function changes sign between two points $a$ and $b$, there MUST be a root. Bracketing methods like Bisection exploit this "no-fail" logic to trap the root in an ever-shrinking interval.

---

### **Theoretical Background**

**Bisection Logic:**
1.  **Initial Bracket:** Find $[a, b]$ such that $f(a) \cdot f(b) < 0$.
2.  **Midpoint:** $c = (a + b) / 2$.
3.  **Update:** If $f(a) \cdot f(c) < 0$, the root is in $[a, c]$. Otherwise, it's in $[c, b]$.
4.  **Convergence:** The interval size after $n$ steps is $(b-a) / 2^n$.

!!! tip "Slow but Certain"
    Bisection is the only method that **guarantees** convergence even if the function has nasty wiggles or steep slopes. It is the "Safe Mode" of numerical solvers.

---

### **Comprehension Check**

!!! note "Quiz"
    **1. If your initial bracket is $[0, 10]$, how many iterations are needed to reach a precision of $10^{-6}$?**
    
    - A. 6 iterations (one per decimal place).
    - B. 10 iterations.
    - C. **Approximately 24 iterations, as $2^{24} \approx 1.6 \times 10^7$.**
    - D. 1,000,000 iterations (linear scaling).
    
    **2. What is the fundamental requirement for a bracketing method to work?**
    
    - A. The function must be a polynomial.
    - B. **The function must be continuous and have opposite signs at the two ends of the bracket ($f(a) \cdot f(b) < 0$).**
    - C. The initial guess must be within 1% of the true root.
    - D. The derivative of the function must be known.

??? info "See Answer"
    **Correct: C, B**  
    1. **C.** Each iteration of Bisection halves the interval. $(10 / 2^n) \approx 10^{-6} \Rightarrow 2^n \approx 10^7$. Since $2^{10} \approx 10^3$ and $2^{20} \approx 10^6$, 24 iterations are required.
    2. **B.** The Intermediate Value Theorem guarantees a root exists only if the function is continuous and changes sign across the interval.

---

## **3.2 Open Methods: Newton-Raphson & Secant** {.heading-with-pill}

> **Difficulty:** ★★★★☆
> 
> **Concept:** Gradient-Driven Search
> 
> **Summary:** "Open" methods use local derivatives to guess the next position of the root. They are exponentially faster than Bisection but can "explode" if the initial guess is poor or the function is nearly flat.

---

### **Theoretical Background**

**Newton-Raphson Formula:**
$$ x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)} $$
It approximates the function as a straight line at point $x_n$ and follows that line to where it hits the x-axis.

**The Secant Method:**
If you don't know the derivative $f'(x)$, you can use two previous points to estimate the slope:
$$ f'(x_n) \approx \frac{f(x_n) - f(x_{n-1})}{x_n - x_{n-1}} $$

!!! abstract "Interview-Style Question"
    
    Why does Newton-Raphson fail if $f'(x) \approx 0$ near the root? How would you modify the solver to handle this?
    
    ???+ info "Answer Strategy"
        When the derivative is zero, the tangent line is horizontal—it never hits the x-axis. Numerically, the formula becomes $x - f(x)/0$, leading to an infinite step.
        
        **Modification (The Hybrid Strategy):**
        Use a **Hybrid Solver** (like Brent's Method). Keep a bracket $[a, b]$ at all times. Attempt a Newton step; if the step lands outside the bracket or is too small, "fall back" to a Bisection step to ensure progress. This combines the speed of Newton with the safety of Bisection.

---

## **3.3 Hands-On Projects** {.heading-with-pill}

### **Project Blueprint: Root-Finding Reliability Report**

| Component | Description |
| :--- | :--- |
| **Objective** | Compare Bisection, Newton, and Secant on the transcendental equation: $f(x) = \cos(x) - x$. |
| **Mathematical Concept** | Convergence rates: Linear (Bisection) vs. Quadratic (Newton). |
| **Experiment Setup** | Python, NumPy, and a custom `solver_audit` function to track `(x, f(x), error)` per iteration. |
| **Process Steps** | 1. Implement 3 solvers. 2. Solve $\cos(x)-x=0$. 3. Plot error vs. iteration count. |
| **Expected Behavior** | Newton should solve in $< 5$ steps; Bisection will take $\sim 50$ steps for the same tolerance. |
| **Verification Goal** | Identify the fixed decimal digits gained per step (e.g., bits per iteration). |

---

#### **Outcome and Interpretation**

Executing this project proves that **Speed comes with a Price**. Newton is remarkably fast but requires a derivative and a good initial guess. In production physics, we often use Bisection to find the "neighborhood" of the root and then switch to Newton to polish the final decimal places.

---

## **Exit Ticket**

Before moving to **Chapter 4: Interpolation**, verify:
- [ ] I can describe the "Bracket" condition $f(a) \cdot f(b) < 0$.
- [ ] I understand why a flat derivative ($f' \to 0$) is catastrophic for Newton.
- [ ] I can implement a multi-condition stopping criteria (Residual AND Step Size).
- [ ] I have solved at least one root-finding problem from a random starting point.