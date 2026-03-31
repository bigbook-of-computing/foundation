
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft

# ==========================================================
# Chapter 15 Codebook: Fourier Analysis & The FFT
# Project 2: Spectral Filtering (Noise Reduction)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Generate Noisy Signal (Reuse P1 Data)
# ==========================================================

FS = 1000       # Sampling rate (Hz)
T_DURATION = 1.0
N = int(FS * T_DURATION)
F1 = 5.0        # Signal 1
F2 = 30.0       # Signal 2
time = np.linspace(0, T_DURATION, N, endpoint=False)
signal_true = 2.0 * np.sin(2.0 * np.pi * F1 * time) + 0.5 * np.sin(2.0 * np.pi * F2 * time)
NOISE_STD = 0.5
signal_noisy = signal_true + NOISE_STD * np.random.randn(N)

# ==========================================================
# 2. Compute FFT and Define Filter
# ==========================================================

Y = fft(signal_noisy)
f_k = fftfreq(N, 1/FS)

# Define the cutoff frequency for the low-pass filter (Hz)
# We choose a value above F2 (30 Hz) but well below the Nyquist (500 Hz).
F_CUTOFF = 50.0 

# Create a mask: True for frequencies we want to KEEP, False for those to filter out
# Filtering mask must be symmetric around the DC (f=0) component
filter_mask = np.abs(f_k) < F_CUTOFF

# Create the filtered spectrum by zeroing out coefficients outside the cutoff range
Y_filtered = Y * filter_mask

# ==========================================================
# 3. Compute Inverse FFT (IFFT)
# ==========================================================

# Use the Inverse FFT to return the clean signal to the time domain
# The result of the IFFT is inherently complex, so we take the real part.
signal_clean = np.real(ifft(Y_filtered))

# ==========================================================
# 4. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))
time_window = time[0:200] # Plot first 20% of the data for clarity

# --- Plot 1: Time Domain Filter Comparison ---
ax[0].plot(time_window, signal_noisy[0:200], 'r-', alpha=0.5, label="1. Noisy Input")
ax[0].plot(time_window, signal_clean[0:200], 'b-', linewidth=2, label=f"2. Filtered Output (Cutoff: {F_CUTOFF} Hz)")
ax[0].plot(time_window, signal_true[0:200], 'k--', alpha=0.7, label="3. True Signal (Hidden)")

ax[0].set_title(f"Time Domain: Noise Reduction (Low-Pass Filter at {F_CUTOFF} Hz)")
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Amplitude")
ax[0].grid(True)
ax[0].legend()

# --- Plot 2: Spectrum Comparison (Before/After Filter) ---
power_noisy = np.abs(Y)**2
power_filtered = np.abs(Y_filtered)**2
positive_f_mask = f_k >= 0

ax[1].semilogy(f_k[positive_f_mask], power_noisy[positive_f_mask], 'r-', alpha=0.6, label="Noisy Spectrum")
ax[1].semilogy(f_k[positive_f_mask], power_filtered[positive_f_mask], 'b-', linewidth=2, label="Filtered Spectrum")

ax[1].axvline(F_CUTOFF, color='k', linestyle='--', label="Cutoff Frequency")

ax[1].set_title("Frequency Domain: Filter Action (Power)")
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_ylabel("Power ($\log_{10}$ Scale)")
ax[1].grid(True)
ax[1].legend()

plt.tight_layout()
plt.show()

# Final Analysis
print("\n--- Spectral Filtering Summary ---")
print(f"Cutoff Frequency: {F_CUTOFF} Hz")
print(f"Original RMS Error (vs. True Signal): {np.sqrt(np.mean((signal_noisy - signal_true)**2)):.4f}")
print(f"Filtered RMS Error (vs. True Signal): {np.sqrt(np.mean((signal_clean - signal_true)**2)):.4f}")
print("\nConclusion: The filtering process successfully reduced the high-frequency components, resulting in a significantly lower RMS error and a cleaner signal in the time domain.")
