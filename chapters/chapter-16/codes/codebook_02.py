
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import svd

# ==========================================================
# Chapter 16 Codebook: SVD & PCA
# Project 2: SVD for Noise Filtering (Image Compression)
# ==========================================================

# ==========================================================
# 1. Setup Data: Create a Sample 2D Matrix (Simple Image)
# ==========================================================
# Create a 20x20 matrix representing a simple visual pattern (a cross/checkerboard)
N_SIZE = 20
base_matrix = np.zeros((N_SIZE, N_SIZE))
base_matrix[5:15, 5:15] = 0.5 # Central gray square
base_matrix[7:13, 7:13] = 1.0 # Inner white square
base_matrix[10, :] = 0.8     # Horizontal line
base_matrix[:, 10] = 0.8     # Vertical line

# Add high-frequency noise to simulate messy data
NOISE_STD = 0.1
X_noisy = base_matrix + NOISE_STD * np.random.randn(N_SIZE, N_SIZE)

# ==========================================================
# 2. Compute SVD and Truncate
# ==========================================================
# U: Left singular vectors, s: Singular values, Vt: Transpose of right singular vectors
U, s, Vt = svd(X_noisy)

# Define the truncation rank (K)
# K=1 is maximal compression; K=20 is full reconstruction
K_RANK = 5 
# This rank should be large enough to capture the main signal, but small 
# enough to filter out most of the noise.

# Truncate the factorization
U_k = U[:, :K_RANK]
s_k = np.diag(s[:K_RANK]) # Reconstruct the diagonal matrix
Vt_k = Vt[:K_RANK, :]

# Reconstruct the filtered matrix
X_filtered = U_k @ s_k @ Vt_k

# ==========================================================
# 3. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 3, figsize=(15, 5))

# --- Plot 1: Original Noisy Matrix ---
im1 = ax[0].imshow(X_noisy, cmap='gray', vmin=0, vmax=1)
ax[0].set_title(r"Original Noisy Matrix ($\sigma=0.1$)")

# --- Plot 2: Singular Values ---
ax[1].plot(np.arange(1, N_SIZE + 1), s, 'b-o')
ax[1].axvline(K_RANK, color='r', linestyle='--', label=f"Truncation Rank K={K_RANK}")
ax[1].set_title("Singular Values ($\sigma_k$)")
ax[1].set_xlabel("Index k")
ax[1].set_ylabel("Singular Value Magnitude")
ax[1].set_yscale('log')
ax[1].grid(True)
ax[1].legend()

# --- Plot 3: SVD Filtered Matrix ---
im3 = ax[2].imshow(X_filtered, cmap='gray', vmin=0, vmax=1)
ax[2].set_title(f"SVD Filtered (Rank K={K_RANK})")


plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- SVD Filtering Summary ---")
print(f"Original Matrix Rank: {N_SIZE}")
print(f"Truncated Rank (K): {K_RANK}")

# Calculate the error improvement
rms_error_noisy = np.sqrt(np.mean((X_noisy - base_matrix)**2))
rms_error_filtered = np.sqrt(np.mean((X_filtered - base_matrix)**2))

print(f"RMS Error (Noisy vs. True Signal): {rms_error_noisy:.4f}")
print(f"RMS Error (Filtered vs. True Signal): {rms_error_filtered:.4f}")
print("\nConclusion: By zeroing out the smallest singular values (K=6 to 20), SVD effectively \nfilters the random noise, bringing the RMS error of the reconstructed matrix closer \nto the true, clean signal.")
