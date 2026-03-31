# Algorithm: Linear Congruential Generator (LCG)

class LCG:
    def __init__(self, seed, a=1664525, c=1013904223, m=2**32):
        """
        Initialize a Linear Congruential Generator.
        
        Parameters:
        seed: initial seed value
        a: multiplier (default: 1664525)
        c: increment (default: 1013904223)
        m: modulus (default: 2^32)
        """
        self.a = a
        self.c = c
        self.m = m
        self.r_n = seed
    
    def get_next_random_int(self):
        self.r_n = (self.a * self.r_n + self.c) % self.m
        return self.r_n
    
    def get_next_random_float(self):
        return self.get_next_random_int() / self.m

# Example Monte Carlo simulation
import random

def monte_carlo_pi(num_samples):
    inside_circle = 0
    for _ in range(num_samples):
        x = random.random()
        y = random.random()
        if x**2 + y**2 <= 1:
            inside_circle += 1
            
    return (inside_circle / num_samples) * 4
