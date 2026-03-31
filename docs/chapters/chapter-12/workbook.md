# **Chapter 12: Hyperbolic PDEs (e.g., The Wave Equation) (Workbook)**

### 12.1 Chapter Opener: The Physics of "Propagation"

> Summary: Wave phenomena are governed by **Hyperbolic PDEs** which feature a **second-order time derivative** ($\frac{\partial^2 y}{\partial t^2}$), enabling **propagation** without the dissipation that defines the diffusion processes of Chapter 11.

Our previous work categorized dynamic phenomena into two types: **Elliptic PDEs** (Chapter 10) gave us static equilibrium, and **Parabolic PDEs** (Chapter 11) modeled **diffusion**—systems that smooth out irregularities over time.

This chapter introduces the physics of **waves**, which are distinct because they **propagate** energy through space while, ideally, **retaining** their original shape without dissipation.

**Physical Examples of Wave Propagation:**
* **Mechanical Vibrations:** The motion of a guitar string or a drum head.
* **Fluid Dynamics:** Surface ripples on a pond.
* **Electromagnetism:** The propagation of light, where the field components are governed by the wave equation.

**The "Problem": The Hyperbolic PDE**

These propagation phenomena are governed by **Hyperbolic PDEs**. The classic example is the **1D Wave Equation** for displacement $y(x, t)$:

$$\frac{\partial^2 y}{\partial t^2} = v^2 \frac{\partial^2 y}{\partial x^2}$$

The key difference from the Heat Equation (Chapter 11) is the **second-order time derivative** ($\frac{\partial^2 y}{\partial t^2}$). Because of this, we need *two* initial conditions to start the simulation:
1.  The initial **position** or shape: $y(x, 0)$.
2.  The initial **velocity**: $\frac{\partial y}{\partial t} (x, 0)$.

---

### 12.2 Method 1: The "Verlet" of PDEs: The FTCS Algorithm

> Summary: The Wave Equation is discretized using the **Central Difference stencil** for *both* time and space, resulting in an explicit recurrence relation structurally identical to the **Verlet algorithm** (Chapter 8).

To solve the Wave Equation numerically, we apply the **Finite Difference Method (FDM)**, replacing all continuous derivatives with algebraic stencils. We use the preferred **Central Difference stencil** (Chapter 5) for both the time and space derivatives to maintain second-order accuracy.

**Discretization of Derivatives:**
* **Time ($\frac{\partial^2 y}{\partial t^2}$):** $\frac{y_{i, n+1} - 2y_{i, n} + y_{i, n-1}}{h_t^2}$
* **Space ($\frac{\partial^2 y}{\partial x^2}$):** $\frac{y_{i+1, n} - 2y_{i, n} + y_{i-1, n}}{h_x^2}$

**The Recurrence Relation:**
Substituting these into the Wave Equation and solving for the future state, $y_{i, n+1}$, yields the explicit FDM recurrence relation:

$$y_{i, n+1} = 2y_{i, n} - y_{i, n-1} + \left( \frac{v h_t}{h_x} \right)^2 \left[ y_{i+1, n} - 2y_{i, n} + y_{i-1, n} \right]$$

**Connection to Verlet:**
This equation is structurally identical to the **Verlet algorithm** (Chapter 8): $x_{n+1} = 2x_n - x_{n-1} + h^2 a_n$. Here, the term $\left[ y_{i+1, n} - 2y_{i, n} + y_{i-1, n} \right]$ represents the **curvature** (the Laplacian, Chapter 5), which is the source of the acceleration of the string.

---

### 12.3 The "Speed Limit": The CFL Condition

> Summary: The explicit FDM scheme for the Wave Equation is **conditionally stable**, requiring the **Courant Number ($C = \frac{v h_t}{h_x}$)** to be less than or equal to one. Violating this **CFL condition** causes the numerical solution to explode.

This explicit scheme is subject to a severe **conditional stability** constraint, similar to the one we found for the FTCS Heat Equation solver in Chapter 11.

**The Courant Number ($C$):**
The stability is controlled by the **Courant Number**, $C$, which compares the **physical distance** the wave travels in one time step ($v h_t$) to the **spatial size** of a grid box ($h_x$):

$$C = \frac{v h_t}{h_x}$$

**The CFL Stability Condition:**
The algorithm will only produce a stable solution if:
$$\mathbf{C} = \frac{v h_t}{h_x} \le 1$$

**Physical Meaning:**
This **Courant–Friedrichs–Lewy (CFL) condition** states that **information cannot be allowed to travel more than one spatial grid box per time step**. If $C>1$, the physical wave "jumps over" points in the numerical grid, leading to catastrophic numerical instability and an explosion of the solution.

---

### 12.4 The "First Step" Problem

