import time


def hybrid_prng(m, n):
    a = 5
    x = time.time_ns()
    random_numbers = []
    for _ in range(n):
        x = (n**2 + a * x) % (m + 1)
        random_numbers.append(x / (m + 1))  # Normalize to [0, 1]
    return random_numbers
