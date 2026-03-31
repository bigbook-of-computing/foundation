# **Chapter 2: Computational Numbers**

---

# **Introduction**

In theoretical physics, we operate in the realm of **Real Numbers** ($\mathbb{R}$)—an infinite, continuous continuum where values like $\pi$ or $\sqrt{2}$ possess arbitrary precision. However, as we step into the "Digital Lab," we must confront a fundamental reality: the computer is a finite machine. It does not possess an infinite ruler; it possesses a digital one with discrete, non-uniform gaps.

This discrepancy between the continuous nature of physical laws and the discrete nature of digital hardware is the primary source of **numerical error**. This chapter deconstructs the "Digital Ruler," introducing the **IEEE 754 Floating-Point Standard** and building a rigorous framework for understanding, classifying, and mitigating the errors that arise from finite precision. Mastering these concepts is the "safety manual" for computational science; without it, even the most sophisticated simulation is prone to "catastrophic cancellation" and numerical instability.

---

# **Chapter 2: Outline**

| **Sec.** | **Title** | **Core Ideas & Examples** |
| :--- | :--- | :--- |
| **2.1** | **The Digital Ruler (IEEE 754)** | Sign, Exponent, and Mantissa; scientific notation in binary; why $0.1 + 0.2 \neq 0.3$. |
| **2.2** | **Machine Precision ($\epsilon_m$)** | The "Planck length" of computation; the gap between $1.0$ and the next representable number; calculating $\epsilon_m$. |
| **2.3** | **Round-off vs. Truncation Error** | Hardware limits (round-off) vs. algorithmic approximations (truncation); the Taylor series trade-off. |
| **2.4** | **Catastrophic Cancellation** | Subtracting nearly equal numbers; loss of significance; the quadratic formula trap. |
| **2.5** | **Numerical Stability** | Error propagation in iterative loops; stable vs. unstable algorithms; the recurrence relation case study. |

---

## **2.1 The Digital Ruler: IEEE 754 Standard**

---

To represent a vast range of physical scales—from the radius of a proton ($10^{-15}$ m) to the size of the observable universe ($10^{26}$ m)—computers use **floating-point arithmetic**. This is essentially binary scientific notation:

$$ \text{Value} = (-1)^s \times (1.f) \times 2^{E - \text{bias}} $$

In the standard 64-bit **double precision** (`float64`) format, the bits are allocated to balance range and precision:

```mermaid
bit-field
  0-0: "Sign (1 bit)"
  1-11: "Exponent (11 bits)"
  12-63: "Mantissa/Fraction (52 bits)"
```

!!! tip "The 0.1 + 0.2 Trap"
    Many decimal numbers, like $0.1$, cannot be represented exactly in binary (much like $1/3$ cannot be represented exactly in decimal). In a computer, $0.1$ is stored as a slightly larger value. This is why `0.1 + 0.2` results in `0.30000000000000004` rather than exactly `0.3`.

---

## **2.2 Machine Precision ($\epsilon_m$)**

---

Because the mantissa has a finite number of bits (52), there is a smallest possible change that a computer can record. This is **Machine Epsilon** ($\epsilon_m$), defined as the smallest positive number that, when added to $1.0$, yields a result distinguishable from $1.0$.

$$ \epsilon_m = 2^{-52} \approx 2.22 \times 10^{-16} $$

!!! example "Finding $\epsilon_m$ via Algorithm"
    You can measure the resolution of your own digital ruler using a simple iterative loop:
    ```python
    eps = 1.0
    while (1.0 + eps/2.0) > 1.0:
        eps /= 2.0
    print(f"Machine Epsilon: {eps}")
    ```

---

## **2.3 Round-off and Truncation Errors**

---

It is critical to distinguish between errors caused by the hardware and errors caused by our math.

1.  **Round-off Error:** Caused by the finite precision of the `float64` representation. It occurs every time a number is stored or an arithmetic operation is performed.
2.  **Truncation Error:** Caused by approximating an infinite mathematical process with a finite one. For example, using a few terms of a Taylor series to approximate $\sin(x)$ or using discrete steps to approximate a derivative.

??? question "Can we eliminate error by using more bits?"
    While "quadruple precision" (128-bit) reduces round-off error, it does not eliminate it, and it significantly slows down computation. Furthermore, it does nothing to solve **truncation error**, which is a property of the algorithm, not the hardware.

---

## **2.4 Catastrophic Cancellation**

---

The most dangerous error in computational physics is **catastrophic cancellation**. This occurs when two nearly equal numbers are subtracted. The leading identical digits cancel out, leaving only the "garbage" bits in the lower-order mantissa as the result.

!!! example "The Quadratic Formula Trap"
    Consider $x^2 + 10^8x + 1 = 0$. The standard formula $x = \frac{-b + \sqrt{b^2-4ac}}{2a}$ involves subtracting $\sqrt{b^2-4ac}$ (which is very close to $b$) from $b$. This leads to a massive loss of precision.
    
    **Numerical Fix:** Compute the "safe" root first: $x_1 = \frac{-b - \text{sgn}(b)\sqrt{b^2-4ac}}{2a}$, then find the second root using the identity $x_1 x_2 = c/a$.

---

## **2.5 Numerical Stability**

---

An algorithm is **stable** if small errors (like round-off) are dampened over time. It is **unstable** if those errors are amplified, eventually overwhelming the true physical solution.

### **Case Study: The Golden Ratio Recurrence**
Consider the sequence $x_n = \phi^n$ where $\phi = (\sqrt{5}-1)/2$. Mathematically, this follows $x_{n+1} = x_{n-1} - x_n$.
- **Theory:** The values should decrease toward zero ($0.618 \dots^n$).
- **Reality:** Because of initial round-off, an "unphysical" growing component $(\phi+1)^n$ is seeded. After $\sim 40$ iterations, the result explodes to infinity, producing total nonsense.

---

## **Summary: Computational vs. Mathematical Reality**

---

| Feature | Mathematical Reals ($\mathbb{R}$) | Computational Floats (`float64`) |
| :--- | :--- | :--- |
| **Precision** | Infinite | Terminated at 16 decimal digits |
| **Continuity** | Perfect continuum | Discrete gaps ("Gappy Ruler") |
| **Associativity** | $(a+b)+c = a+(b+c)$ | **Not guaranteed** due to rounding |
| **Operations** | Exact | Probabilistic noise in the 16th digit |
| **Failure Modes** | None | Overflow (`inf`), Underflow, `NaN` |

---

## **References**

---

[1] Goldberg, D. (1991). What Every Computer Scientist Should Know About Floating-Point Arithmetic. *ACM Computing Surveys*.

[2] Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*. SIAM.

[3] IEEE Computer Society. (2008). *IEEE Standard for Floating-Point Arithmetic (IEEE 754-2008)*.

[4] Trefethen, L. N., & Bau, D. (1997). *Numerical Linear Algebra*. SIAM.

[5] Muller, J. M., et al. (2018). *Handbook of Floating-Point Arithmetic*. Birkhäuser.