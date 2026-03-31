# **Chapter 3: Root Finding for Scientific Reliability () () (Workbook)**

---

## Workbook Purpose

This workbook is designed for active, assessable participation.

By the end, you should be able to:

1. Translate physical constraints into root equations.
2. Compare bisection, Newton, and secant on safety and speed.
3. Select stopping criteria appropriate to scale and physics.
4. Diagnose and fix convergence failures.
5. Implement a mini root-finding study with reproducible evidence.

---

## Part A: Concept Quiz (Foundations)

!!! note "Quiz 1"
```
A bracketing method requires:

- A. A derivative function
- B. Two points with opposite signs in a continuous interval
- C. A second derivative
- D. A random initial guess

```
!!! note "Quiz 2"
```
Newton-Raphson is generally fast when:

- A. The initial guess is near a simple root and derivative is well-behaved
- B. The function is discontinuous
- C. The derivative is always zero
- D. No initial guess is provided

```
!!! note "Quiz 3"
```
Secant method is attractive because:

- A. It guarantees convergence globally
- B. It avoids explicit derivative evaluation
- C. It always outperforms Newton
- D. It needs only one iterate

```
!!! note "Quiz 4"
```
The most robust stopping design is:

- A. Residual-only criterion
- B. Iteration-count-only criterion
- C. Multi-condition criterion combining step, residual, and safeguards
- D. Stop after fixed wall-clock time

```
!!! note "Quiz 5"
```
Catastrophic cancellation is most related to:

- A. Multiplication overflow
- B. Subtracting nearly equal quantities
- C. FFT aliasing
- D. Integer truncation

```
---

## Part B: Concept Quiz (Professional Practice)

!!! note "Quiz 6"
```
A solver reports $|f(x)|$ very small, but $x$ is physically impossible. Best interpretation:

- A. Converged and valid
- B. Numerical convergence must still be checked against domain constraints
- C. Physics constraints are optional
- D. Residual always dominates physical checks

```
!!! note "Quiz 7"
```
If Newton diverges from a valid bracket, a practical response is:

- A. Increase iteration limit only
- B. Use damped or bracketed fallback steps
- C. Remove tolerance checks
- D. Assume model is wrong

```
!!! note "Quiz 8"
```
For reproducibility, the most important metadata includes:

- A. Plot colors only
- B. Hardware RGB profile
- C. Tolerances, initial guesses/brackets, iteration counts, and solver type
- D. Window size of IDE only

```
!!! note "Quiz 9"
```
In bisection, interval width after $n$ steps is:

- A. $|I_0| / n$
- B. $|I_0| / 2^n$
- C. $|I_0| \times n$
- D. Constant

```
!!! note "Quiz 10"
```
A root-finding method is numerically stable when:

- A. It amplifies tiny perturbations unpredictably
- B. It is fastest on one benchmark
- C. It tends to control and not explosively amplify perturbations
- D. It uses symbolic algebra only

```
---

## Part C: Interview-Style Questions

Answer each in 6 to 12 sentences.

1. Why should method selection be tied to model smoothness and derivative availability?
2. Explain the difference between algorithm failure and model failure in nonlinear solving.
3. Describe a strategy to detect false convergence in a root-finding report.
4. In safety-critical computation, when is slower bisection preferable to faster Newton?
5. How does Chapter 2 (floating-point limits) influence Chapter 3 stopping tolerance choices?

---

## Part D: Guided Lab 1 (Method Behavior)

### Objective

Compare convergence traces for bisection, Newton, and secant on:

$$
f(x) = \cos(x) - x
$$

### Setup Code

```python
import numpy as np


def f(x):
    return np.cos(x) - x


def df(x):
    return -np.sin(x) - 1.0
```

### Task

1. Implement bisection using bracket $[0,1]$.
2. Implement Newton using $x_0=0.5$.
3. Implement secant using $(x_0,x_1)=(0,1)$.
4. Record per-iteration: $x_n$, $|f(x_n)|$, and step size.
5. Compare iteration counts to hit $|f(x)| < 1e-12$.

### Reflection

- Which method converged fastest?
- Which method had strongest safety guarantee?
- How would you justify choice for production?

---

## Part E: Guided Lab 2 (Stopping Criteria Stress Test)

### Objective

Show why residual-only stopping is risky.

### Setup Function

```python
import numpy as np


def g(x):
    # Flat near root region to stress residual-only logic
    return (x - 1.0) ** 7
```

### Task

1. Use Newton-like updates or fixed-point updates to approach root near $x=1$.
2. Stop once with residual-only threshold.
3. Stop again with combined criteria:
   - $|f(x)| < 1e-10$
   - and $|x_{n+1} - x_n| < 1e-10$
4. Compare final $x$, final residual, and step size.

### Reflection

- Did residual-only stop too early or too late?
- What condition prevented false confidence?

---

## Part F: Guided Lab 3 (Finite Square Well Bracketing)

### Objective

Build physically meaningful brackets for odd-state roots.

### Residual Form

$$
R(k) = -k \cot(k) - \sqrt{\alpha^2-k^2}
$$

with $\alpha > 0$ and $0 < k < \alpha$.

### Task

1. Choose $\alpha=8.0$.
2. Identify singular points of $\cot(k)$.
3. Construct candidate intervals between singularities.
4. Evaluate sign changes to isolate valid brackets.
5. Solve each bracket with bisection or hybrid method.

### Reflection

- Why is pre-plotting essential before solving?
- Which intervals were invalid and why?

---

## Part G: Participation Project

### Project Title

Root-Finding Reliability Report for a Physical Residual

### Project Goal

Produce a comparative solver report that demonstrates method behavior, stopping logic, and physical interpretation.

### Required Deliverables

1. Notebook with complete workflow and narrative.
2. Two required figures in this chapter's codes folder:
   - `codes/ch3_method_convergence.png`
   - `codes/ch3_residual_landscape.png`
3. One comparative table:
   - solver
   - iterations
   - final root
   - final residual
   - termination reason
4. One short discussion (300 to 500 words) answering:
   - What failed in at least one method setup?
   - How was failure detected?
   - What mitigation did you apply?

### Technical Standards

- Include explicit tolerances and maximum iteration cap.
- Use at least two stopping criteria.
- Show at least one case where initial guess quality changes behavior.
- Keep all generated artifacts in this chapter only.

### Scoring Rubric (25 points)

- Correct solver implementation (8)
- Quality of convergence analysis (6)
- Stopping-criteria rigor (5)
- Physical interpretation quality (4)
- Reproducibility and clarity (2)

---

## Part H: Error Analysis Prompt

Write a short technical memo (200 to 300 words):

"If two teams report different roots for the same residual, what diagnostics would you run before concluding one team is wrong?"

Expected dimensions:

1. Numerical tolerance and stopping policy.
2. Initial guess or bracket dependence.
3. Floating-point sensitivity.
4. Residual scaling and conditioning.
5. Domain and physical constraints.

---

## Part I: Self-Check Answers

!!! success "Quiz Key"
    1. B
    2. A
    3. B
    4. C
    5. B
    6. B
    7. B
    8. C
    9. B
    10. C

---

## Exit Ticket

Before moving to Chapter 4, confirm:

- I can justify solver choice, not just run a formula.
- I can design robust stopping logic.
- I can detect divergence, stagnation, and false convergence.
- I can connect numerical roots back to physical meaning.