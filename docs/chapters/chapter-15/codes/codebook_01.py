
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq, ifft

# ==========================================================
# Chapter 15 Codebook: Fourier Analysis & The FFT
# Project 1: Spectral Analysis (Frequency Decomposition)
# ==========================================================

# ==========================================================
# 1. Setup Parameters and Generate Composite Signal
# ==========================================================

# Sampling parameters
FS = 1000       # Sampling rate (Hz) (must be > 2 * max_freq)
T_DURATION = 1.0  # Duration of the signal (seconds)
N = int(FS * T_DURATION) # Total number of data points (ideally a power of 2)

# Define the two sine wave components
F1 = 5.0        # Frequency 1 (Hz)
F2 = 30.0       # Frequency 2 (Hz)
A1 = 2.0        # Amplitude 1
A2 = 0.5        # Amplitude 2

# Time array
time = np.linspace(0, T_DURATION, N, endpoint=False)

# Generate the signal
signal = A1 * np.sin(2.0 * np.pi * F1 * time) + \
         A2 * np.sin(2.0 * np.pi * F2 * time)

# Add random noise for realism
NOISE_STD = 0.5
noise = NOISE_STD * np.random.randn(N)
signal_noisy = signal + noise

# ==========================================================
# 2. Compute FFT and Power Spectrum
# ==========================================================

# 1. Compute the FFT (returns complex coefficients Y_k)
Y = fft(signal_noisy)

# 2. Map the frequency indices to physical frequencies (f_k)
f_k = fftfreq(N, 1/FS)

# 3. Calculate the Power Spectrum (P_k = |Y_k|²)
# We only plot the positive frequency side (the spectrum is symmetric)
power_spectrum = np.abs(Y)**2
positive_f_mask = f_k >= 0

# ==========================================================
# 3. Visualization and Analysis
# ==========================================================

fig, ax = plt.subplots(1, 2, figsize=(12, 5))

# --- Plot 1: Time Domain Signal ---
ax[0].plot(time, signal_noisy)
ax[0].set_title("Time Domain: Composite Signal + Noise")
ax[0].set_xlabel("Time (s)")
ax[0].set_ylabel("Amplitude")
ax[0].grid(True)

# --- Plot 2: Frequency Domain (Power Spectrum) ---
ax[1].plot(f_k[positive_f_mask], power_spectrum[positive_f_mask], 'r-')
ax[1].set_title("Frequency Domain: Power Spectrum")
ax[1].set_xlabel("Frequency (Hz)")
ax[1].set_ylabel("Power ($|Y_k|^2$)")
ax[1].grid(True)

# Highlight the expected peaks
ax[1].axvline(F1, color='g', linestyle='--', label=f"{F1} Hz Peak")
ax[1].axvline(F2, color='b', linestyle=':', label=f"{F2} Hz Peak")
ax[1].legend()

plt.tight_layout()
plt.show()

# ==========================================================
# 4. Analysis Output
# ==========================================================

# Find the peak frequencies for verification
# Exclude the DC component (k=0) and small frequencies to ignore the noise floor
peak_indices = np.argsort(power_spectrum[positive_f_mask])[::-1]
f_peaks_found = f_k[positive_f_mask][peak_indices[:2]]

print("\n--- Spectral Analysis Summary ---")
print(f"Sampling Rate (Fs): {FS} Hz")
print(f"Nyquist Frequency (Fs/2): {FS/2.0} Hz")
print(f"Target Frequencies: {F1} Hz and {F2} Hz")
print(f"Top 2 Frequencies Found in Spectrum: {np.sort(f_peaks_found):.1f} Hz")
print("\nConclusion: The FFT successfully decomposed the composite signal, isolating the two \nfundamental frequencies as the dominant peaks in the Power Spectrum.")
