
import numpy as np
import matplotlib.pyplot as plt
from scipy.linalg import eigh

# ==========================================================
# Chapter 16 Codebook: SVD & PCA
# Project 1: Principal Component Analysis (PCA) on Data
# ==========================================================

# ==========================================================
# 1. Generate Synthetic Data
# ==========================================================
# Data represents 500 observations of 3 coupled variables (dimensions)
N_OBSERVATIONS = 500
N_DIMENSIONS = 3

# Create correlated data: Data is primarily aligned along PC1 and PC2.
rng = np.random.default_rng(42)
z = rng.normal(size=(N_OBSERVATIONS, 3)) # Base Gaussian data

# Create transformation matrix to induce correlation and variance
# This matrix ensures that variance is dominated by the first two components
T = np.array([
    [10.0, 1.0, 0.5], # PC1: High variance
    [1.0, 5.0, 0.5],  # PC2: Medium variance
    [0.5, 0.5, 1.0]   # PC3: Low variance (mostly noise)
])
X = z @ T # X is the final 500x3 high-dimensional data matrix

# ==========================================================
# 2. PCA Step 1: Centering the Data
# ==========================================================
# Center the data by subtracting the mean of each column
X_mean = np.mean(X, axis=0)
X_centered = X - X_mean

# ==========================================================
# 3. PCA Step 2: Calculate Covariance Matrix (C)
# ==========================================================
# C = (1 / (N-1)) * X_centeredᵀ * X_centered
C = np.cov(X_centered, rowvar=False) # rowvar=False means columns are variables

# ==========================================================
# 4. PCA Step 3: Solve the Eigenvalue Problem
# ==========================================================
# C * v = λ * v  (Eigenvalues λ are the variances; Eigenvectors v are the PCs)

# Solve the symmetric eigenvalue problem
eigenvalues, eigenvectors = eigh(C)

# Sort results in descending order of eigenvalue (variance)
# Eigenvectors (PCs) are columns in the output; transpose for easy sorting
idx = np.argsort(eigenvalues)[::-1]
eigenvalues_sorted = eigenvalues[idx]
eigenvectors_sorted = eigenvectors[:, idx] # Principal Components (PCs)

# Calculate the explained variance ratio
total_variance = np.sum(eigenvalues_sorted)
variance_ratio = eigenvalues_sorted / total_variance

PC1 = eigenvectors_sorted[:, 0]
PC2 = eigenvectors_sorted[:, 1]

# ==========================================================
# 5. Projection (Dimensionality Reduction)
# ==========================================================
# Project the original data onto the new 2D subspace defined by PC1 and PC2
# X_reduced = X_centered @ V_reduced (V_reduced = [PC1, PC2])
X_reduced = X_centered @ eigenvectors_sorted[:, 0:2]

# ==========================================================
# 6. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Explained Variance ---
cumulative_variance = np.cumsum(variance_ratio)
ax[0].plot(range(1, N_DIMENSIONS + 1), variance_ratio, 'bo-', label="Individual Variance")
ax[0].plot(range(1, N_DIMENSIONS + 1), cumulative_variance, 'r*-', label="Cumulative Variance")
ax[0].set_title("Explained Variance by Principal Components")
ax[0].set_xlabel("Principal Component Index")
ax[0].set_ylabel("Variance Explained")
ax[0].set_xticks(range(1, N_DIMENSIONS + 1))
ax[0].grid(True)
ax[0].legend()


# --- Plot 2: Reduced 2D Projection ---
# Visualize the 3D data in the new 2D coordinate system
ax[1].scatter(X_reduced[:, 0], X_reduced[:, 1], alpha=0.5)
ax[1].set_title("Data Projected onto PC1 and PC2 (Dimensionality Reduction)")
ax[1].set_xlabel(f"Principal Component 1 (PC1, {variance_ratio[0]*100:.1f}%)")
ax[1].set_ylabel(f"Principal Component 2 (PC2, {variance_ratio[1]*100:.1f}%)")
ax[1].axis('equal')
ax[1].grid(True)

plt.tight_layout()
plt.show()

# ==========================================================
# 7. Analysis Output
# ==========================================================

print("\n--- PCA Results Summary ---")
print(f"Total Variance Explained by All Components: {total_variance:.2f}")
print("-" * 55)
print("| Component | Eigenvalue (Variance) | Variance Ratio |")
print("|-----------|-----------------------|----------------|")
for i in range(N_DIMENSIONS):
    print(f"| PC {i+1}     | {eigenvalues_sorted[i]:<21.4f} | {variance_ratio[i]*100:<14.2f}% |")

print("-" * 55)
print(f"Conclusion: PC1 and PC2 together account for {cumulative_variance[1]*100:.1f}% of the total variance, \nallowing the 3D system to be accurately reduced to a 2D plot.")
