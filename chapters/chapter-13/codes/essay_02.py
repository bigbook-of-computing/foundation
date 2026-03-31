# Algorithm: Thomas Algorithm (Tridiagonal Solver)

import numpy as np

def thomas_algorithm(a, b, c, d):
    """
    Solve a tridiagonal system using the Thomas algorithm.
    
    Parameters:
    a: lower diagonal (N-1 elements, a[0] is not used)
    b: main diagonal (N elements)
    c: upper diagonal (N-1 elements, c[N-1] is not used)
    d: RHS vector (N elements)
    
    Returns:
    x: solution vector (N elements)
    """
    N = len(d)
    c_prime = np.zeros(N)
    d_prime = np.zeros(N)
    
    # 1. Forward Elimination Pass (O(N))
    # Modify coefficients and RHS
    c_prime[0] = c[0] / b[0]
    d_prime[0] = d[0] / b[0]
    
    for i in range(1, N):
        temp = b[i] - a[i] * c_prime[i-1]
        c_prime[i] = c[i] / temp if i < N-1 else 0
        d_prime[i] = (d[i] - a[i] * d_prime[i-1]) / temp
    
    # 2. Backward Substitution Pass (O(N))
    # The solution vector is x (or d_prime)
    for i in range(N-2, -1, -1):
        d_prime[i] = d_prime[i] - c_prime[i] * d_prime[i+1]
    
    # Solution is now in the d_prime array
    return d_prime
