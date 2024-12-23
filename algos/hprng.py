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
