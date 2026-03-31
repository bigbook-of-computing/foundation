
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh_tridiagonal # O(N²) specialized solver

# ==========================================================
# Chapter 14 Codebook: Eigenvalue Problems
# Project 1: Quantum Eigenvalues (TISE Solver for SHO)
# ==========================================================

# ==========================================================
# 1. Setup Physical and Numerical Parameters
# ==========================================================

# Set constants for simplified units (hbar=1, m=1)
HBAR = 1.0
MASS = 1.0
K_SPRING = 1.0 # Spring constant for the SHO potential V(x) = 1/2 * k * x^2

# Define the spatial domain and grid
X_MAX = 5.0    # Domain length from -X_MAX to +X_MAX
L = 2.0 * X_MAX
N = 500        # Number of interior grid points (matrix size)
H = L / (N + 1) # Spatial step size (h)

# Grid for plotting (includes boundaries)
x_interior = np.linspace(-X_MAX + H, X_MAX - H, N)
x_plot = np.linspace(-X_MAX, X_MAX, N + 2)

# --- Potential Energy Function V(x) ---
def V_SHO(x):
    """The potential energy function for the Simple Harmonic Oscillator."""
    return 0.5 * K_SPRING * x**2

# Pre-calculate Kinetic Energy factors
# KE_FACTOR: -hbar^2 / (2m * h^2) (Off-diagonal coefficient)
KE_FACTOR = -(HBAR**2) / (2.0 * MASS * H**2)
# DIAG_COEFF: (hbar^2 / m h^2) (Base for main diagonal)
DIAG_COEFF = -2.0 * KE_FACTOR 

# ==========================================================
# 2. Construct the Hamiltonian Matrix (H)
# ==========================================================

# The FDM approximation Hψ = Eψ results in a symmetric, tridiagonal matrix.

# --- Main Diagonal (d_i = (hbar² / m h²) + V_i) ---
V_grid = V_SHO(x_interior)
d = DIAG_COEFF + V_grid

# --- Off-Diagonal (e_i = -hbar² / (2m h²)) ---
# This couples neighbor nodes (purely kinetic energy term).
e = np.full(N - 1, KE_FACTOR)

# ==========================================================
# 3. Solve the Matrix Eigenvalue Problem
# ==========================================================

# E_n: Eigenvalues (Energy Levels)
# psi_n_raw: Eigenvectors (Wavefunctions)
E_num, psi_raw = eigh_tridiagonal(d, e)

# The eigenvalues and eigenvectors are sorted by energy (ascending).

# ==========================================================
# 4. Process and Visualize Results
# ==========================================================

# --- Process Wavefunctions (Add boundaries and normalize) ---
def add_boundaries_and_scale(psi_vector, n, plot_scale=10.0):
    """Adds fixed boundary zeros and scales/offsets for visualization."""
    # Add boundary zeros (Dirichlet BCs)
    psi_with_bc = np.insert(psi_vector, [0, psi_vector.size], [0.0, 0.0])
    
    # Normalize (Standard L2 norm)
    # The normalization factor calculated from the grid sum
    norm_factor = np.sqrt(np.sum(psi_with_bc**2 * H))
    psi_normalized = psi_with_bc / norm_factor
    
    # Apply vertical offset by the energy level for separation
    return psi_normalized * plot_scale + E_num[n]

# --- Visualization ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(x_plot, V_SHO(x_plot), 'k--', label=r"Potential $V(x) = \frac{1}{2}kx^2$")

# Plot the first four stationary states (n=0, n=1, n=2, n=3)
for n in range(4):
    E_n_numerical = E_num[n]
    
    # Calculate the normalized and offset wavefunction
    psi_n_plot = add_boundaries_and_scale(psi_raw[:, n], n)

    # Plot the wavefunction
    ax.plot(x_plot, psi_n_plot, label=f"$n={n}$: $E = {E_n_numerical:.4f}$")
    
    # Plot the energy level line
    ax.axhline(E_n_numerical, color='gray', linestyle=':', alpha=0.6)

ax.set_title(r"FDM Solution to TISE: Simple Harmonic Oscillator")
ax.set_xlabel("Position $x$")
ax.set_ylabel(r"Energy $E$ and Wavefunction $\psi_n(x)$ (Offset)")
ax.set_ylim(-0.5, E_num[3] * 1.5)
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 5. Analysis Output
# ==========================================================

# Analytic Check: E_n = (n + 1/2) * hbar * sqrt(k/m)
E_analytic_factor = HBAR * np.sqrt(K_SPRING / MASS)
print("\n--- TISE Eigenvalue Analysis (Simple Harmonic Oscillator) ---")
print(f"Grid Size (N): {N}, Step Size (h): {H:.4e}")
print(f"Analytic Energy Factor (ℏω): {E_analytic_factor:.6f}")
print("-" * 60)
print("| State (n) | Numerical E | Analytic E | Rel Error |")
print("|-----------|-------------|------------|-----------|")
for n in range(4):
    E_num_n = E_num[n]
    E_ana_n = (n + 0.5) * E_analytic_factor
    rel_error = np.abs(E_num_n - E_ana_n) / E_ana_n
    print(f"| {n:<9} | {E_num_n:.6f} | {E_ana_n:.6f} | {rel_error:.2e} |")

print("\nConclusion: The FDM successfully finds the quantized SHO energy levels, which are \nevenly spaced by ℏω, with high accuracy. The efficiency of the specialized \ntridiagonal solver is key to the performance of this quantum model.")
