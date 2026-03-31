# **Chapter 8: Initial Value Problems II — The Leapfrog & Verlet () () (Workbook)**

### 8.1 Chapter Opener: The Problem of "Forever"

> Summary: For long-term conservative systems (like orbits), the $\mathcal{O}(h^4)$ RK4 method fails due to slow, accumulating energy drift. The solution is the **symplectic integrator**, which preserves the Hamiltonian geometry for infinite-term stability.

In Chapter 7, we established the **Runge–Kutta 4th Order (RK4)** integrator as the numerical masterpiece for short-term motion and systems that *lose* energy (dissipative systems). However, for systems that must **conserve** total energy (conservative systems, such as orbits, springs, and molecular dynamics simulations), RK4 is inadequate.

**The Problem: RK4 Energy Drift**

RK4, despite its high local accuracy ($\mathcal{O}(h^5)$ local error), does **not** respect the hidden symmetries of Hamiltonian physics. Every step introduces a tiny numerical imbalance; over millions of steps, these errors accumulate, causing the total energy ($E$) to slowly **drift** upward or downward.

* **Consequence:** A stable orbit spirals away, or a molecular box heats up for no physical reason, leading to a numerical "**heat death**".

**The Solution: Symplectic Integrators**

We adopt a new philosophy: sacrifice some short-term precision for long-term fidelity. **Symplectic integrators** are structure-preserving algorithms designed to conserve the **geometry of phase space** (the invariant area/volume of all possible states) dictated by Hamilton’s equations.

* **Energy Behavior:** Symplectic algorithms conserve a **shadow Hamiltonian** ($\tilde{H}$). This means the energy will gently **oscillate** about the true value but will **never drift away**.
* **Time Reversibility:** These methods are inherently **time-reversible**—running the simulation backward exactly recovers the initial state.

### Comprehension & Conceptual Questions

#### Quiz Questions

**1. Why does the RK4 method, despite its high local accuracy, fail to conserve total energy in a long-term simulation of a harmonic oscillator?**

* a) RK4 uses variable step sizes that cause numerical instability.
* b) RK4 is only a first-order accurate method.
* c) RK4 does **not** preserve the symplectic geometry of Hamiltonian systems, leading to accumulating error. (**Correct**)
* d) RK4 is too slow for millions of steps.

**2. How do symplectic integrators behave with respect to energy conservation over long time periods?**

* a) The energy slowly drifts away from the starting value.
* b) The energy is perfectly conserved to machine precision.
* c) The energy **oscillates** around the true mean value but remains **bounded**. (**Correct**)
* d) They systematically subtract energy, simulating friction.

#### Interview-Style Question

**Question:** Explain the difference between *accuracy per step* and *global stability* in numerical integration, using the "circle-drawing" analogy provided in the chapter.

**Answer Strategy:**
* **Accuracy (RK4):** RK4 focuses on *local precision*—making each small step as close as possible to the true analytical curve. However, because it breaks the inherent geometry, the accumulation of tiny errors causes the overall trajectory (the circle) to **drift** into a spiral.
* **Global Stability (Verlet):** Symplectic integrators sacrifice a little local precision (the steps might "wiggle") to focus on preserving the **structure** (the phase-space area). This structural conservation guarantees that the trajectory (the circle) remains **closed and bounded** forever.

### Hands-On Project

**Project: The Energy Drift Showdown (RK4 vs. Verlet)**

1.  **Formulation:** Simulate the simple harmonic oscillator ($x'' = -x$) using both RK4 and the **Velocity–Verlet** algorithm (to be implemented later).
2.  **Tasks:** Integrate from $t=0$ to a long time (e.g., $t=1000$) with a fixed step size.
3.  **Goal:** Plot the total energy $E(t)$ for both methods. The task is to visually observe RK4 energy *drifting* (showing instability) versus the Velocity–Verlet energy *oscillating* (showing long-term stability).

### 8.2 What is a "Symplectic" Integrator?

> Summary: Symplectic integrators preserve the **phase-space area** ($dx \wedge dp = \text{constant}$) dictated by **Hamilton’s equations** (Liouville’s Theorem), guaranteeing long-term stability by ensuring energy oscillations rather than secular drift.

**The Theory: Hamiltonian Geometry**

Conservative systems are governed by **Hamilton’s equations**, which define the state in **phase space** (position $x$ vs. momentum $p$). The total energy, or **Hamiltonian** ($H = \frac{p^2}{2m} + V(x)$), is conserved. More profoundly, **Liouville’s Theorem** states that the volume (or area) of any cluster of states in phase space must remain constant as the system evolves.

