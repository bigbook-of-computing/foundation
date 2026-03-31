# **Chapter 2: Precision, Error, and Numerical Judgment () () (Workbook)**

---

## Workbook Purpose

This workbook is for active participation and interview-style reasoning.

By the end of this chapter, you should be able to:

1. Explain why floating-point values are approximations.
2. Estimate and interpret machine-level precision limits.
3. Distinguish round-off, truncation, and conditioning.
4. Diagnose cancellation risk in formulas.
5. Defend numerically stable design choices.

---

## Part A: Concept Quiz

!!! note "Quiz 1"
```
The main reason `0.1 + 0.2 != 0.3` exactly in binary floating-point is:

- A. Python parser bug
- B. Decimal fractions like 0.1 are often non-terminating in base 2
- C. CPU cannot add numbers
- D. Matplotlib formatting issue

```
!!! note "Quiz 2"
```
Machine epsilon is best interpreted as:

- A. The maximum error in any computation
- B. The smallest positive representable number
- C. The smallest distinguishable relative increment near 1.0
- D. A hardware temperature coefficient

```
!!! note "Quiz 3"
```
Which is an algorithmic approximation error?

- A. Round-off error from finite mantissa
- B. Truncation from finite-difference derivatives
- C. Underflow to zero
- D. Overflow to infinity

```
!!! note "Quiz 4"
```
Catastrophic cancellation is most likely when:

- A. Multiplying large numbers
- B. Dividing by powers of ten
- C. Subtracting nearly equal numbers
- D. Sorting arrays

```
!!! note "Quiz 5"
```
A problem is ill-conditioned when:

- A. Inputs are measured in SI units
- B. Small input perturbations cause large output changes
- C. The algorithm is vectorized
- D. The plot uses a log axis

```
---

## Part B: Interview-Style Questions

Answer in 5 to 10 sentences each.

1. Why is “numerically stable” not equivalent to “mathematically correct”?
2. Describe a workflow to detect whether observed error comes from truncation or round-off.
3. Explain how conditioning and algorithmic stability interact.
4. Give one real scientific scenario where silent floating-point assumptions could cause wrong conclusions.
5. How would you communicate numerical uncertainty to non-specialist stakeholders?

---

## Part C: Guided Labs

### Lab 1: Representation and Machine Epsilon

Goal: inspect finite precision directly.

```python
import numpy as np

eps = np.finfo(np.float64).eps
print("Machine epsilon:", eps)
print("1 + eps > 1 ?", (1.0 + eps) > 1.0)
print("1 + eps/2 > 1 ?", (1.0 + eps / 2.0) > 1.0)
print("0.1 stored as:", format(np.float64(0.1), ".55f"))
```
**Sample Output:**
```python
Machine epsilon: 2.220446049250313e-16
1 + eps > 1 ? True
1 + eps/2 > 1 ? False
0.1 stored as: 0.1000000000000000055511151231257827021181583404541015625
```


Reflection:

- Why does the second boolean return False?
- What does the long decimal expansion of 0.1 tell you?

### Lab 2: Gap Growth Across Magnitude

Goal: verify nonuniform absolute spacing.

```python
import numpy as np

values = [1.0, 1e3, 1e8, 1e12, 1e16]
for x in values:
    next_x = np.nextafter(x, np.inf)
    abs_gap = next_x - x
    rel_gap = abs_gap / x
    print(f"x={x:>10.1e} abs_gap={abs_gap:>10.3e} rel_gap={rel_gap:>10.3e}")
```
**Sample Output:**
```python
x=   1.0e+00 abs_gap= 2.220e-16 rel_gap= 2.220e-16
x=   1.0e+03 abs_gap= 1.137e-13 rel_gap= 1.137e-16
x=   1.0e+08 abs_gap= 1.490e-08 rel_gap= 1.490e-16
x=   1.0e+12 abs_gap= 1.221e-04 rel_gap= 1.221e-16
x=   1.0e+16 abs_gap= 2.000e+00 rel_gap= 2.000e-16
```


Reflection:

- Which trend changes with magnitude, absolute or relative gap?

### Lab 3: Cancellation Stress Test

Goal: observe loss of significance.

```python
import numpy as np

x = np.float64(1e8)
deltas = np.logspace(-2, -12, 11)

for d in deltas:
    computed = (x + d) - x
    rel_err = abs(computed - d) / d
    print(f"delta={d:.1e} computed={computed:.1e} rel_err={rel_err:.2e}")
```
**Sample Output:**
```python
delta=1.0e-02 computed=1.0e-02 rel_err=5.36e-07
delta=1.0e-03 computed=1.0e-03 rel_err=2.03e-06
delta=1.0e-04 computed=1.0e-04 rel_err=1.69e-05
delta=1.0e-05 computed=1.0e-05 rel_err=1.32e-04
delta=1.0e-06 computed=1.0e-06 rel_err=1.62e-03
delta=1.0e-07 computed=1.0e-07 rel_err=4.31e-02
delta=1.0e-08 computed=1.5e-08 rel_err=4.90e-01
delta=1.0e-09 computed=0.0e+00 rel_err=1.00e+00
delta=1.0e-10 computed=0.0e+00 rel_err=1.00e+00
delta=1.0e-11 computed=0.0e+00 rel_err=1.00e+00
delta=1.0e-12 computed=0.0e+00 rel_err=1.00e+00
```


Reflection:

- At what scale does the recovered delta become unreliable?

---

## Part D: Participation Project

### Project Title

Numerical Reliability Report: Representation, Spacing, and Cancellation

### Objective

Produce a concise student report demonstrating three error mechanisms with evidence.

### Required Deliverables

1. One notebook with all experiments and explanations.
2. Two plots saved to chapter assets:
   - `codes/ch2_gap_scaling.png`
   - `codes/ch2_cancellation_error.png`
3. A one-page interpretation section answering:
   - What did you measure?
   - What failed and why?
   - What mitigation would you use in production code?

### Evaluation Rubric (20 points)

- Correct experiment design (6)
- Quality of analysis narrative (6)
- Plot quality and interpretability (4)
- Reproducibility discipline (4)

---

## Part E: Self-Check Answers

!!! success "Quiz Key"
    1. B
    2. C
    3. B
    4. C
    5. B

---

## Exit Ticket

Before Chapter 3, confirm:

- I can explain why floating-point is approximate.
- I can measure machine-scale precision behavior.
- I can identify cancellation-prone formulas.
- I can justify stable alternatives in writing.