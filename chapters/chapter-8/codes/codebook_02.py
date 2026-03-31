import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 8 Codebook: Symplectic Integrators
# Project 2: N-Body Simulation (Two-Body Orbit)
# ==========================================================

# ==========================================================
# 1. Setup Model (Gravitational Acceleration)
# ==========================================================

# Physical parameters (in reduced units for stability: G=1, M=1)
G = 1.0 
M = 1.0 

# Initial conditions for a circular orbit (r=1, v=1, G*M=1)
R0 = 1.0               # Initial radius
V0 = np.sqrt(G * M / R0) # Initial velocity magnitude for a circular orbit

# Initial State Vector (S = [x, y, vx, vy])
S0 = np.array([R0, 0.0, 0.0, V0]) 

def gravitational_acceleration(S):
    """
    Calculates the acceleration vector (ax, ay) due to gravity.
    a = - (GM / r^2) * r_hat
    """
    x, y, vx, vy = S
    r_sq = x**2 + y**2
    r_mag = np.sqrt(r_sq)
    
    # Acceleration magnitude a_mag = -GM / r^2
    a_mag = -G * M / r_sq
    
    # Acceleration vector components
    ax = a_mag * (x / r_mag)
    ay = a_mag * (y / r_mag)
    
    return np.array([ax, ay])

def two_body_energy(S):
    """Calculates the total energy (Kinetic + Potential)."""
    x, y, vx, vy = S
    r_mag = np.sqrt(x**2 + y**2)
    v_sq = vx**2 + vy**2
    
    # Potential Energy (U) = -GM/r
    U = -G * M / r_mag
    # Kinetic Energy (K) = 1/2 * v^2 (m=1)
    K = 0.5 * v_sq
    
    return K + U

# ==========================================================
# 2. Velocity-Verlet Solver (Adapted for 4D Vector System)
# ==========================================================

def velocity_verlet_solve_4D(accel_func, S0, h, N_steps):
    """
    Implements Velocity-Verlet for a 4D state vector (x, y, vx, vy).
    """
    # Unpack initial state and calculate initial acceleration
    S = S0.copy()
    history = [S.copy()]
    
    # a is the 2D acceleration vector [ax, ay]
    a = accel_func(S) 
    
    for _ in range(N_steps):
        x, y, vx, vy = S
        ax, ay = a
        
        # 1. Half-Kick (Update v to v + h/2 * a)
        vx_half = vx + 0.5 * h * ax
        vy_half = vy + 0.5 * h * ay
        
        # 2. Full Drift (Update x/y to x/y + h * v_half)
        x_new = x + h * vx_half
        y_new = y + h * vy_half
        
        # New State for acceleration calculation
        S_new_pos = np.array([x_new, y_new, vx_half, vy_half])
        
        # 3. New Acceleration (Based on x_new, y_new)
        a_new = gravitational_acceleration(S_new_pos)
        ax_new, ay_new = a_new
        
        # 4. Half-Kick (Update v to v_half + h/2 * a_new)
        vx_new = vx_half + 0.5 * h * ax_new
        vy_new = vy_half + 0.5 * h * ay_new
        
        # Update state for next step
        S = np.array([x_new, y_new, vx_new, vy_new])
        a = a_new
        
        history.append(S.copy())
        
    return np.array(history)

# ==========================================================
# 3. Run Simulation and Compute Energy History
# ==========================================================
T_ORBITS = 100               # Simulate for 100 orbits
T_PERIOD = 2 * np.pi * np.sqrt(R0**3 / (G * M)) # Period for circular orbit
T_FINAL = T_ORBITS * T_PERIOD 
N_STEPS = 20000              # Total steps (200 steps per orbit)
H = T_FINAL / N_STEPS

# Run Velocity-Verlet
history_orbit = velocity_verlet_solve_4D(gravitational_acceleration, S0, H, N_STEPS)
E_orbit = np.array([two_body_energy(S) for S in history_orbit])
E_TRUE = two_body_energy(S0)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Trajectory (x vs. y) ---
ax[0].plot(history_orbit[:, 0], history_orbit[:, 1], 'b-', linewidth=1, label="Velocity-Verlet Orbit")
ax[0].plot(0, 0, 'y*', markersize=15, label="Central Mass")
ax[0].set_title(f"Symplectic Orbit Simulation ({T_ORBITS} Periods)")
ax[0].set_xlabel("x Position (AU)")
ax[0].set_ylabel("y Position (AU)")
ax[0].axis('equal')
ax[0].grid(True)
ax[0].legend()

# --- Plot 2: Total Energy (Stability Check) ---
T_GRID = np.linspace(0, T_FINAL, N_STEPS + 1)
ax[1].plot(T_GRID, E_orbit - E_TRUE, 'r-', linewidth=1.5, label="Energy Deviation (E - E₀)")
ax[1].axhline(0, color='k', linestyle='--', label="Zero Deviation")
ax[1].set_title("Energy Deviation from True Initial Value (Verlet)")
ax[1].set_xlabel("Time (t)")
ax[1].set_ylabel(r"$\Delta E$ (Deviation from $E_0$)")
ax[1].grid(True)
ax[1].ticklabel_format(axis='y', style='sci', scilimits=(0, 0)) # Scientific notation for small error

plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================
E_deviation = np.max(np.abs(E_orbit - E_TRUE))

print("\n--- Symplectic Orbit Stability Analysis ---")
print(f"Initial Energy (E₀): {E_TRUE:.6f}")
print(f"Total Periods Simulated: {T_ORBITS}")
print(f"Time Step (h): {H:.4e} (Steps per orbit: {N_STEPS / T_ORBITS:.0f})")
print("-" * 50)
print(f"Maximum Absolute Energy Deviation (ΔE_max): {E_deviation:.3e}")
print("\nConclusion: The energy deviation remains extremely small and bounded over 100 orbits, \nconfirming that Velocity-Verlet is a stable, structure-preserving (symplectic) integrator \nnecessary for long-term conservative dynamics.")
