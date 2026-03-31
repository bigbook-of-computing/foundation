def runge_kutta_4(f, y0, t0, t_end, h):
    t_values = [t0]
    y_values = [y0]
    
    t = t0
    y = y0
    
    while t < t_end:
        k1 = h * f(t, y)
        k2 = h * f(t + 0.5*h, y + 0.5*k1)
        k3 = h * f(t + 0.5*h, y + 0.5*k2)
        k4 = h * f(t + h, y + k3)
        
        y += (k1 + 2*k2 + 2*k3 + k4) / 6.0
        t += h
        t_values.append(t)
        y_values.append(y)
        
    return t_values, y_values

# Algorithm: Basic Störmer-Verlet

# Initialize: x[0], x[1] (requires a special startup step, e.g., Euler)
# Initialize: h (timestep)

def stormer_verlet(x0, x1, h, F, m, N_steps):
    x = [x0, x1]
    a = [F(x[0]) / m, F(x[1]) / m]
    
    for n in range(1, N_steps - 1):
        # Verlet position update
        x_next = 2 * x[n] - x[n-1] + h * h * a[n]
        x.append(x_next)
        
        # Update acceleration for next step
        a_next = F(x[n+1]) / m
        a.append(a_next)
    
    return x
