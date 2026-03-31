import numpy as np

rng = np.random.default_rng(123)

# Clean reference signal
x_clean = np.linspace(0.0, 6.0, 25)
y_clean = np.sin(x_clean)

# Noisy observation set
noise_sigma = 0.12
y_noisy = y_clean + noise_sigma * rng.standard_normal(len(x_clean))

print("N samples:", len(x_clean))
print("Noise sigma:", noise_sigma)
print("y mean:", float(np.mean(y_noisy)))
print("y std:", float(np.std(y_noisy)))
