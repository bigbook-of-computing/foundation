# **Introduction**

Our computational journey through **Volume I** has been fundamentally rooted in the **deterministic** world. Our core solvers (ODEs, PDEs, and Linear Algebra, Chapters 7–14) are governed by strict mathematical rules where the same input **must** produce the same output.

However, a huge and fundamental part of the physical universe is **not** deterministic; it is inherently **stochastic** (driven by random chance) and **probabilistic** (described by distributions, not single values).

**Physical Examples of Stochastic Systems:**

* **Statistical Mechanics:** The individual trajectory of a single gas molecule is chaotic and random; its ensemble properties (like speed and energy) are described by a **distribution** (e.g., the Maxwell–Boltzmann distribution).
* **Quantum Mechanics:** The act of measuring a quantum state (e.g., photon emission) is fundamentally **probabilistic**.
* **Brownian Motion:** The seemingly chaotic path of a pollen grain is the macroscopic result of countless **random collisions** (a random walk).

Our deterministic solvers fail entirely in these domains. We cannot model the random path of a molecule using RK4, nor can we calculate a statistical average by simply integrating the average of the distribution. The only way to simulate these systems is to introduce the final, crucial pillar of computation: **Randomness**. We must develop a method to simulate **chance** itself and use it to **sample** from the statistical distributions that govern these stochastic systems [3].

# **Chapter 17: Outline**

| Sec.     | Title                           | Core Ideas & Examples                                           |
| :------- | :------------------------------ | :-------------------------------------------------------------- |
| **17.1** | Pseudo-Random Number Generation | PRNGs, “seed”, LCG, Mersenne Twister.                           |
| **17.2** | The Random Walk                 | $\Delta x \propto \sqrt{t}$, link to diffusion (Heat Equation). |
| **17.3** | Monte Carlo Integration         | Curse of Dimensionality, Error $\propto 1/\sqrt{N}$.            |
| **17.4** | Summary & Bridge                | The three pillars of computation, bridge to Volume II.          |

---

## **17.1 The Digital Die: Pseudo-Random Number Generation (PRNG)**

The initial challenge is philosophical: a computer, by design, is a deterministic machine. It cannot, by definition, throw a truly random, non-repeatable digital die. The solution is the **Pseudo-Random Number Generator (PRNG)**.

A PRNG is a **deterministic algorithm** that produces a sequence of numbers that appears random, passes stringent statistical tests for randomness, and yet is fully reproducible given its starting value, or **seed** [1]. This reproducibility is essential for the scientific process, allowing simulations to be verified and debugged.

??? question "Why is a *reproducible* random number useful?"
    If a complex simulation (like a galaxy merger) fails due to a random fluctuation, a *truly* random number would make the bug impossible to reproduce. A PRNG’s **seed** acts like a “save state.” By re-using the same seed, we can re-run the *exact same* sequence of “random” events to find and fix the bug.
    
---

### **The Linear Congruential Generator (LCG)**

Historically, the simplest and most famous PRNG is the **Linear Congruential Generator (LCG)** [1]. It generates a new random number $r_{n+1}$ from the previous one $r_n$ using a modular arithmetic formula:

$$
r_{n+1} = (a r_n + c) \bmod m
$$

where $a$ (multiplier), $c$ (increment), and $m$ (modulus) are large, carefully chosen integer constants. The quality of the sequence (its period and statistical properties) depends entirely on the choice of these constants.

```python
# Algorithm: Linear Congruential Generator (LCG)

class LCG:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        """
        Initialize a Linear Congruential Generator.

        Parameters:
        seed: initial seed value
        a: multiplier (default: 1664525)
        c: increment (default: 1013904223)
        m: modulus (default: 2^32)
        """
        self.a = a
        self.c = c
        self.m = m
        self.r_n = seed

    def get_next_random_int(self):
        self.r_n = (self.a * self.r_n + self.c) % self.m
        return self.r_n

    def get_next_random_float(self):
        return self.get_next_random_int() / self.m

## Example Monte Carlo simulation

import random

def monte_carlo_pi(num_samples):
    inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1

    return (inside_circle / num_samples) * 4
```

