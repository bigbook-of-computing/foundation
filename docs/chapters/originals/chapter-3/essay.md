# **Chapter 3: Root Finding as a Scientific Instrument**

---

# **Introduction**

Chapter 2 established an uncomfortable truth: numerical computation is approximate by construction. Chapter 3 answers the next professional question: if every model evaluation is approximate, how do we still solve equations reliably?

In scientific computing, many core tasks reduce to finding roots:

$$
f(x) = 0
$$

A root is not just a mathematical object. It can represent a physical equilibrium, a conservation boundary, a resonance condition, or an eigenvalue constraint. Root finding is therefore not a side topic. It is a central scientific instrument.

This chapter develops root finding from a practitioner viewpoint:

1. Method mechanics (what the algorithm does).
2. Convergence behavior (how fast and under what assumptions).
3. Failure modes (how and why methods break).
4. Professional stopping criteria (how to decide you are done).
5. Physical application (finite square well energy states).

---

## Learning Outcomes

By the end of this chapter, you should be able to:

1. Distinguish bracketing methods from open methods.
2. Explain linear, superlinear, and quadratic convergence in practical terms.
3. Choose a root-finding strategy based on smoothness, derivative access, and safety requirements.
4. Define robust multi-condition stopping criteria.
5. Solve a transcendental physics equation using a defendable workflow.

---

# **Chapter 3: Outline**

| Sec. | Title | Core Idea |
| :--- | :--- | :--- |
| 3.1 | Why Roots Matter in Physics | Root equations as physical constraints |
| 3.2 | Bisection: Safety First | Guaranteed convergence under sign change |
| 3.3 | Newton-Raphson: Local Speed | Derivative-informed updates and fragility |
| 3.4 | Secant and Hybrid Practice | Derivative-free acceleration and robust combinations |
| 3.5 | Stopping Criteria and Verification | Tolerance design, residual traps, and sanity checks |
| 3.6 | Core Case Study: Finite Square Well | Bound-state roots from transcendental equations |

---

## 3.1 Why Roots Matter in Physics

Many equations in applied physics are not solved in explicit form. Instead, the target variable is embedded nonlinearly, and we solve for where a residual function crosses zero.

Examples:

1. Force balance: $F_{\text{net}}(x)=0$.
2. Nonlinear circuit operating point: $I(V)-I_{\text{load}}(V)=0$.
3. Dispersion relations: $D(\omega, k)=0$.
4. Quantum boundary constraints: transcendental matching equations.

A root-finding workflow translates physical interpretation into numerical procedure:

1. Build a residual function from governing equations.
2. Inspect domain, singularities, and expected root count.
3. Choose algorithm class (safe vs fast vs hybrid).
4. Validate with tolerance and physical checks.

---

## 3.2 Bisection: Safety First

Bisection is the method of controlled narrowing. If $f(a)$ and $f(b)$ have opposite signs and $f$ is continuous on $[a,b]$, then at least one root lies inside.

Algorithm:

1. Compute midpoint $m=(a+b)/2$.
2. Keep the half interval that preserves sign change.
3. Repeat until interval width or residual is below tolerance.

Convergence is linear: interval width halves each iteration.

$$
|I_n| = \frac{|I_0|}{2^n}
$$

Professional interpretation:

- Strength: global reliability with minimal assumptions.
- Limitation: slow near final digits compared with Newton-type methods.

When safety dominates speed, bisection is often the first pass.

---

## 3.3 Newton-Raphson: Local Speed, Global Risk

Newton uses first-order local linearization:

$$
x_{n+1} = x_n - \frac{f(x_n)}{f'(x_n)}
$$

Near a simple root, convergence is typically quadratic, meaning error roughly squares each step.

$$
|e_{n+1}| \approx C |e_n|^2
$$

However, Newton can fail if:

1. Initial guess is poor.
2. Derivative is small or noisy.
3. Function has non-smooth structure.
4. Update jumps outside physically meaningful domain.

Professional use of Newton includes safeguards:

1. Step damping.
2. Domain clipping.
3. Derivative floor checks.
4. Fallback to bracketed updates when needed.

---

## 3.4 Secant and Hybrid Practice

Secant approximates the derivative using two recent iterates:

$$
x_{n+1} = x_n - f(x_n) \frac{x_n - x_{n-1}}{f(x_n)-f(x_{n-1})}
$$

It avoids explicit derivatives and is often superlinear in convergence (faster than bisection, usually slower than ideal Newton).

Practical reality in production workflows:

- No single method dominates all problems.
- Robust solvers combine bracketing safety with interpolation speed.

Hybrid mindset:

1. Bracket root first.
2. Attempt fast step (secant/newton/inverse quadratic).
3. Accept only if step is safe and progress is credible.
4. Otherwise fall back to bracket contraction.

This is the logic behind widely used methods such as Brent-style solvers.

---

## 3.5 Stopping Criteria and Verification

A professional root solver never stops on one condition alone.

Common stopping metrics:

1. Step size: $|x_{n+1}-x_n| < \tau_x$.
2. Residual size: $|f(x_n)| < \tau_f$.
3. Bracket width: $|b-a| < \tau_b$.
4. Iteration cap: $n \le n_{\max}$.

Why this matters:

- Small residual alone can be misleading for very flat functions.
- Small step alone can be misleading if stagnation occurs away from root.
- Tight tolerance without scale awareness can waste computation.

Recommended practical rule:

1. Use absolute + relative tolerance for $x$.
2. Use residual tolerance scaled to model units.
3. Require at least two criteria simultaneously.
4. Log final metrics for auditability.

---

## 3.6 Core Case Study: Finite Square Well

For a 1D finite square well, bound states are determined by transcendental equations from continuity and boundary matching. For odd parity (in one normalized form), one encounters equations like:

$$
-k \cot(k) = \sqrt{\alpha^2 - k^2}
$$

with $0 < k < \alpha$ and singularities from $\cot(k)$.

Professional solution workflow:

1. Plot both sides or equivalent residual first.
2. Identify admissible intervals between singularities.
3. Build valid brackets around each expected state.
4. Use a safe method (bisection/hybrid) to isolate roots.
5. Convert roots to energies and verify physical ordering.

This is where Chapter 2 principles become operational: finite precision, sensitivity, and stopping criteria determine whether the computed spectrum is trustworthy.

---

## Summary

Chapter 3 reframes root finding as methodological design, not just formula application.

Key professional takeaways:

1. Safety and speed are distinct properties.
2. Method selection is problem-dependent.
3. Stopping criteria are part of scientific validity.
4. Physical interpretation must close the loop after convergence.

Chapter 4 will extend this mindset from root location to local approximation and interpolation, where we trade model evaluations for surrogate structure.

---

## References

1. Burden, R. L., and Faires, J. D. Numerical Analysis. Brooks/Cole.
2. Quarteroni, A., Sacco, R., and Saleri, F. Numerical Mathematics. Springer.
3. Press, W. H., et al. Numerical Recipes. Cambridge University Press.
4. Heath, M. T. Scientific Computing. McGraw-Hill.
5. Trefethen, L. N., and Bau, D. Numerical Linear Algebra. SIAM.