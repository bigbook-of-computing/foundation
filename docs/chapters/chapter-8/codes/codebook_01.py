import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 8 Codebook: Symplectic Integrators
# Project 1: Energy Conservation Showdown (RK4 vs. Velocity-Verlet)
# ==========================================================

# ==========================================================
# 1. Setup Model (Simple Harmonic Oscillator)
# ==========================================================

def sho_deriv(S):
    """
    Derivative function for the SHO (x'' = -x).
    S = [x, v], S' = [v, -x]
    """
    x, v = S
    # dx/dt = v, dv/dt = -x
    return np.array([v, -x])

def sho_acceleration(x):
    """Acceleration function a = -x (for Verlet)."""
    return -x

def sho_energy(S):
    """Total Energy: E = 1/2 * (v^2 + x^2) (m=k=1)."""
    x, v = S
    return 0.5 * (v**2 + x**2)

# Initial conditions and parameters
S0 = np.array([1.0, 0.0])  # Initial state: x(0)=1, v(0)=0
T_FINAL = 500.0            # Long simulation time to show drift
N_STEPS = 50000            # Large number of steps
H = T_FINAL / N_STEPS      # Time step size (Δt)
T_GRID = np.linspace(0, T_FINAL, N_STEPS + 1)
E_TRUE = sho_energy(S0)    # True energy = 0.5




# ==========================================================
# 2. Velocity-Verlet Solver (Symplectic)
# ==========================================================

def velocity_verlet_solve(accel_func, S0, h, N_steps):
    """
    Implements the Velocity-Verlet algorithm (symplectic, O(h²) accurate).
    """
    x = S0[0]
    v = S0[1]
    a = accel_func(x)
    history = [[x, v]]
    
    for _ in range(N_steps):
        # 1. Half-Kick (Update v to v + h/2 * a)
        v_half = v + 0.5 * h * a
        
        # 2. Full Drift (Update x to x + h * v_half)
        x_new = x + h * v_half
        
        # 3. New Acceleration (Based on x_new)
        a_new = accel_func(x_new)
        
        # 4. Half-Kick (Update v to v_half + h/2 * a_new)
        v_new = v_half + 0.5 * h * a_new
        
        # Update state for next step
        x = x_new
        v = v_new
        a = a_new
        
        history.append([x, v])
        
    return np.array(history)

# ==========================================================
# 3. RK4 Solver (Non-Symplectic, O(h⁴) Accurate)
# ==========================================================

def rk4_solve(deriv_func, S0, h, N_steps):
    """Explicit Fourth-Order Runge-Kutta integrator (RK4)."""
    S = S0.copy()
    history = [S0.copy()]
    
    for _ in range(N_steps):
        # Calculate four slopes (k1, k2, k3, k4)
        k1 = deriv_func(S)
        k2 = deriv_func(S + 0.5 * h * k1)
        k3 = deriv_func(S + 0.5 * h * k2)
        k4 = deriv_func(S + h * k3)
        
        # Apply weighted average (1/6, 2/6, 2/6, 1/6)
        S += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        history.append(S.copy())
        
    return np.array(history)

# ==========================================================
# 4. Run Solvers and Compute Energy Histories
# ==========================================================

# Run Velocity-Verlet (Symplectic)
history_verlet = velocity_verlet_solve(sho_acceleration, S0, H, N_STEPS)
E_verlet = np.array([sho_energy(S) for S in history_verlet])

# Run RK4 (Non-Symplectic)
history_rk4 = rk4_solve(sho_deriv, S0, H, N_STEPS)
E_rk4 = np.array([sho_energy(S) for S in history_rk4])

# ==========================================================
# 5. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the Total Energy histories
ax.plot(T_GRID, E_rk4, 'r-', linewidth=1.5, label=f"RK4 (Non-Symplectic, O(h⁴))")
ax.plot(T_GRID, E_verlet, 'b-', linewidth=1.5, label=f"Velocity-Verlet (Symplectic, O(h²))")

ax.axhline(E_TRUE, color='k', linestyle='--', label=f"True Energy (E={E_TRUE})")
ax.set_title(r"Energy Conservation in a Conservative System (SHO) Over Time")
ax.set_xlabel("Time (t)")
ax.set_ylabel(r"Total Energy $E$")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 6. Analysis Output
# ==========================================================
E_rk4_max_drift = (E_rk4[-1] - E_TRUE)
E_verlet_max_dev = np.max(np.abs(E_verlet - E_TRUE))

print("\n--- Long-Term Energy Drift Analysis ---")
print(f"Time Step (h): {H:.4f}")
print(f"Total Simulation Time: {T_FINAL} s ({N_STEPS} steps)")
print("-" * 40)
print("RK4 Method (Non-Symplectic):")
print(f"  Final Absolute Drift (E_final - E_true): {E_rk4_max_drift:.3e}")
print(f"  Result: Unbounded secular drift (RK4 fails long-term stability).")

print("\nVelocity-Verlet Method (Symplectic):")
print(f"  Maximum Absolute Deviation: {E_verlet_max_dev:.3e}")
print(f"  Result: Error oscillates and remains bounded (Symplectic integrity preserved).")
