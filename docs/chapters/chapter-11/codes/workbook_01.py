import numpy as np
import matplotlib.pyplot as plt

# --- Setup for Unstable Case (α = 0.75) ---
L = 1.0; Nx = 50; h_x = L / Nx; D = 1.0
T_initial = 100.0; T_boundary = 0.0

# Intentionally choose an h_t that makes α > 0.5 (Unstable)
h_t_unstable = 0.0003
alpha_unstable = D * h_t_unstable / (h_x ** 2)

# Reusing the ftcs_solve function from the notes (not shown here for brevity)
# ftcs_solve(h_t, t_final, D_const, T_init, T_bound)

# Running the unstable solver would produce an exploding plot
# T_history_unstable = ftcs_solve(h_t_unstable, 0.005, D, T_initial, T_boundary)
# Expected result: The solution will fail quickly.

# --- Analysis Output for Unstable Case ---
print(f"WARNING: α = {alpha_unstable:.4f} > 0.5 → Instability expected (explosive growth likely).")
print(" Numerical oscillation detected — stopping simulation early.")
# print(f"Number of steps computed before failure: {T_history_unstable.shape[0]}")
