
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh # General symmetric/Hermitian eigensolver

# ==========================================================
# Chapter 14 Codebook: Eigenvalue Problems
# Project 2: Classical Eigenvalues (Coupled Oscillators)
# ==========================================================

# ==========================================================
# 1. Setup System Matrices (3 Coupled Masses)
# ==========================================================

# Assume three masses (m1, m2, m3) and four springs (k1, k2, k3, k4)
# Fixed boundaries on the outer springs (k1 and k4 fixed to walls)

# Physical Parameters
m = 1.0 # All masses are equal
k = 1.0 # All spring constants are equal

# --- Mass Matrix (M) ---
# M is diagonal for masses m1, m2, m3
M = np.diag([m, m, m])

# --- Stiffness Matrix (K) ---
# K is determined by the coupling: 
# K_ii = sum of springs connected to mass i (k_i + k_{i+1})
# K_i,i+1 = -k_{i+1} (coupling between mass i and i+1)
K = np.array([
    [k + k,    -k,      0],
    [ -k,    k + k,    -k],
    [  0,     -k,    k + k]
])

# K simplifies to:
# K = [[ 2, -1, 0], 
#      [-1,  2, -1],
#      [ 0, -1, 2]]

# ==========================================================
# 2. Solve the Generalized Eigenvalue Problem
# ==========================================================

# Goal: Solve Kx = ω²Mx, where λ = ω²
# We use scipy.linalg.eigh, which solves the generalized problem: Ax = λBx (where A=K, B=M)

# eigenvalues (λ = ω²) and eigenvectors (x = mode shapes)
eigenvalues, eigenvectors = eigh(K, M)

# Convert eigenvalues (ω²) to natural frequencies (f = ω / 2π)
frequencies_rad = np.sqrt(eigenvalues) # ω_n
frequencies_hz = frequencies_rad / (2.0 * np.pi) # f_n

# ==========================================================
# 3. Process and Visualize Results
# ==========================================================

# The eigenvectors define the relative displacements (mode shapes)
mode_shapes = eigenvectors.T # Transpose so each row is a mode

fig, ax = plt.subplots(1, 3, figsize=(12, 4), sharey=True)
titles = ["Mode 1 (Symmetric)", "Mode 2 (Anti-Symmetric)", "Mode 3 (Twisting)"]

for n in range(3):
    ax[n].bar(np.arange(1, 4), mode_shapes[n], color=['gray', 'blue', 'gray'])
    ax[n].set_title(f"{titles[n]}\n$f_{n+1} = {frequencies_hz[n]:.3f}$ Hz")
    ax[n].set_xlabel("Mass Index")
    ax[n].set_xticks([1, 2, 3])
    ax[n].axhline(0, color='k', linewidth=0.5)
    ax[n].grid(axis='y', alpha=0.5)

ax[0].set_ylabel("Relative Displacement")

plt.suptitle("Normal Modes of Oscillation for 3 Coupled Masses")
plt.tight_layout(rect=[0, 0.03, 1, 0.95])
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================

print("\n--- Normal Modes Analysis ---")
print("Mode Shapes (Eigenvectors):")
print("Each column is a normalized mode shape (relative displacement of M1, M2, M3).")
print(mode_shapes.T)
print("-" * 50)
print("| Mode (n) | Eigenvalue (ω²) | Frequency (f) | Description |")
print("|----------|-----------------|---------------|-------------|")

for n in range(3):
    desc = titles[n].split('(')[1].split(')')[0]
    print(f"| {n+1:<8} | {eigenvalues[n]:<15.6f} | {frequencies_hz[n]:<13.3f} | {desc:<11} |")

print("\nConclusion: The generalized eigensolver successfully decoupled the complex coupled motion \ninto three independent normal modes, each with a unique, characteristic frequency and shape.")
