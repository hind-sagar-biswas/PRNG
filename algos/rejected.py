import time
import maps as mp

INT_BITS = 64


def leftRotate(n, d):
    return (n << d) | (n >> (INT_BITS - d))

def tent_hybrid(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    tnt = (x % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 * np.exp(tnt) + (x * a)) % (m + 1)
        tnt = mp.tent(tnt)
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
        tnt = mp.tent(tnt)
        random_numbers.append(x)
    return random_numbers


def tent_hybrid_5(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    t = (x % 1_000_000) / 1_000_000
    l = t
    random_numbers = []
    for i in range(n):
        t = mp.tent(t, 2)
        l = mp.logistic(l, r=3.99)
        mix = int(t * 1_000_000) ^ int(l * 1_000_000)
        x = (mix ^ (x * a)) % (m + 1)
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
        g_var = mp.gauss(g_var)
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
        g_var = mp.gauss(g_var)
        random_numbers.append(x)
    return random_numbers


def gauss_map_prng(m: int, size: int, _):
    sequence = []
    state = (time.time_ns() % 1_000_000) / 1_000_000
    alpha = 4.9 + (state * 0.001)
    beta = 0.5
    for _ in range(size):
        state = (np.exp(-alpha * state**2) + beta) % (m + 1)
        sequence.append(state)
    return sequence


def shift_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x * a) << 5) % (m + 1)
        random_numbers.append(x)
    return random_numbers


def switch_shift_rotate_alt_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(0.01 * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + leftRotate((x * a) << 5, 7)) % (
            m + 1
        )  # Use of Higher shift value improves performance
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def switch_shift_rotate_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(0.01 * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = leftRotate((n**2 + (x * a) << 5), 7) % (
            m + 1
        )  # Use of Higher shift value improves performance
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def xor_hprng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = ((n**2) ^ (x * a)) % (m + 1)
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


def shift_rotate_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = leftRotate((n**2 + (x * a) << 5), 7) % (
            m + 1
        )  # Use of Higher shift value improves performance
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def mask_shift_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ a) << 5) % (m + 1)
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


def mask_shift_alt_prng(m, n, a):
    a = 5 * (10**a)
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + (x ^ n) << 5) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers


def switch_mask_shift_alt_prng(m, n, a, worst_case_period=0.01):
    a = 5 * (10**a)
    x = time.time_ns()
    worst_case_period = round(worst_case_period * m)  # worst case period: 1% of m
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        x = (n**2 + (x ^ a) << 5) % (m + 1)
        random_numbers.append(x)
    return random_numbers