**The Symplectic Condition**

A **symplectic integrator** is designed to perfectly preserve this phase-space area.

* The algorithm evolves the system on a **shadow Hamiltonian** ($\tilde{H} = H + \mathcal{O}(h^2)$), a modified energy surface that is conserved for all time.
* This conservation of structure ensures that energy errors cancel out, preventing secular drift.

### 8.3 The "Birth" of MD: The (Störmer–)Verlet Algorithm

> Summary: The original Verlet algorithm is derived by **adding** the forward and backward Taylor expansions, canceling the odd-order terms ($v, b$), resulting in a simple, symplectic, $\mathcal{O}(h^2)$ update that only uses positions and acceleration.

The **Verlet algorithm** (1967) was born from the need for a cheap, simple, and stable integrator for **Molecular Dynamics (MD)**.

**The Derivation**

The core formula is found by **adding** the forward ($x(t+h)$) and backward ($x(t-h)$) Taylor expansions. This eliminates all the odd-power terms (velocity, jerk, etc.), leaving a symmetric, position-only update:

$$x(t + h) + x(t - h) = 2x(t) + h^2 a(t) + \mathcal{O}(h^4)$$

**The Formula**

$$\boxed{x_{n+1} = 2x_n - x_{n-1} + h^2 a_n + \mathcal{O}(h^4)}$$

* **Key Features:** It is $\mathcal{O}(h^2)$ accurate, time-reversible, and symplectic.
* **Limitation:** It does not explicitly calculate velocity $v(t)$, making kinetic energy calculations inconvenient.

### 8.4 The “Fix”: The Velocity–Verlet Algorithm

> Summary: Velocity–Verlet is a synchronized version of Verlet that updates $x$ and $v$ explicitly via a four-step **Kick–Drift–Kick** sequence. It is the modern $\mathcal{O}(h^2)$, symplectic workhorse of molecular dynamics.

The **Velocity–Verlet** algorithm is the most popular modern variant of Verlet because it calculates both position and velocity **synchronously** at every step.

**The Kick–Drift–Kick Sequence**

The update advances $x$ and $v$ from $t$ to $t+h$ in four steps:

1.  **Half-Kick:** Advance velocity by half a step using current acceleration $a_n$.
```
$$v_{n+\frac{1}{2}} = v_n + \frac{h}{2} a_n$$
```
2.  **Full Drift:** Advance position using the mid-step velocity $v_{n+\frac{1}{2}}$.
```
$$x_{n+1} = x_n + h \cdot v_{n+\frac{1}{2}}$$
```
3.  **New Acceleration:** Compute the new acceleration $a_{n+1}$ from the new position $x_{n+1}$.
```
$$a_{n+1} = \frac{F(x_{n+1})}{m}$$
```
4.  **Half-Kick:** Finish the velocity update using the new acceleration $a_{n+1}$.
```
$$v_{n+1} = v_{n+\frac{1}{2}} + \frac{h}{2} a_{n+1}$$

```
**Key Features:** Velocity–Verlet retains the $\mathcal{O}(h^2)$ accuracy, time-reversibility, and symplectic structure of the original Verlet method.

### 8.5 The “Other” Fix: The Leapfrog Algorithm

> Summary: Leapfrog is mathematically equivalent to Velocity–Verlet but maintains stability by intentionally **staggering** the position ($x_n$) and velocity ($v_{n+1/2}$) updates by half a time step.

The **Leapfrog algorithm** is a structural twin of Velocity–Verlet, often favored in astrophysics or charged-particle motion.

**The Staggered Rhythm**

It maintains synchronization by defining:
* Positions $x$ at **integer** times ($t_n, t_{n+1}, \dots$).
* Velocities $v$ at **half-integer** times ($t_{n+1/2}, t_{n+3/2}, \dots$).

**The Update Scheme**

1.  **Kick:** Advance velocity from $t_{n-1/2}$ to $t_{n+1/2}$ using the acceleration $a_n$ at the central position $x_n$.
```
$$v_{n+\frac{1}{2}} = v_{n-\frac{1}{2}} + h \cdot a_n$$
```
2.  **Drift:** Advance position from $t_n$ to $t_{n+1}$ using the new half-step velocity $v_{n+1/2}$.
```
$$x_{n+1} = x_n + h \cdot v_{n+\frac{1}{2}}$$

```
**Key Insight:** Leapfrog and Velocity–Verlet are **mathematically equivalent**; they simply express the same underlying symplectic mapping in different coordinate systems.

