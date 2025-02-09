import numpy as np
import time

"""
Parameters:
    m (int): Modulus value for the generator.
    n (int): Number of random numbers to generate.
    a (int): Exponent for scaling the multiplier.
    w (float): Worst case period percentage for seed switching

Returns:
    A list of n random numbers between 0 and m.
"""


def tent(x: float, mu: float = 0.5) -> float:  # 0 < x < 1 ; 1 < mu < 2
    return mu * x if x < 0.5 else mu * (1 - x)


def gauss(
    x: float, alpha: float = 0.3, beta: float = -0.7
) -> float:  # a > 0 ; -1 < b < 1
    return np.exp(-alpha * x**2) + beta


def tent_hybrid(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    tnt = (x % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 * np.exp(tnt) + (x * a)) % (m + 1)
        tnt = tent(tnt)
        random_numbers.append(x)
    return random_numbers


def tent_hybrid_2(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    tnt = (x % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n * np.exp(tnt) + (x * a)) % (m + 1)
        tnt = tent(tnt)
        random_numbers.append(x)
    return random_numbers


def gauss_hybrid(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    g_var = (x % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 * np.exp(g_var) + (x * a)) % (m + 1)
        g_var = gauss(g_var)
        random_numbers.append(x)
    return random_numbers


def gauss_hybrid_2(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    g_var = (x % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n * np.exp(g_var) + (x * a)) % (m + 1)
        g_var = gauss(g_var)
        random_numbers.append(x)
    return random_numbers


def switch_prng(m, n, a, w=0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x * a)) % (m + 1)
        random_numbers.append(x)
    return random_numbers


def switch_shift_prng(m, n, a, w=0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x * a) << 5) % (
            m + 1
        )  # Use of Higher shift value improves performance
        random_numbers.append(x)
    return random_numbers


def switch_mask_shift_prng(m, n, a, w=0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x ^ a) << 5) % (m + 1)
        random_numbers.append(x)
    return random_numbers


def hybrid_prng(m, n, a):
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + a * x) % (m + 1)
        random_numbers.append(x)
    return random_numbers
