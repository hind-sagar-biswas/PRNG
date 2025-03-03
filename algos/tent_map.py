import time


def tent_map(m: int, n: int, _):
    mu = 0.5
    x = (time.time_ns() % 1_000_000) / 1_000_000
    random_numbers = []
    for i in range(n):
        if x < 0.5:
            x = mu * x
        else:
            x = mu * (1 - x)
        random_numbers.append(x % (m + 1))
    return random_numbers