### 8.6 Core Application: An N-Body Planetary Simulation

> Summary: The **N-Body problem** is a fully coupled, nonlinear $\mathcal{O}(N^2)$ system that requires a symplectic integrator (like Velocity–Verlet) to conserve total energy and momentum, ensuring the orbits remain stable over cosmic timescales.

The **N-Body problem** (simulating the motion of $N$ masses under mutual gravity) has no general analytical solution and requires stable numerical integration.

**The Physics: Acceleration**

The acceleration ($\mathbf{a}_i$) on each body $i$ is the sum of gravitational forces from all other bodies $j$:
$$\mathbf{a}_i = G \sum_{j \neq i} m_j \frac{\mathbf{r}_{ij}}{|\mathbf{r}_{ij}|^3}$$

**The Computational Cost:** Computing all pairwise accelerations is an $\mathcal{O}(N^2)$ operation.

**Conservation Checks:** For verification, a symplectic integrator must show:
* **Total Energy ($E$):** Should **oscillate** with no secular drift.
* **Total Momentum ($\mathbf{P}$):** Should be perfectly conserved.

The stability of Velocity–Verlet ensures that these simulated orbits remain perfectly bound and balanced, unlike RK4, which causes orbits to spiral.

---

# **Chapter 8: Symplectic Integrators and Long-Term Dynamics () () (Workbook)**

**1. What is the main limitation of RK4 that motivates the use of symplectic integrators?**

* a) RK4 is too slow for real-time simulations.
* b) RK4 does not conserve total energy in Hamiltonian systems, causing secular drift. (**Correct**)
* c) RK4 is only first-order accurate.
* d) RK4 cannot handle vector systems.

**2. What mathematical property does a symplectic integrator preserve to ensure long-term stability?**

* a) The maximum position ($x_{\max}$).
* b) The phase-space area/volume. (**Correct**)
* c) The derivative $f'(x)$.
* d) The initial condition $x_0$.

**3. What is the order of accuracy of the basic Verlet algorithm?**

* a) $\mathcal{O}(h)$
* b) $\mathcal{O}(h^2)$ (**Correct**)
* c) $\mathcal{O}(h^4)$
* d) $\mathcal{O}(h^5)$

**4. How is the Verlet algorithm formula derived?**

* a) By subtracting the forward and backward Taylor expansions, canceling the even terms.
* b) By adding the forward and backward Taylor expansions, canceling the odd terms ($v, b$). (**Correct**)
* c) By using a high-order polynomial fit.
* d) By solving the $2 \times 2$ matrix system.

**5. Why is the Velocity–Verlet algorithm often preferred over the original Verlet algorithm?**

* a) It has a higher order of accuracy ($\mathcal{O}(h^4)$).
* b) It is non-symplectic, making it faster.
* c) It explicitly calculates both position ($x$) and velocity ($v$) synchronously at every step. (**Correct**)
* d) It only requires one initial guess.

**6. The Velocity–Verlet method is structured as a sequence of:**

* a) Predictor–Corrector–Averager.
* b) Forward–Centered–Backward.
* c) Kick–Drift–Kick (half-step velocity, full-step position, half-step velocity). (**Correct**)
* d) $\mathcal{O}(h^4)$ approximation, $\mathcal{O}(h^2)$ approximation.

**7. In the Leapfrog scheme, if $x_n$ is known at time $t_n$, at what time is the velocity $v$ known?**

* a) $t_n$ (synchronous)
* b) $t_{n+1}$ (ahead of time)
* c) $t_{n+1/2}$ (staggered by half a step) (**Correct**)
* d) $t_{n-1}$ (behind time)

**8. Which statement about the relationship between Leapfrog and Velocity–Verlet is true?**

* a) They have different accuracy orders.
* b) They are non-symplectic.
* c) They are mathematically equivalent, representing the same symplectic map with different variable timing. (**Correct**)
* d) Leapfrog is RK4, and Velocity–Verlet is RK2.

**9. For a three-body planetary simulation, what is the computational cost of the `get_accelerations` function per time step?**

* a) $\mathcal{O}(N)$
* b) $\mathcal{O}(N \log N)$
* c) $\mathcal{O}(N^2)$ (**Correct**)
* d) $\mathcal{O}(N^3)$

**10. What is the total energy of a conservative harmonic oscillator?**

* a) $E = \frac{p^2}{2m} + F(x)$
* b) $E = \frac{1}{2}v^2 + \frac{1}{2}x^2$ (**Correct**)
* c) $E = m \cdot x''$
* d) $E = x_n - x_{n-1}$

***