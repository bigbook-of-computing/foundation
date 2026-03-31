
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.optimize import root_scalar

# ==========================================================
# Chapter 9 Codebook: Boundary Value Problems
# Project 1: The Shooting Method — Instability Demonstration
# ==========================================================

# ==========================================================
# 1. Setup IVP Model and Parameters
# ==========================================================

# BVP: y''(x) = 0.25 * y(x)
# Convert to coupled first-order IVP: S' = [y', y''] = [v, 0.25*y]
def ivp_deriv(x, S):
    """Derivative function for the IVP solver."""
    y, v = S
    return np.array([v, 0.25 * y])

# Boundary Conditions (Target)
Y_A = 1.0  # y(0) = 1.0
X_FINAL = 2.0
Y_B_TARGET = 0.5 # y(2) = 0.5

# ==========================================================
# 2. Define the Error Function (The Root-Finding Problem)
# ==========================================================

def error_function(g_initial_slope):
    """
    The Error Function E(g) = y_final(L, g) - Y_B_TARGET.
    This runs a full IVP simulation for a given initial slope (g) and measures 
    how far the final position is from the target (Y_B_TARGET).
    """
    # Initial conditions for the IVP: S0 = [y(0), y'(0)]
    S0_ivp = np.array([Y_A, g_initial_slope])
    
    # Solve the IVP from x=0 to x=X_FINAL
    # Use the accurate RK45 method (default in solve_ivp)
    sol = solve_ivp(ivp_deriv, [0, X_FINAL], S0_ivp, 
                    dense_output=True, rtol=1e-6, atol=1e-9)
    
    # Extract the final y-position at x=X_FINAL
    y_final = sol.y[0, -1]
    
    # Return the "miss distance"
    return y_final - Y_B_TARGET

# ==========================================================
# 3. Solve for the Correct Initial Slope (Root Finding)
# ==========================================================

# Initial Guesses (This step is often difficult and unstable)
g_guess_1 = -0.5
g_guess_2 = -0.4

# Solve for the root of the error function E(g) = 0
try:
    # Use Brent's method for efficiency and robustness
    g_solution = root_scalar(error_function, bracket=[g_guess_1, g_guess_2], method='brentq')
    G_OPT = g_solution.root
    
    print(f"✅ Root-finding successful: Optimal initial slope g = y'(0) = {G_OPT:.6f}")

except ValueError:
    # Catches the case where the initial bracket does not contain the root (a common failure)
    print("❌ Root-finding failed: Initial slope guesses did not bracket the root.")
    G_OPT = np.nan # Set to NaN if failure occurs
    
# ==========================================================
# 4. Run Final, Corrected Trajectory and Visualization
# ==========================================================

if not np.isnan(G_OPT):
    # Run the final IVP simulation with the optimal initial slope
    S0_final = np.array([Y_A, G_OPT])
    sol_final = solve_ivp(ivp_deriv, [0, X_FINAL], S0_final, 
                        dense_output=True, rtol=1e-6, atol=1e-9)
    
    # Generate fine grid for plotting
    x_grid = np.linspace(0, X_FINAL, 100)
    y_final_trajectory = sol_final.sol(x_grid)[0]

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(x_grid, y_final_trajectory, 'b-', linewidth=2, label="BVP Solution (Shooting Method)")
    
    # Mark Boundary Conditions
    ax.plot(0, Y_A, 'ro', label=f"Boundary A: y(0)={Y_A}")
    ax.plot(X_FINAL, Y_B_TARGET, 'go', label=f"Boundary B: y({X_FINAL})={Y_B_TARGET}")
    
    # Mark the successful endpoint check
    ax.axhline(Y_B_TARGET, color='g', linestyle='--')

    ax.set_title(r"BVP Solution using Shooting Method (Optimal $y'(0)$ Found)")
    ax.set_xlabel("Position (x)")
    ax.set_ylabel("Displacement (y)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# Final Analysis
if not np.isnan(G_OPT):
    print("\n--- Shooting Method Summary ---")
    print(f"BVP Solved on domain [0, {X_FINAL}]")
    print(f"Optimal Initial Slope (y'(0)): {G_OPT:.6f}")
    print(f"Final Value Check (y({X_FINAL})): {y_final_trajectory[-1]:.6f} (Target: {Y_B_TARGET})")
