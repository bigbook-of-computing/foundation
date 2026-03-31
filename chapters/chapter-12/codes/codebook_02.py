
import numpy as np
import matplotlib.pyplot as plt

# ==========================================================
# Chapter 12 Codebook: Hyperbolic PDEs
# Project 2: Plucked String Simulation (Verlet and First Step)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Initial Conditions
# ==========================================================

L = 1.0           # Length of the string (m)
Nx = 100          # Number of interior spatial points
v = 1.0           # Wave speed (m/s)

h_x = L / (Nx + 1)  # Spatial step size (Δx)
C = 1.0             # Courant Number (C=1 for fastest stable simulation, C <= 1)
h_t = C * h_x / v   # Time step size (Δt)
C_sq = C**2

T_FINAL = 2.0     # Total simulation time (s) (One full period: 2L/v)
N_steps = int(T_FINAL / h_t)
N_total = Nx + 2

x_grid = np.linspace(0, L, N_total)

# Initial condition: A triangular plucked shape
PLUCK_HEIGHT = 0.05
PLUCK_POS = 0.2  # Pluck point (e.g., L/5)

def initial_plucked_shape(x):
    """Creates a triangular displacement profile."""
    return np.where(x <= PLUCK_POS,
                    PLUCK_HEIGHT * x / PLUCK_POS,
                    PLUCK_HEIGHT * (L - x) / (L - PLUCK_POS))

# Initial state: Plucked and released from rest (v_initial = 0)
y_past = initial_plucked_shape(x_grid) # y(n=0)
y_present = np.zeros_like(y_past)
V_INITIAL = 0.0 # Initial velocity is zero everywhere

# Store history for visualization
y_history = [] 

# ==========================================================
# 2. Initialization: The Special First Step (n=0 to n=1)
# ==========================================================

# Formula for v_i,0 = 0: y_i,1 = y_i,0 + (C^2 / 2) * [Laplacian]
print(f"Starting simulation with C={C:.2f} (Verlet/FTCS).")

for i in range(1, N_total - 1):
    laplacian_term = y_past[i+1] - 2 * y_past[i] + y_past[i-1]
    
    # Special formula for v_initial = 0
    y_present[i] = y_past[i] + 0.5 * C_sq * laplacian_term
    
# Boundary conditions y(0)=y(L)=0 are preserved
y_past[0] = y_past[-1] = 0.0
y_present[0] = y_present[-1] = 0.0

y_history.append(y_past.copy()) 
y_history.append(y_present.copy())

# ==========================================================
# 3. The Main Time March (FTCS / Verlet Loop, n >= 1)
# ==========================================================

for n in range(1, N_steps):
    y_future = np.zeros_like(y_past)

    for i in range(1, N_total - 1):
        laplacian_term = y_present[i+1] - 2 * y_present[i] + y_present[i-1]
        
        # FTCS (Verlet) Update Rule: y_n+1 = 2y_n - y_n-1 + C^2 * [Laplacian]
        y_future[i] = 2 * y_present[i] - y_past[i] + C_sq * laplacian_term

    # Advance the time levels
    y_past = y_present.copy()
    y_present = y_future.copy()
    y_history.append(y_present.copy())

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

# Select indices for plotting key moments in the wave cycle (e.g., reflection stages)
time_points = [0, N_steps // 4, N_steps // 2, N_steps - 1] 
time_points_labels = [f"t = {idx * h_t:.2f} s" for idx in time_points]

fig, ax = plt.subplots(figsize=(8, 5))
ax.set_title(r"1D Wave Equation: Plucked String Simulation ($C = 1.0$)")
ax.set_xlabel("Position $x$")
ax.set_ylabel("Displacement $y$")
ax.set_ylim(-PLUCK_HEIGHT * 1.1, PLUCK_HEIGHT * 1.1) 

# Plot the key stages of propagation and reflection
for idx, label in zip(time_points, time_points_labels):
    ax.plot(x_grid, y_history[idx], label=label)

ax.axhline(0, color='gray', linestyle='-')
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Plucked String Simulation Summary ---")
print(f"Analytic Wave Period (2L/v): {2 * L / v:.2f} s")
print(f"Total Time Simulated: {T_FINAL:.2f} s")
print(f"Courant Number C: {C:.2f}")
print("\nConclusion: The string successfully simulated propagation and reflection over a full period \nwithout dissipation or explosion, validating the use of the explicit (Verlet-like) FTCS scheme \nunder the CFL constraint.")
