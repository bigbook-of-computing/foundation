import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 7 Codebook: Initial Value Problems I
# Project 2: Coupled Systems — Projectile Motion with Drag
# ==========================================================

# ==========================================================
# 1. Setup Parameters and 4D Derivative Function
# ==========================================================

# Physical parameters
G = 9.81              # Gravity (m/s²)
M = 1.0               # Mass (kg)
K_DRAG = 0.05         # Quadratic Drag Coefficient (k)

# Initial conditions
THETA_DEG = 45.0
V0 = 50.0             # Initial velocity (m/s)
V0X = V0 * np.cos(np.deg2rad(THETA_DEG))
V0Y = V0 * np.sin(np.deg2rad(THETA_DEG))

# State vector S = [x, y, vx, vy]
S0 = np.array([0.0, 0.0, V0X, V0Y])

def drag_deriv(t, S):
    """
    Derivative function for 4D coupled system: S' = [vx, vy, ax, ay].
    Drag force: F_d = -k * |v| * v
    """
    # Unpack state
    x, y, vx, vy = S
    
    # Velocity magnitude
    v_mag = np.sqrt(vx**2 + vy**2)
    
    # Calculate acceleration vector (a = F_net / m)
    
    # Gravity component: F_g = [0, -m*g]
    # Drag component: F_d = [-k*|v|*vx, -k*|v|*vy]
    
    # Net Force Components
    Fx_net = -K_DRAG * v_mag * vx
    Fy_net = -M * G - K_DRAG * v_mag * vy
    
    # Accelerations (ax, ay)
    ax = Fx_net / M
    ay = Fy_net / M
    
    # Return the derivative vector S' = [vx, vy, ax, ay]
    return np.array([vx, vy, ax, ay])

# ==========================================================
# 2. Implement RK4 Solver (Adapted from Project 1)
# ==========================================================

def rk4_solve(deriv_func, S0, h, T_max):
    """RK4 solver with a stopping condition (y < 0)."""
    S = S0.copy()
    history = [S0.copy()]
    
    time = 0.0
    
    while S[1] >= 0: # Stop when y-position (S[1]) hits or goes below ground
        # Calculate four slopes
        k1 = deriv_func(time, S)
        k2 = deriv_func(time + 0.5 * h, S + 0.5 * h * k1)
        k3 = deriv_func(time + 0.5 * h, S + 0.5 * h * k2)
        k4 = deriv_func(time + h, S + h * k3)
        
        # Apply weighted average
        S += (h / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        time += h
        
        # Safety break and store
        if len(history) > 50000: break
        history.append(S.copy())
    
    return np.array(history)

# ==========================================================
# 3. Run Simulation and Calculate Comparison Trajectory
# ==========================================================

# Simulation parameters
H = 0.01             # Time step size (Δt)

# Run RK4 for the drag trajectory
history_drag = rk4_solve(drag_deriv, S0, H, 100) # T_max is large, stop condition is y<0

# Analytic trajectory (no drag) for comparison: y(x) = x * tan(theta) - (g * x^2) / (2 * v0^2 * cos^2(theta))
def analytic_trajectory(x):
    tan_theta = np.tan(np.deg2rad(THETA_DEG))
    cos_sq_theta = np.cos(np.deg2rad(THETA_DEG))**2
    return x * tan_theta - (G * x**2) / (2 * V0**2 * cos_sq_theta)

# Determine the max x-range for the analytic plot
X_DRAG_MAX = history_drag[-1, 0]
x_analytic_grid = np.linspace(0, X_DRAG_MAX, 100)
y_analytic_grid = analytic_trajectory(x_analytic_grid)

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the drag trajectory
ax.plot(history_drag[:, 0], history_drag[:, 1], 'r-', linewidth=2, label=f"RK4 with Drag (k={K_DRAG})")

# Plot the ideal (no drag) trajectory
ax.plot(x_analytic_grid, y_analytic_grid, 'k--', label="Analytic (No Drag)")

ax.axhline(0, color='gray', linestyle='-')
ax.set_title("Projectile Motion: Drag vs. Ideal Trajectory (RK4)")
ax.set_xlabel("Horizontal Distance (x) [m]")
ax.set_ylabel("Vertical Distance (y) [m]")
ax.legend()
ax.grid(True)
ax.set_ylim(bottom=0)
plt.tight_layout()
plt.show()

# Final Analysis
range_drag = history_drag[-1, 0]
range_ideal = V0**2 * np.sin(2*np.deg2rad(THETA_DEG)) / G

print("\n--- Projectile Range Analysis ---")
print(f"Time Step (h): {H:.2f}")
print(f"Initial Velocity: {V0} m/s at {THETA_DEG}°")
print(f"Ideal Range (No Drag): {range_ideal:.2f} m")
print(f"RK4 Range (with Drag): {range_drag:.2f} m")
print(f"Range Reduction due to Drag: {range_ideal - range_drag:.2f} m")