> Summary: The two-step recurrence relation requires $y_{i, n-1}$ to begin. The missing initial profile is found by using a Central Difference approximation for the **initial velocity** condition ($\frac{\partial y}{\partial t} (x, 0)$).

The Wave Equation recurrence relation is a **two-step algorithm**, meaning it requires the displacement at two previous time levels ($y_{i, n}$ and $y_{i, n-1}$) to calculate the future state $y_{i, n+1}$.

**The Missing Profile:** At the initial time ($n=0$), we know $y_{i, 0}$ (the starting position) and the initial velocity, $v_{i, 0} = \frac{\partial y}{\partial t} (x_i, 0)$. However, the relation needs the displacement at $y_{i, -1}$, which is unknown.

**The Solution:** We solve for the first step ($y_{i, 1}$) by approximating the initial velocity ($v_{i, 0}$) using a **Central Difference in time** centered at $t=0$:

$$v_{i, 0} \approx \frac{y_{i, 1} - y_{i, -1}}{2 h_t}$$

Solving for $y_{i, -1}$ and substituting the result into the general recurrence relation yields a special, one-time formula for the first time step:

$$y_{i, 1} = y_{i, 0} + h_t v_{i, 0} + \frac{C^2}{2} (y_{i+1, 0} - 2y_{i, 0} + y_{i-1, 0})$$

After this first step, the simulation uses $y_{i, 0}$ and $y_{i, 1}$ to drive the general recurrence relation for all subsequent steps ($n \ge 1$).

---

### 12.5 Core Application: The "Plucked" Guitar String

> Summary: The **"Plucked String"** models a string fixed at both ends (Dirichlet BCs) and released from an initial shape (IVP). The simulation yields harmonics (standing waves) and demonstrates the conservation of energy inherent in the scheme.

The classic application of the Wave Equation is simulating a vibrating string (like a guitar string). This is a perfect example of a **BVP/IVP hybrid**.

**Conditions:**
* **Boundary Conditions (BVP):** Fixed ends (Dirichlet): $y(0, t) = 0$ and $y(L, t) = 0$.
* **Initial Conditions (IVP):** The string is "plucked" into a non-zero, usually **triangular shape** ($y(x, 0)$) and released **from rest** (zero initial velocity: $v(x, 0) = 0$).

**Computational Strategy:**
1.  **First Step:** The special first-step formula is used to get $y_{i, 1}$. Since $v_{i, 0}=0$, the term $h_t v_{i, 0}$ vanishes.
2.  **Time March:** The main FTCS recurrence relation is used for all subsequent steps.
3.  **Analysis:** The simulation demonstrates the principle of wave superposition. The initial displacement breaks into two waves that propagate away from the pluck point, reflect off the fixed boundaries, and interfere to create the **standing wave patterns** (the harmonics) that define the sound of the string.

---

# **Chapter 12: and Project Questions () () (Workbook)**

#### Quiz Questions

**1. What is the fundamental difference between the Heat Equation (Chapter 11) and the Wave Equation?**

* a) The Heat Equation is solved with FDM; the Wave Equation is solved with RK4.
* b) The Heat Equation models **diffusion** ($\frac{\partial T}{\partial t}$); the Wave Equation models **propagation** ($\frac{\partial^2 y}{\partial t^2}$). (**Correct**)
* c) The Wave Equation is unconditionally stable.
* d) The Heat Equation only requires one initial condition.

**2. The FDM recurrence relation for the Wave Equation is structurally identical to which other integrator from this volume?**

* a) Euler's Method.
* b) The RK4 Method.
* c) The **Verlet Algorithm**. (**Correct**)
* d) The Secant Method.

**3. The CFL stability condition for the Wave Equation, $C \le 1$, states that in one time step ($\Delta t$):**

* a) The Courant Number must be zero.
* b) The wave speed must be less than $v^2$.
* c) The numerical wave cannot travel more than **one spatial grid box ($\Delta x$)**. (**Correct**)
* d) The error must be less than $\mathcal{O}(h^4)$.

**4. The Wave Equation recurrence relation is a two-step algorithm. The missing initial profile ($y_{i, -1}$) is found by combining the initial position $y_{i, 0}$ with what other initial condition?**

* a) The final position $y_{i, L}$.
* b) The initial **velocity** ($v_{i, 0}$). (**Correct**)
* c) The acceleration $a_{i, 0}$.
* d) The Courant number $C$.

#### Interview-Style Question

**Question:** The FDM scheme for the Wave Equation is explicit and only $\mathcal{O}(h^2)$ accurate, yet it is often preferred over a high-order implicit scheme like Crank-Nicolson for wave simulation. Why might a lower-order, explicit method be a better choice for a wave problem?

