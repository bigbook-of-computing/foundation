# Algorithm: Jacobi Relaxation

import numpy as np

def jacobi_relaxation(phi_old, tolerance=1e-6):
    # Initialize: phi_new[M, N], phi_old[M, N] (with boundaries)
    M, N = phi_old.shape
    phi_new = np.copy(phi_old)
    max_error = 1.0
    
    while max_error > tolerance:
        max_error = 0.0
        
        # 1. Calculate all new values using only old values
        for i in range(1, M-1):
            for j in range(1, N-1):
                phi_new[i,j] = 0.25 * (phi_old[i+1,j] + phi_old[i-1,j] + 
                                     phi_old[i,j+1] + phi_old[i,j-1])
        
        # 2. Check for convergence (compare new to old)
        for i in range(1, M-1):
            for j in range(1, N-1):
                error = abs(phi_new[i,j] - phi_old[i,j])
                if error > max_error:
                    max_error = error
                    
        # 3. Copy new to old for next iteration
        phi_old = np.copy(phi_new)
    
    return phi_new
