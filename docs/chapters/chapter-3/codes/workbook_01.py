import numpy as np


def f(x):
    return np.cos(x) - x


def df(x):
    return -np.sin(x) - 1.0
