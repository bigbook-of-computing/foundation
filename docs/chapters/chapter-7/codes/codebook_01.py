import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 7 Codebook: Initial Value Problems I
# Project 1: Accuracy and Stability Showdown (Euler vs. RK4)
# ==========================================================

# ==========================================================
# 1. Define Model (Simple Harmonic Oscillator)
# ==========================================================

def sho_deriv(t, S):
    """
    Derivative function for the Simple Harmonic Oscillator (x'' = -x).
    S = [x, v], S' = [v, -x]
    """
    x, v = S
    # dx/dt = v, dv/dt = -x
    return np.array([v, -x])

def sho_energy(S):
    """Calculates the total energy: E = 1/2 * (v^2 + x^2) (assuming m=k=1)."""
    x, v = S
    return 0.5 * (v**2 + x**2)

# Initial conditions and parameters
S0 = np.array([1.0, 0.0]) # Initial state: x(0)=1, v(0)=0
T_FINAL = 50.0            # Simulate for 50 periods (t=0 to 50)
N_STEPS = 5000            # Total number of steps
H = T_FINAL / N_STEPS     # Time step size (Δt)
T_GRID = np.linspace(0, T_FINAL, N_STEPS + 1)
E_TRUE = sho_energy(S0)   # True energy should be constant: 0.5 * (1^2 + 0^2) = 0.5

# ==========================================================
# 2. Implement Euler's Method (O(h) Accuracy)
# ==========================================================

def euler_solve(deriv_func, S0, h, N_steps):
    """Explicit Forward Euler integrator."""
    S = S0.copy()
    history = [S0.copy()]
    
    for _ in range(N_steps):
        S_prime = deriv_func(0, S) # t is ignored for autonomous system
        S += h * S_prime
        history.append(S.copy())
    return np.array(history)

# ==========================================================
# 3. Implement RK4 Method (O(h⁴) Accuracy)
# ==========================================================

def rk4_solve(deriv_func, S0, h, N_steps):
    """Explicit Fourth-Order Runge-Kutta integrator (RK4)."""
    S = S0.copy()
    history = [S0.copy()]
    
    for _ in range(N_steps):
        # Calculate four slopes (k1, k2, k3, k4)
        k1 = deriv_func(0, S)
        k2 = deriv_func(0, S + 0.5 * h * k1)
        k3 = deriv_func(0, S + 0.5 * h * k2)
        k4 = deriv_func(0, S + h * k3)
        
        # Apply weighted average (1/6, 2/6, 2/6, 1/6)
        S += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        history.append(S.copy())
    return np.array(history)

# ==========================================================
# 4. Run Solvers and Compute Energy Histories
# ==========================================================

# Run Euler's Method
history_euler = euler_solve(sho_deriv, S0, H, N_STEPS)
E_euler = np.array([sho_energy(S) for S in history_euler])

# Run RK4 Method
history_rk4 = rk4_solve(sho_deriv, S0, H, N_STEPS)
E_rk4 = np.array([sho_energy(S) for S in history_rk4])

# ==========================================================
# 5. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Trajectory (x vs. t) ---
ax[0].plot(T_GRID, history_euler[:, 0], 'r--', label="Euler (x)")
ax[0].plot(T_GRID, history_rk4[:, 0], 'b-', label="RK4 (x)")
ax[0].plot(T_GRID, np.cos(T_GRID), 'k:', label="Analytic (cos(t))")
ax[0].set_title(f"SHO Trajectory Comparison (h={H:.4f})")
ax[0].set_xlabel("Time (t)")
ax[0].set_ylabel("Position (x)")
ax[0].legend()
ax[0].grid(True)

# --- Plot 2: Total Energy (Stability Check) ---
ax[1].plot(T_GRID, E_euler, 'r-', label="Euler Energy (Drifting)")
ax[1].plot(T_GRID, E_rk4, 'b-', label="RK4 Energy (Stable Locally)")
ax[1].axhline(E_TRUE, color='k', linestyle='--', label=f"True Energy (E={E_TRUE})")
ax[1].set_title("Stability and Energy Drift Over Time")
ax[1].set_xlabel("Time (t)")
ax[1].set_ylabel(r"Total Energy $E$")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()

# ==========================================================
# 6. Analysis Output
# ==========================================================
print("\n--- Stability and Accuracy Analysis ---")
print(f"Time Step (h): {H:.4f}")
print(f"Total Simulation Time: {T_FINAL} s")
print("-" * 35)

# Measure final energy deviation
E_euler_dev = (E_euler[-1] - E_TRUE) / E_TRUE
E_rk4_dev = (E_rk4[-1] - E_TRUE) / E_TRUE

print("Euler Method:")
print(f"  Final Energy Deviation: {E_euler_dev * 100:.2f}% (Systematically Unstable)")

print("RK4 Method:")
print(f"  Final Energy Deviation: {E_rk4_dev * 100:.2f}% (Locally Accurate, but still small drift)")

print("\nConclusion: Euler's method systematically injects energy into the system, causing an \nexponential growth in amplitude and energy (instability). RK4 maintains high local \naccuracy and energy conservation over this timescale, demonstrating its superiority as \na general-purpose integrator.")
