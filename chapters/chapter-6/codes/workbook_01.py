# Infinite upper limit
scipy.integrate.quad(lambda x: np.exp(-x), 0, np.inf)

# Singularity at lower endpoint
scipy.integrate.quad(lambda x: 1/np.sqrt(x), 0, 1)
