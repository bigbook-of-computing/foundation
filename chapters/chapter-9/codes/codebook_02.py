
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal # Specialized eigensolver for TISE

# ==========================================================
# Chapter 9 Codebook: Boundary Value Problems
# Project 2: FDM & Quantum Mechanics (TISE Solver)
# ==========================================================

# ==========================================================
# 1. Setup Physical and Numerical Parameters
# ==========================================================

# Set constants for simplified units (hbar=1, m=1)
HBAR = 1.0
MASS = 1.0
L = 1.0        # Length of the box (m)
N = 500        # Number of interior grid points (determines matrix size)
H = L / (N + 1) # Spatial step size (h)

# Potential: V(x) = 0 for the infinite square well (Particle in a Box)
def potential_V(x):
    return 0.0

# Pre-calculate constants for the Hamiltonian matrix (H)
# Factor related to the kinetic energy term: -hbar^2 / (2m * h^2)
KE_FACTOR = -(HBAR**2) / (2.0 * MASS * H**2)
# Coefficient of the main diagonal terms (Kinetic + Potential)
DIAG_COEFF = -2.0 * KE_FACTOR # = (hbar^2 / (m * h^2))

# ==========================================================
# 2. Construct the Hamiltonian Matrix (H)
# ==========================================================

# The FDM converts TISE into Hψ = Eψ, where H is a tridiagonal matrix.
# We build the main diagonal (d) and the off-diagonal (e).

# --- Main Diagonal (d_i = (hbar² / m h²) + V_i) ---
# For V(x) = 0 (Particle in a Box): d_i = (hbar² / m h²)
d = np.full(N, DIAG_COEFF)
# If V(x) were non-zero (e.g., Finite Well), we would add V(x_i) here:
# x_grid = np.linspace(H, L - H, N)
# V_grid = potential_V(x_grid)
# d = np.full(N, DIAG_COEFF) + V_grid

# --- Off-Diagonal (e_i = -hbar² / (2m h²)) ---
# This couples neighbor nodes.
e = np.full(N - 1, KE_FACTOR)

# ==========================================================
# 3. Solve the Matrix Eigenvalue Problem
# ==========================================================

# The specialized routine eigh_tridiagonal is O(N²) and much faster than 
# a general O(N³) eigensolver, exploiting the tridiagonal structure.
eigenvalues_E, eigenvectors_psi_raw = eigh_tridiagonal(d, e)

# The eigenvalues are the quantized energy levels E.
# The eigenvectors are the wavefunctions ψ (at the interior grid points).

# ==========================================================
# 4. Process and Visualize Results
# ==========================================================

# --- Process Wavefunctions (Add boundary zeros) ---
# The solution ψ is 0 at the boundaries (Dirichlet BCs).
# We reshape the results to include x=0 and x=L.
def add_boundaries(psi_vector):
    return np.insert(psi_vector, [0, psi_vector.size], [0.0, 0.0])

# Grid for plotting (includes boundaries)
x_plot = np.linspace(0, L, N + 2) 

# --- Visualization ---
fig, ax = plt.subplots(figsize=(8, 5))

# Plot the first three stationary states (n=1, n=2, n=3)
for n in range(3):
    E_n_numerical = eigenvalues_E[n]
    psi_n = add_boundaries(eigenvectors_psi_raw[:, n])
    
    # Normalize the wavefunction for plotting ease (standard is L2 norm)
    # Scale for visualization: shift by the energy level to separate the plots
    plot_scale = 0.5 # Arbitrary scaling for clean visualization
    psi_n_normalized = psi_n / np.sqrt(np.sum(psi_n**2 * H))
    
    # Apply vertical offset for visualization
    y_plot = (n + 1) * plot_scale + psi_n_normalized

    ax.plot(x_plot, y_plot, 
            label=f"$n={n+1}$: $E = {E_n_numerical:.3f}$")

# Plot the energy lines
for n in range(3):
    ax.axhline((n + 1) * plot_scale, color='gray', linestyle=':', alpha=0.5)

# --- Analytic Check (E_n = n^2 * pi^2 * hbar^2 / (2m L^2)) ---
E_analytic_factor = (np.pi**2 * HBAR**2) / (2 * MASS * L**2)
E_analytic_1 = E_analytic_factor * (1**2)

ax.set_title(r"FDM Solution to TISE: Wavefunctions and Energy Levels")
ax.set_xlabel("Position $x$")
ax.set_ylabel(r"Wavefunction $\psi_n(x)$ (Offset)")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================
E_num_1 = eigenvalues_E[0]
E_ana_1 = E_analytic_1
E_error_1 = np.abs(E_num_1 - E_ana_1) / E_ana_1

print("\n--- Eigenvalue (Energy) Analysis ---")
print(f"Grid Size (N): {N} points, Step Size (h): {H:.4e}")
print(f"Analytic E₁ Factor: {E_analytic_factor:.6f}")
print("-" * 40)
print(f"| State (n) | Numerical E | Analytic E | Rel Error |")
print("|-----------|-------------|------------|-----------|")
for n in range(3):
    E_num = eigenvalues_E[n]
    E_ana = E_analytic_factor * ((n + 1)**2)
    rel_error = np.abs(E_num - E_ana) / E_ana
    print(f"| {n+1:<9} | {E_num:.6f} | {E_ana:.6f} | {rel_error:.2e} |")

print("\nConclusion: The FDM successfully finds the quantized energy eigenvalues with high \naccuracy (error < 10⁻⁴), confirming the stable and efficient conversion of the TISE \ninto a tridiagonal matrix problem.")
