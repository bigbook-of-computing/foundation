# **Chapter 4: Interpolation, Fitting, and Residual Judgment () () (Workbook)**

---

## Workbook Purpose

This workbook develops professional data-modeling habits through quiz, analysis, labs, and project work.

By the end of this chapter you should be able to:

1. Distinguish interpolation tasks from fitting tasks.
2. Select stable interpolation strategies for sparse smooth data.
3. Fit noisy data and evaluate uncertainty and residual quality.
4. Detect overfitting and extrapolation misuse.
5. Communicate modeling decisions with defensible technical evidence.

---

## Part A: Core Quiz (Conceptual)

!!! note "Quiz 1"
```
Interpolation is most appropriate when:

- A. Data are heavily noisy and trend-only is desired
- B. Data points are treated as exact constraints
- C. Extrapolation dominates the task
- D. Model uncertainty is unknown

```
!!! note "Quiz 2"
```
Least-squares fitting minimizes:

- A. Sum of absolute x values
- B. Sum of signed residuals
- C. Sum of squared residuals
- D. Maximum residual only

```
!!! note "Quiz 3"
```
Runge phenomenon is commonly associated with:

- A. Piecewise cubic splines
- B. Low-degree local interpolation
- C. High-degree global polynomial interpolation on uniform nodes
- D. Linear regression with Gaussian noise

```
!!! note "Quiz 4"
```
A residual pattern with clear oscillation usually indicates:

- A. Excellent model adequacy
- B. Model misspecification or missing structure
- C. Guaranteed homoscedasticity
- D. Numerical overflow

```
!!! note "Quiz 5"
```
Extrapolation is risky because:

- A. Interpolation error theory no longer strongly constrains behavior outside sampled domain
- B. Solvers cannot evaluate outside domain
- C. Splines are undefined outside interval
- D. All models become linear outside interval

```
---

## Part B: Advanced Quiz (Practice)

!!! note "Quiz 6"
```
If you need exact value continuity and smooth first derivative for trajectory data, you should first consider:

- A. 12th-degree global polynomial
- B. Natural cubic spline
- C. Constant model
- D. Random forest

```
!!! note "Quiz 7"
```
A model with very low training RMSE but high validation RMSE likely suffers from:

- A. Underfitting
- B. Overfitting
- C. Integer overflow
- D. Unit conversion success

```
!!! note "Quiz 8"
```
In weighted least squares, higher weight means:

- A. Point has lower reliability
- B. Point contributes less to objective
- C. Point contributes more because it is more trusted
- D. Point is ignored

```
!!! note "Quiz 9"
```
A physically meaningful fit should satisfy:

- A. Numerical convergence only
- B. Residual minimum only
- C. Parameter plausibility and dimensional consistency in addition to error metrics
- D. Highest possible polynomial degree

```
!!! note "Quiz 10"
```
A good model report should include:

- A. Plot colors and font choice only
- B. Parameters without uncertainty
- C. Data preprocessing, model form, fit quality, diagnostics, and limitations
- D. Execution time only

```
---

## Part C: Interview-Style Questions

Answer each in 6 to 12 sentences.

1. Why can exact interpolation be mathematically correct but scientifically misleading for noisy experiments?
2. Explain why residual plots can reveal failures that scalar metrics alone hide.
3. Compare model complexity control via domain knowledge versus purely data-driven selection.
4. How would you justify using spline interpolation for trajectory reconstruction in orbital mechanics?
5. What minimum checks should be mandatory before accepting a fitted model for forecasting?

---

## Part D: Guided Lab 1 (Interpolation vs Fitting)

### Objective

Construct a controlled experiment showing the behavioral difference between interpolation and least-squares fitting under noise.

### Setup Code

```python
import numpy as np
from scipy.interpolate import CubicSpline

rng = np.random.default_rng(42)
x = np.linspace(0, 6, 20)
y_true = np.sin(x)
y_noisy = y_true + 0.12 * rng.standard_normal(len(x))

# Interpolation through noisy points
spline = CubicSpline(x, y_noisy)

# Quadratic trend fit
coef = np.polyfit(x, y_noisy, deg=2)
```

### Tasks

1. Plot noisy points, spline interpolation, and quadratic fit.
2. Compare behavior at sample points and between sample points.
3. Explain which model better reflects local fluctuations and which better reflects global trend.

### Reflection

- If data are measurement-noisy, should local wiggles be interpreted as physics?

---

## Part E: Guided Lab 2 (Runge Demonstration)

### Objective

Empirically demonstrate instability of high-degree global interpolation on uniform nodes.

### Setup Function

$$
f(x) = \frac{1}{1 + 25x^2}, \quad x \in [-1,1]
$$

### Tasks

1. Build interpolation polynomials for degrees 5, 10, and 15 on uniform nodes.
2. Evaluate all models on a dense grid.
3. Plot approximation error near boundaries.
4. Repeat with Chebyshev-like nodes and compare.

### Reflection

- Which node strategy reduced boundary oscillation and why?

---

## Part F: Guided Lab 3 (Residual Diagnostics)

### Objective

Use residual analysis to choose between competing fit models.

### Setup

1. Generate noisy cubic-shaped data.
2. Fit linear, quadratic, and cubic polynomials.
3. Compute RMSE and inspect residual plots.

### Required Output

- A table with model degree, RMSE, and qualitative residual notes.
- One residual plot per model.

### Reflection

- Which model is adequate without unnecessary complexity?

---

## Part G: Applied Project

### Project Title

Data-to-Model Professional Report: Interpolate, Fit, Diagnose, Validate

### Goal

Deliver a professional modeling packet that shows sound algorithmic choice and diagnostic reasoning.

### Required Deliverables

1. Notebook with complete workflow and commentary.
2. Three artifacts saved in chapter codes folder:
   - `codes/ch4_interpolation_comparison.png`
   - `codes/ch4_runge_phenomenon.png`
   - `codes/ch4_fit_residuals.png`
3. One executive summary (400 to 700 words) including:
   - modeling objective
   - method choices and rationale
   - residual findings
   - limitations and next-step recommendations

### Technical Standards

- Explicitly separate interpolation tasks from fitting tasks.
- Report at least one uncertainty indicator (for example, parameter standard error or residual spread).
- Use train/validation split if prediction is claimed.
- Avoid unsupported extrapolation claims.

### Scoring Rubric (30 points)

- Method selection rationale (8)
- Implementation correctness (8)
- Diagnostic quality and interpretation (8)
- Reproducibility and communication quality (6)

---

## Part H: Professional Memo Prompt

Write a short memo (250 to 350 words):

"A colleague proposes a 15th-degree polynomial because it gives near-zero training error. How do you respond as a numerical scientist?"

Include:

1. Bias-variance tradeoff.
2. Runge risk and conditioning concerns.
3. Validation strategy.
4. Simpler alternatives (spline, lower-degree model, regularized approach).

---

## Part I: Self-Check Answers

!!! success "Quiz Key"
    1. B
    2. C
    3. C
    4. B
    5. A
    6. B
    7. B
    8. C
    9. C
    10. C

---

## Exit Ticket

Before Chapter 5, confirm:

- I can justify interpolation versus fitting based on data regime.
- I can explain and detect Runge phenomenon.
- I can use residual analysis to validate or reject a model.
- I can communicate model limitations responsibly.