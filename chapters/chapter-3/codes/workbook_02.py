import numpy as np


def g(x):
    # Flat near root region to stress residual-only logic
    return (x - 1.0) ** 7
