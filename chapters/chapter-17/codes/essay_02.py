# Algorithm: 1D Random Walk

import random

def random_walk_1d(N_steps=1000):
    """
    Simulate a 1D random walk.
    
    Parameters:
    N_steps: number of steps to take
    
    Returns:
    path: list of positions at each step
    """
    x = 0
    path = [x]
    
    for i in range(N_steps):
        r = random.random()
        
        if r < 0.5:
            x = x + 1
        else:
            x = x - 1
        
        # Store x in the array to plot the path
        path.append(x)
    
    return path
