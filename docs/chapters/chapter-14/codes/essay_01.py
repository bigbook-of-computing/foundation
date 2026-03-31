# Algorithm: The Power Method

import numpy as np

def power_method(A, x_k=None, tolerance=1e-9, max_iterations=1000):
    """
    Find the largest eigenvalue and corresponding eigenvector using the power method.
    
    Parameters:
    A: square matrix
    x_k: initial guess vector (random if None)
    tolerance: convergence tolerance
    max_iterations: maximum number of iterations
    
    Returns:
    lambda_max: largest eigenvalue
    x_k: corresponding eigenvector
    """
    if x_k is None:
        x_k = np.random.rand(A.shape[0])
    
    x_k = x_k / np.linalg.norm(x_k)
    
    for i in range(max_iterations):
        x_k_plus_1 = A @ x_k
        x_k_plus_1 = x_k_plus_1 / np.linalg.norm(x_k_plus_1)
        
        if np.linalg.norm(x_k_plus_1 - x_k) < tolerance:
            break
        
        x_k = x_k_plus_1
    
    lambda_max = (x_k.T @ A @ x_k) / (x_k.T @ x_k)
    return lambda_max, x_k