**Answer Strategy:** The explicit FDM scheme for the wave equation is $\mathcal{O}(h^2)$ accurate and, crucially, is **non-dissipative** (it mimics the energy-conserving structure of the **Verlet algorithm**). Waves must conserve energy and retain their shape. Implicit methods (like Crank-Nicolson, Chapter 11) introduce numerical damping (dissipation), which would artificially **smooth out and dampen** the wave over time. Explicit methods, when stable, preserve the wave's amplitude and shape more faithfully over long distances.

# **Chapter 12: On Projects: Wave Propagation Dynamics () () (Workbook)**

**1. Project: The CFL Stability Catastrophe for Waves**
* **Problem:** Demonstrate the instability of the explicit wave scheme when the Courant number $C$ is violated.
* **Formulation:** Simulate a 1D string using the FTCS recurrence relation.
* **Tasks:**
    1.  Integrate the string with a stable $C=0.5$.
    2.  Integrate the string with an unstable $C=1.1$.
    3.  Plot the maximum displacement of the string over time for both cases.
    4.  The stable case should show bounded oscillation, while the unstable case should show exponential growth/explosion.

**2. Project: Simulating the Plucked String and Harmonics**
* **Problem:** Model the motion of a plucked guitar string and analyze its resulting frequency content (a preview of Chapter 15).
* **Formulation:** Set the initial position $y(x, 0)$ to a triangular profile and $v(x, 0) = 0$. Use the special "First Step" formula to start the simulation.
* **Tasks:**
    1.  Implement the full FTCS scheme including the two-part initialization process.
    2.  Integrate the simulation for a long time.
    3.  **Visualization:** Plot a sequence of snapshots of the string's profile over time, showing the propagation and reflection of the waves.
    4.  Extract the time series $y(t)$ for a single point (e.g., $x=L/4$).

**3. Project: The Effect of Initial Velocity**
* **Problem:** Analyze the difference between plucking a string (non-zero position, zero velocity) and striking a string (zero position, non-zero velocity).
* **Formulation:** Simulate the Wave Equation under the following initial conditions:
    1.  **Case A (Pluck):** $y(x, 0) = \text{Gaussian Peak}$, $\frac{\partial y}{\partial t} (x, 0) = 0$.
    2.  **Case B (Strike):** $y(x, 0) = 0$, $\frac{\partial y}{\partial t} (x, 0) = \text{Gaussian Peak}$.
* **Tasks:**
    1.  Implement both initial conditions and run the FTCS solver for each.
    2.  Compare the resulting wave propagation patterns. (Case B should immediately split into two outward-moving peaks).

**4. Project: Boundary Conditions - A Free End**
* **Problem:** Model a string that is fixed at $x=0$ ($y(0, t)=0$) but whose end at $x=L$ is **free** (a Neumann boundary condition, $\frac{\partial y}{\partial x}(L, t) = 0$).
* **Formulation:** The free boundary condition must be incorporated into the FTCS recurrence relation at the boundary node $i=N$. This is achieved by using an **imaginary point** $y_{N+1}$ such that $\frac{\partial y}{\partial x} \approx 0$ (e.g., $y_{N+1} = y_{N-1}$).
* **Tasks:**
    1.  Modify the FTCS loop to include a special update rule for the rightmost boundary node that uses the imaginary point condition.
    2.  **Visualization:** Simulate a wave moving toward the free boundary and show that it **reflects without inverting** its sign (unlike the fixed end, which inverts the wave).

---

### 12.6 Chapter Summary & Next Steps

> Summary: We've established the FDM-based recurrence relation for the **Hyperbolic PDE** (Wave Equation), noting its connection to the **Verlet algorithm**. We learned the explicit scheme is critically restricted by the **CFL stability condition** ($C \le 1$) and requires a special formula to handle the initial velocity condition.

**What We Built: The Wave Simulator**
* **The Engine:** The FDM yielded the **Verlet-like recurrence relation**, solved via explicit marching.
* **The Restriction:** We are bound by the **CFL condition**, which limits the time step based on the spatial resolution.

**Bridge to Part 5: The Language of Physics: Linear Algebra**

The solutions for nearly all advanced FDM problems (Chapters 9-12) inevitably converge on the same core requirement: **solving a system of linear equations**.

* **FDM on BVPs (Chapter 9):** Led to a tridiagonal matrix equation ($\mathbf{A}\mathbf{y} = \mathbf{b}$).
* **Implicit PDEs (Chapter 11):** Led to a tridiagonal system that must be solved at every time step.

We now shift our focus from **discretization** (Part 4) to **solution**. We have identified the problems; we must now build the core **Linear Algebra** algorithms—the engine room—to solve these massive, sparse systems efficiently. This begins with **Chapter 13: Systems of Linear Equations**.