# Algorithm: FTCS for 1D Wave Equation (Main Loop)

import numpy as np

def wave_equation_ftcs(y_present, y_past, v, h_t, h_x, N_steps):
    # (Assumes y_present (n) and y_past (n-1) are known)
    N = len(y_present)
    C = v * h_t / h_x
    C_squared = C * C
    
    y_future = np.copy(y_present)
    
    for step in range(N_steps):
        for i in range(1, N-1):  # (Iterate over interior points)
            # Calculate spatial curvature (Laplacian)
            laplacian_y = y_present[i+1] - 2*y_present[i] + y_present[i-1]
            
            # Apply the "Verlet" recurrence relation
            y_future[i] = 2*y_present[i] - y_past[i] + C_squared * laplacian_y
        
        # (Boundaries y_future[0] and y_future[N-1] are set by BCs)
        
        # Update for next iteration
        y_past = np.copy(y_present)
        y_present = np.copy(y_future)
    
    return y_present
    u = u0.copy()
    u_old = u_prev.copy()
    
    r = (c * dt / dx)**2
    
    for n in range(nt):
        u_new = np.zeros_like(u)
        for i in range(1, nx-1):
            u_new[i] = 2*u[i] - u_old[i] + r * (u[i+1] - 2*u[i] + u[i-1])
        u_old = u.copy()
        u = u_new.copy()
        
    return u
