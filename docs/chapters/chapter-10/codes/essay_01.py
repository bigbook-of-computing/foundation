import numpy as np

def solve_laplace(grid_size, boundary_conditions, max_iter=1000, tol=1e-4):
    u = np.zeros((grid_size, grid_size))
    # Apply boundary conditions...
    
    for _ in range(max_iter):
        u_next = u.copy()
        # Finite difference update
        u_next[1:-1, 1:-1] = 0.25 * (u[0:-2, 1:-1] + u[2:, 1:-1] + 
                                     u[1:-1, 0:-2] + u[1:-1, 2:])
        
        if np.max(np.abs(u_next - u)) < tol:
            break
        u = u_next
        
    return u
