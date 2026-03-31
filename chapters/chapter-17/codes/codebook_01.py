
import numpy as np
import matplotlib.pyplot as plt

# Set a seed for reproducibility (a core principle of PRNGs)
np.random.seed(42)

# ==========================================================
# Chapter 17 Codebook: Randomness in Physics
# Project 1: The Random Walk (Microscopic Diffusion)
# ==========================================================

# ==========================================================
# 1. Setup Parameters
# ==========================================================

N_STEPS = 1000       # Total steps in each walk (time t)
N_WALKERS = 5000     # Number of walkers (ensemble average)

# Time points to record the RMS displacement
time_indices = np.arange(0, N_STEPS, 50) 
time_indices[0] = 1 # Start from step 1 to avoid log(0) issues

# ==========================================================
# 2. Simulate the Random Walk Ensemble
# ==========================================================

# Array to store the final positions of all walkers after N_STEPS
final_positions = np.zeros(N_WALKERS)

# Array to store the squared displacement (x²) over time, averaged across walkers
mean_sq_displacement_history = np.zeros(len(time_indices))

# Loop over the ensemble of walkers
for w in range(N_WALKERS):
    # Steps array: +1 or -1
    # np.random.choice([1, -1], size=N_STEPS) efficiently generates the steps
    steps = np.random.choice([1, -1], size=N_STEPS)
    
    # Calculate the cumulative displacement (position x) over time
    positions = np.cumsum(steps)
    final_positions[w] = positions[-1]
    
    # Store the square of the displacement for the RMS average
    for i, t_idx in enumerate(time_indices):
        mean_sq_displacement_history[i] += positions[t_idx - 1]**2

# Calculate the ensemble average: divide the sum of squares by the number of walkers
mean_sq_displacement_history /= N_WALKERS

# Calculate the Root Mean Square (RMS) displacement
rms_displacement_history = np.sqrt(mean_sq_displacement_history)

# ==========================================================
# 3. Visualization and Analysis (Verifying the sqrt(t) law)
# ==========================================================

fig, ax = plt.subplots(figsize=(8, 5))

# Plot the computed RMS displacement
ax.plot(time_indices, rms_displacement_history, 'b-o', markersize=3, label="Simulated RMS Displacement")

# Plot the theoretical prediction: RMS ∝ sqrt(t)
# Theory: RMS = sqrt(t), so we plot y = sqrt(x)
ax.plot(time_indices, np.sqrt(time_indices), 'r--', label=r"Theoretical $\Delta x_{\text{RMS}} \propto \sqrt{t}$")

ax.set_title(r"1D Random Walk: Verification of $\Delta x_{\text{RMS}} \propto \sqrt{t}$")
ax.set_xlabel("Time (Number of Steps $t$)")
ax.set_ylabel(r"Root Mean Square Displacement $\Delta x_{\text{RMS}}$")
ax.grid(True)
ax.legend()
plt.tight_layout()
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================

# Final check of the predicted vs. observed relationship
final_t = time_indices[-1]
final_rms_observed = rms_displacement_history[-1]
final_rms_theoretical = np.sqrt(final_t)

print("\n--- Random Walk Analysis Summary ---")
print(f"Total Walkers Simulated: {N_WALKERS}")
print(f"Total Steps (t_final): {final_t}")
print("-" * 40)
print(f"Observed Final RMS Displacement: {final_rms_observed:.4f}")
print(f"Theoretical Final RMS Displacement: {final_rms_theoretical:.4f}")
print(f"Relative Error: {np.abs(final_rms_observed - final_rms_theoretical) / final_rms_theoretical:.2e}")

print("\nConclusion: The simulation confirms the fundamental law of diffusion: the observed \nRMS displacement closely follows the square root of time, validating the random walk \nas a stochastic model for diffusion.")
