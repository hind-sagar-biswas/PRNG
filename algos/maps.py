import numpy as np
import math

def gauss(
    x: float, alpha: float = 0.3, beta: float = -0.7
) -> float:  # a > 0 ; -1 < b < 1
    return np.exp(-alpha * x**2) + beta


def tent(x: float, mu: float = 1.7) -> float:  # 0 < x < 1 ; 1 < mu < 2
    return mu * x if x < 0.5 else mu * (1 - x)


def logistic(x: float, r: float = 3.99) -> float:
    return r * x * (1 - x)

def chebyshev(x, n):
    # Ensure x is in the valid range [-1, 1] for arccos.
    return 0.99 * math.cos(n * math.acos(x))