# Algorithm: Explicit FTCS for 1D Heat Equation

import numpy as np

def ftcs_heat_equation(T_present, D, h_x, h_t, N_steps):
    # Initialize: T_present[N], T_future[N] (with BCs)
    N = len(T_present)
    T_future = np.copy(T_present)
    alpha = D * h_t / (h_x * h_x)
    
    # Check stability *before* starting
    if alpha > 0.5:
        raise ValueError("Stability condition alpha <= 0.5 not met!")
    
    for n in range(N_steps):
        # Calculate all interior points for next timestep
        for i in range(1, N-1):
            T_future[i] = T_present[i] + alpha * (T_present[i+1] - 
                                                2*T_present[i] + 
                                                T_present[i-1])
        
        # Copy future to present for next iteration
        T_present = np.copy(T_future)
    
    return T_present