```python
## Algorithm: 1D Random Walk

import random

def random_walk_1d(N_steps=1000):
    """
    Simulate a 1D random walk.

    Parameters:
    N_steps: number of steps to take

    Returns:
    path: list of positions at each step
    """
    x = 0
    path = [x]

    for i in range(N_steps):
        r = random.random()

        if r < 0.5:
            x = x + 1
        else:
            x = x - 1

        # Store x in the array to plot the path
        path.append(x)

    return path
```

!!! example "Brownian Motion"
    The “drunken walk” of a pollen grain in water, first observed by Robert Brown, is the quintessential random walk. The grain isn’t moving on its own; it’s being “kicked” by countless, invisible water molecules. Our PRNG rule `if r < 0.5` simulates a single “kick” from this random thermal environment.
    
---

## **17.3 Core Application: Monte Carlo Integration**

The true power of pseudo-random numbers is realized in **Monte Carlo Integration**, which is essential for solving high-dimensional problems where grid-based methods (quadrature, Chapter 6) fail [1, 3].

Monte Carlo integration solves the problem of the **Curse of Dimensionality** by averaging function values sampled randomly over a domain, rather than sampling on a fixed grid.

The integral $I$ is approximated by:

$$
I \approx V \cdot \langle f \rangle
= V \cdot \frac{1}{N} \sum_{i=1}^N f(\mathbf{x}_i)
$$

The statistical error:

$$
\text{Error} \propto \frac{1}{\sqrt{N}}
$$

This scaling is **independent of dimension**.

!!! tip "Defeating the Curse of Dimensionality"
    A 10D grid with only 10 points per axis requires
    **$10^{10}$ function evaluations** — impossible.
    
    Monte Carlo with N = 10,000 samples achieves workable accuracy.
    The error depends only on 1/√N, not on dimensionality.
    
    
    ```mermaid
    flowchart TD
        A[Start: need I = ∫ f(x) dx] --> B[Initialize sum = 0, N = 10000]
        B --> C{Loop i = 1 to N}
        C --> D[Generate random point x_i]
        D --> E[Compute f(x_i)]
        E --> F[sum = sum + f(x_i)]
        F --> C
        C -->|Done| G[Compute average ⟨f⟩ = sum / N]
        G --> H[Compute domain volume V]
        H --> I[Approximation I ≈ V ⟨f⟩]
    
---

## **17.4 Chapter Summary and Bridge to Volume II**

This final chapter of **Volume I** completes the foundational computational toolkit. The three indispensable pillars of computational physics are now established:

1. **Deterministic Solvers:** ODEs, PDEs, and Linear Algebra (Chapters 7–14).
2. **Data-Driven Analysis:** FFT, SVD, and PCA (Chapters 15–16).
3. **Stochastic Modeling:** Pseudo-Random Numbers and Monte Carlo methods (Chapter 17).

This final pillar is the explicit **on-ramp to Volume II: Modeling Complex Systems**. The core of statistical mechanics is governed by high-dimensional integrals (e.g., the partition function) and sampling from distributions (like the Boltzmann distribution). The **Metropolis Algorithm**, centerpiece of Volume II, is a sophisticated random walk designed to efficiently sample these distributions—built directly upon the PRNG and stochastic tools introduced in this chapter.

---

## **References**

[1] Press, W. H., Teukolsky, S. A., Vetterling, W. T., & Flannery, B. P. (2007). *Numerical Recipes: The Art of Scientific Computing* (3rd ed.). Cambridge University Press.

[2] L’Ecuyer, P. (1998). *Random Number Generation*. Monte Carlo Methods and Applications.

[3] Landau, D. P., & Binder, K. (2009). *A Guide to Monte Carlo Simulations in Statistical Physics* (3rd ed.). Cambridge University Press.

[4] Newman, M. (2013). *Computational Physics*. CreateSpace Independent Publishing Platform.

[5] Garcia, A. L. (2000). *Numerical Methods for Physics* (2nd ed.). Prentice Hall.