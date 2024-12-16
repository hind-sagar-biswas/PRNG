import time


def hybrid_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + a * x) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def mask_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ a)) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def mask_alt_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ n)) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def mask_shift_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ a) << 1) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def mask_shift_alt_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ n) << 1) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def switch_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(0.01 * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x * a)) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def switch_shift_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(0.01 * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x * a) << 5) % (
            m + 1
        )  # Use of Higher shift value improves performance
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def switch_mask_shift_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(0.01 * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x ^ a) << 1) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers
