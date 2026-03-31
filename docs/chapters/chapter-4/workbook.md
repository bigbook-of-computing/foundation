# **Chapter 4: Interpolation, Fitting, and Residual Judgment (Workbook)**

---

> **Summary:** This workbook explores the critical distinction between "hitting the points" and "following the trend." We will analyze the mathematical elegance and numerical dangers of **Lagrange Polynomials**, the localized stability of **Cubic Splines**, and the statistical robustness of **Least-Squares Regression**. By the end, you will be able to diagnose **Runge's Phenomenon** and use **Residual Analysis** to justify your choice of model complexity.

---

## **4.1 Interpolation: The Exact Constraint** {.heading-with-pill}

> **Difficulty:** ★★☆☆☆
> 
> **Concept:** Polynomial Reconstruction
> 
> **Summary:** Interpolation assumes your data points are exact (no noise). We seek a function that passes *exactly* through every point. This section compares global polynomials against piecewise splines.

---

### **Theoretical Background**

**Lagrange Polynomials:** For $N$ points, there is a unique polynomial of degree $N-1$ that passes through all of them.
$$ P(x) = \sum_{i=1}^N y_i L_i(x) $$
While mathematically pure, global polynomials are prone to **Runge's Phenomenon**—wild oscillations near the edges of the interval.

**Cubic Splines:** Instead of one big polynomial, we use many small cubic polynomials between each pair of points, ensuring that the function, the slope, and the curvature are all continuous at the joins (nodes).

!!! tip "Interpolation is for Smooth Truth"
    Use interpolation only when your data comes from a trusted source with zero or negligible noise (e.g., looking up values in a physical property table). If the data is noisy, interpolation will "interpret" the noise as real physics.

---

### **Comprehension Check**

!!! note "Quiz"
    **1. What happens to a high-degree polynomial fit if you add a new data point at the center of the interval?**
    
    - A. Only the local value at that point changes.
    - B. **A "Global Ripple" occurs, where the change at the center can cause massive oscillations at the distant boundaries.**
    - C. The polynomial degree decreases to accommodate the new point.
    - D. The interpolation fails and returns a linear fit.
    
    **2. Why are "Splines" generally preferred over high-degree "Lagrange" polynomials?**
    
    - A. Splines are always lower error than polynomials.
    - B. **Splines offer "Local Control," meaning a change in one area does not cause artificial oscillations to propagate across the entire dataset.**
    - C. Splines are easier to integrate analytically.
    - D. Lagrange polynomials only work for evenly spaced data.

??? info "See Answer"
    **Correct: B, B**  
    1. **B.** Because a global polynomial must pass through all points using a single equation, a small change anywhere is felt everywhere, often leading to Runge's Phenomenon.
    2. **B.** Cubic splines are piecewise; they only connect adjacent nodes, which isolates local changes and prevents the "Global Ripple" effect.

---

## **4.2 Regression: The Statistical Trend** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Minimizing the Residual
> 
> **Summary:** Physical data is almost always "noisy." Instead of fitting the noise, we seek a simple model that minimizes the overall distance to the points. This is the heart of **Least-Squares Fitting**.

---

### **Theoretical Background**

**Least-Squares Logic:**
We minimize the sum of the squares of the **Residuals** ($r_i = y_i - f(x_i)$):
$$ S = \sum_{i=1}^N (y_i - f(x_i, \theta))^2 $$
If the residuals are randomly scattered (no pattern), the model is adequate. If the residuals show a "smile" or a "wave," your model is missing physics.

!!! abstract "Interview-Style Question"
    
    You fitted a 2nd-degree polynomial to your data, and the RMSE is 0.05. You then fitted a 10th-degree polynomial, and the RMSE dropped to 0.001. Why should you still probably choose the 2nd-degree model?
    
    ???+ info "Answer Strategy"
        This is a classic case of **Overfitting**. 
        1. **Noise Fitting:** The 10th-degree model has enough parameters to "wiggle" through every random noise point, resulting in a lower error but a physically meaningless model.
        2. **Generalization:** The 2nd-degree model likely captures the true physical trend. It will perform better on *new* data, whereas the 10th-degree model will fail catastrophically when presented with data it wasn't "trained" on.
        3. **Occam's Razor:** In numerical science, we prefer the simplest model that adequately explains the data.

---

## **4.3 Hands-On Projects** {.heading-with-pill}

### **Project Blueprint: The Interpolation Face-Off**

| Component | Description |
| :--- | :--- |
| **Objective** | Compare Global Polynomials vs. Cubic Splines vs. Linear Fitting on noisy data. |
| **Mathematical Concept** | Runge's Phenomenon and Least-Squares Residuals. |
| **Experiment Setup** | Noisy sampled sine wave over $[0, 2\pi]$. |
| **Process Steps** | 1. Sample 10 points. 2. Interpolate (Spline). 3. Fit (Linear). 4. Analyze Residuals. |
| **Expected Behavior** | Interpolation will track the noise; Fitting will show a smooth (but biased) trend. |
| **Verification Goal** | Plot the residual distribution and identify the "overfitting" signature. |

---

#### **Outcome and Interpretation**

Executing this project proves that **Modeling is a Choice**. You will see that a high-error fit (Linear) can sometimes be "more correct" than a zero-error interpolant if the underlying physics is simple. The **Residual Plot** is your most important diagnostic tool—it tells you when your model is lying to you.

---

## **Exit Ticket**

Before moving to **Chapter 5: Numerical Differentiation**, verify:
- [ ] I can define the difference between "Interpolation" and "Fitting."
- [ ] I can describe **Runge's Phenomenon** in words.
- [ ] I can explain why minimizing squared error is the standard for noisy data.
- [ ] I know how to check a **Residual Plot** for hidden structures.