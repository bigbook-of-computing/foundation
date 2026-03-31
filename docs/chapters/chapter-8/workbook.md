# **Chapter 8: Initial Value Problems II (Workbook)**

---

> **Summary:** This workbook moves beyond simple accuracy to explore the **Geometry of Phase Space**. For long-term conservative systems (like planetary orbits), even high-order methods like RK4 fail due to secular energy drift. We introduce **Symplectic Integrators**—specifically the **Verlet** and **Leapfrog** families—which preserve the Hamiltonian structure, ensuring physical fidelity over infinite timescales.

---

## **8.1 The Problem of "Forever"** {.heading-with-pill}

> **Difficulty:** ★★★☆☆
> 
> **Concept:** Symplecticity vs. Absolute Accuracy
> 
> **Summary:** For systems that must conserve total energy, such as orbits or molecular dynamics, standard integrators suffer from "Numerical Heat Death." This section explains why $O(h^4)$ precision is secondary to structural preservation in long-term simulations.

### **Comprehension Check**

!!! note "Quiz"
    1. Why does the RK4 method, despite its high local accuracy, fail to conserve total energy in a long-term simulation of a harmonic oscillator?
    2. How do symplectic integrators behave with respect to energy conservation over long time periods?

??? info "See Answer"
    1. **RK4 does not preserve the symplectic geometry of Hamiltonian systems, leading to accumulating error.**
    2. **The energy oscillates around the true mean value but remains bounded.**

!!! abstract "Interview-Style Question"
    **Question:** Explain the difference between *accuracy per step* and *global stability* in numerical integration, using the "circle-drawing" analogy provided in the chapter.
    
    ???+ info "Answer Strategy"
        - **Accuracy (RK4):** RK4 focuses on *local precision*—making each small step as close as possible to the true analytical curve. However, because it breaks the inherent geometry, the accumulation of tiny errors causes the overall trajectory (the circle) to **drift** into a spiral.
        - **Global Stability (Verlet):** Symplectic integrators sacrifice a little local precision (the steps might "wiggle") to focus on preserving the **structure** (the phase-space area). This structural conservation guarantees that the trajectory (the circle) remains **closed and bounded** forever.

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

### **Comprehension Check**

!!! note "Quiz"
    1. What is the main limitation of RK4 that motivates the use of symplectic integrators?
    2. What mathematical property does a symplectic integrator preserve to ensure long-term stability?
    3. What is the order of accuracy of the basic Verlet algorithm?
    4. How is the Verlet algorithm formula derived?
    5. Why is the Velocity–Verlet algorithm often preferred over the original Verlet algorithm?
    6. The Velocity–Verlet method is structured as a sequence of:
    7. In the Leapfrog scheme, if $x_n$ is known at time $t_n$, at what time is the velocity $v$ known?
    8. Which statement about the relationship between Leapfrog and Velocity–Verlet is true?
    9. For a three-body planetary simulation, what is the computational cost of the `get_accelerations` function per time step?
    10. What is the total energy of a conservative harmonic oscillator?

??? info "See Answer"
    1. **RK4 does not conserve total energy in Hamiltonian systems, causing secular drift.**
    2. **The phase-space area/volume.**
    3. **$\mathcal{O}(h^2)$**.
    4. **By adding the forward and backward Taylor expansions, canceling the odd terms ($v, b$).**
    5. **It explicitly calculates both position ($x$) and velocity ($v$) synchronously at every step.**
    6. **Kick–Drift–Kick (half-step velocity, full-step position, half-step velocity).**
    7. **$t_{n+1/2}$ (staggered by half a step)**.
    8. **They are mathematically equivalent, representing the same symplectic map with different variable timing.**
    9. **$\mathcal{O}(N^2)$**.
    10. **$E = \frac{1}{2}v^2 + \frac{1}{2}x^2$**.

***