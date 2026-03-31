import numpy as np

def gaussian_elimination(A, b):
    n = len(b)
    # Augment matrix
    Ab = np.hstack([A, b.reshape(-1, 1)])
    
    # Forward elimination
    for i in range(n):
        pivot = Ab[i, i]
        for j in range(i + 1, n):
            factor = Ab[j, i] / pivot
            Ab[j] -= factor * Ab[i]
            
    # Back substitution implementation would follow...
    return Ab
