# **Chapter 4: Interpolation, Fitting, and the Discipline of Modeling Data**

---

# **Introduction**

Chapter 3 taught us how to solve equations reliably when the residual is known. Chapter 4 shifts perspective: in many real settings, we do not start from a full equation. We start from data.

That data may be:

1. Sparse (few measured points).
2. Noisy (measurement uncertainty).
3. Nonuniform (uneven sampling in time or space).
4. Partially observed (missing segments or constrained ranges).

Computational modeling in this regime requires two distinct tools that are often confused:

1. Interpolation: construct a function that passes through known samples.
2. Fitting (regression): construct a function that captures trend while tolerating noise.

This chapter provides a professional framework for deciding which tool is appropriate, quantifying model quality, and avoiding common pathologies such as overfitting, extrapolation error, and unstable polynomial behavior.

---

## Learning Outcomes

By the end of this chapter, you should be able to:

1. Explain the difference between interpolation and fitting in terms of assumptions and goals.
2. Identify when global high-degree polynomial interpolation is unsafe.
3. Apply cubic spline interpolation for stable local approximation.
4. Perform least-squares fitting and interpret parameter uncertainty.
5. Use residual diagnostics to evaluate model adequacy rather than relying on visual fit alone.

---

# **Chapter 4: Outline**

| Sec. | Title | Core Focus |
| :--- | :--- | :--- |
| 4.1 | Data Regimes and Modeling Intent | Sparse vs noisy data, task framing |
| 4.2 | Interpolation Fundamentals | Exact sample matching and local structure |
| 4.3 | Runge Phenomenon and Node Strategy | Why more degree can reduce accuracy |
| 4.4 | Cubic Splines as Practical Interpolators | Local smoothness without global oscillation |
| 4.5 | Least-Squares Fitting | Trend estimation under noise |
| 4.6 | Residual Diagnostics and Model Trust | Validation, bias, variance, and failure modes |
| 4.7 | Summary and Bridge | Transition to differentiation/integration from data |

---

## 4.1 Data Regimes and Modeling Intent

Before choosing algorithms, define the modeling intent.

Intent A: Reconstruct missing values between trusted samples.

- Usually interpolation.
- Assumes measured points are authoritative values.
- Typical in calibration tables or deterministic simulation outputs.

Intent B: Estimate latent relationship from noisy measurements.

- Usually fitting.
- Assumes each observation contains signal + noise.
- Typical in experiments and sensor pipelines.

Mistaking one intent for the other creates systematic error:

1. Interpolating noisy data can overreact to measurement fluctuations.
2. Fitting when exact constraints are required can violate known conditions.

Professional practice starts with a data taxonomy:

1. Deterministic or stochastic source?
2. Noise model available or unknown?
3. Required output: exact reconstruction, trend estimate, or prediction?
4. Domain limits: where interpolation is safe and extrapolation is risky?

---

## 4.2 Interpolation Fundamentals

Given points $(x_i, y_i)$ with distinct $x_i$, interpolation constructs a function $p(x)$ such that:

$$
p(x_i) = y_i \quad \forall i
$$

For polynomial interpolation with $n+1$ points, there is a unique polynomial of degree at most $n$.

Theoretical interpolation error for smooth functions has form:

$$
f(x)-p_n(x)=\frac{f^{(n+1)}(\xi)}{(n+1)!}\prod_{i=0}^{n}(x-x_i)
$$

This expression explains two practical truths:

1. Error depends on higher derivatives of the true function.
2. Error is highly sensitive to node placement.

Hence interpolation quality is about geometry as much as algebra.

---

## 4.3 Runge Phenomenon and Node Strategy

A classic warning in numerical analysis: global high-degree interpolation on equally spaced nodes can oscillate near interval boundaries.

Runge-style behavior reveals a deep lesson:

- Higher polynomial degree is not automatically better.
- Approximation quality is governed by function smoothness, node distribution, and basis stability.

Node strategy matters.

Chebyshev-like nodes reduce boundary oscillation because they cluster near endpoints, controlling the growth of interpolation basis factors.

Practical implications:

1. For many points, avoid one giant global polynomial on uniform nodes.
2. Prefer piecewise local methods (splines) unless global polynomial structure is explicitly required.

---

## 4.4 Cubic Splines as Practical Interpolators

Cubic splines build piecewise third-degree polynomials with continuity constraints on value, first derivative, and second derivative.

Advantages:

1. Local control: changing one data point affects nearby segments more than distant ones.
2. Smoothness: preserves physically plausible continuity in many trajectories.
3. Stability: avoids many high-degree global oscillation pathologies.

Boundary conditions matter:

1. Natural spline: second derivative set to zero at endpoints.
2. Clamped spline: endpoint slopes specified from physics or measurement.

Professional choice of boundary condition should be justified by domain knowledge, not default convenience.

---

## 4.5 Least-Squares Fitting

When data are noisy, exact point matching is usually inappropriate. Least-squares fitting solves:

$$
\min_{\theta} \sum_{i=1}^{m} r_i(\theta)^2, \qquad r_i = y_i - \hat{y}(x_i;\theta)
$$

Linear models permit closed-form normal-equation solutions (with conditioning caveats). Nonlinear models require iterative optimization.

Parameter interpretation should include uncertainty, not just point estimates:

1. Covariance matrix approximates parameter variance.
2. Confidence intervals communicate reliability.
3. Correlated parameters can reduce interpretability.

A good fit is not simply a curve that looks plausible; it is a model with defensible residual structure and physically meaningful parameters.

---

## 4.6 Residual Diagnostics and Model Trust

Residual analysis is the quality-control stage.

A trustworthy model often exhibits residuals that are:

1. Centered near zero.
2. Pattern-free across input domain.
3. Approximately homoscedastic (variance not exploding with x).
4. Not strongly autocorrelated (for ordered data).

Warning signs:

1. Structured residual oscillations -> model misspecification.
2. Fan-shaped residual spread -> heteroscedasticity.
3. Very low training error but poor out-of-sample behavior -> overfitting.
4. Reasonable interpolation but absurd extrapolation -> unsupported domain use.

Use quantitative diagnostics alongside plots:

1. RMSE or MAE for absolute scale.
2. Adjusted criteria for model complexity when comparing candidate models.
3. Train/validation splits when prediction is the objective.

Professional modeling is iterative:

fit -> diagnose -> revise model class -> re-evaluate.

---

## 4.7 Summary and Bridge

Chapter 4 establishes that working with data is a methodological discipline, not a plotting exercise.

Key takeaways:

1. Interpolation and fitting solve different scientific problems.
2. Node choice and basis choice can dominate interpolation behavior.
3. Splines provide robust local smoothness for many practical tasks.
4. Residual diagnostics are essential for model credibility.

Chapter 5 will leverage these approximations to compute derivatives and integrals from discrete data, where approximation error and noise sensitivity become even more tightly coupled.

---

## References

1. Burden, R. L., and Faires, J. D. Numerical Analysis. Brooks/Cole.
2. Quarteroni, A., Sacco, R., and Saleri, F. Numerical Mathematics. Springer.
3. Trefethen, L. N. Approximation Theory and Approximation Practice. SIAM.
4. Hastie, T., Tibshirani, R., and Friedman, J. The Elements of Statistical Learning. Springer.
5. Press, W. H., et al. Numerical Recipes. Cambridge University Press.