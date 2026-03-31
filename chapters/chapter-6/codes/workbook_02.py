           def transformed_integrand(t):
               return (1/t**2) * np.exp(-(1-t)/t)
           
           result, error = scipy.integrate.quad(transformed_integrand, 0, 1)
