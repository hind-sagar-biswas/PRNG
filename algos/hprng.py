import time

import algos.maps as mp
import numpy as np

"""
Parameters:
    m (int): Modulus value for the generator.
    n (int): Number of random numbers to generate.
    a (int): Exponent for scaling the multiplier.
    w (float): Worst case period percentage for seed switching

Returns:
    A list of n random numbers between 0 and m.
"""


def rotl(x: int, k: int, bits: int = 64) -> int:
    mask = (1 << bits) - 1
    return ((x << k) & mask) | (x >> (bits - k))


def mt19937(m: int, n: int, _: int, seed: int = 5489):
    # Initialize the state array with 624 32-bit integers.
    state = [0] * 624
    state[0] = seed & 0xFFFFFFFF
    for i in range(1, 624):
        state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF

    index = 624  # Force twist on first extraction

    def twist():
        nonlocal state, index
        for i in range(624):
            y = (state[i] & 0x80000000) + (state[(i + 1) % 624] & 0x7FFFFFFF)
            state[i] = state[(i + 397) % 624] ^ (y >> 1)
            if y & 1:
                state[i] ^= 0x9908B0DF
        index = 0

    def extract_number():
        nonlocal index, state
        if index >= 624:
            twist()
        y = state[index]
        # Tempering
        y ^= y >> 11
        y ^= (y << 7) & 0x9D2C5680
        y ^= (y << 15) & 0xEFC60000
        y ^= y >> 18
        index += 1
        return y & 0xFFFFFFFF

    # Generate n numbers (each reduced modulo m)
    return [extract_number() % (m + 1) for _ in range(n)]


def pcg(m: int, n: int, _: int, seed: int = 42, inc=1442695040888963407):
    mask = (1 << 64) - 1
    state = seed & mask
    multiplier = 6364136223846793005

    def next():
        nonlocal state
        state = (state * multiplier + inc) & mask
        xorshifted = (((state >> 18) ^ state) >> 27) & 0xFFFFFFFF
        rot = state >> 59
        # Perform a bitwise right rotation on xorshifted
        return ((xorshifted >> rot) | (xorshifted << ((-rot) & 31))) & 0xFFFFFFFF

    return [next() % (m + 1) for _ in range(n)]


def xorshift128plus(m: int, n: int, _: int, seed1: int = 123456789, seed2=362436069):
    mask = (1 << 64) - 1
    # Initialize state with two 64-bit values.
    s = [seed1 & mask, seed2 & mask]

    def next():
        nonlocal s
        s0 = s[0]
        s1 = s[1]
        result = (s0 + s1) & mask
        # Xorshift steps
        s1 ^= (s1 << 23) & mask
        s[0] = (s0 ^ s1 ^ (s1 >> 17) ^ (s0 >> 26)) & mask
        s[1] = s0
        return result

    return [next() % (m + 1) for _ in range(n)]


def well512a(m: int, n: int, _: int, seed: int = 123456789):
    # Initialize a state array of 16 32-bit unsigned integers.
    state = [0] * 16
    state[0] = seed & 0xFFFFFFFF
    for i in range(1, 16):
        state[i] = (1812433253 * (state[i - 1] ^ (state[i - 1] >> 30)) + i) & 0xFFFFFFFF
    index = 0

    def next():
        nonlocal index, state
        a = state[index]
        c = state[(index + 13) & 15]
        b = a ^ c ^ ((a << 16) & 0xFFFFFFFF) ^ ((c << 15) & 0xFFFFFFFF)
        c = state[(index + 9) & 15]
        c ^= c >> 11
        a = state[index] = (b ^ c) & 0xFFFFFFFF
        d = a ^ ((a << 5) & 0xDA442D24)
        index = (index + 15) & 15
        a = state[index]
        state[index] = (
            a
            ^ b
            ^ d
            ^ ((a << 2) & 0xFFFFFFFF)
            ^ ((b << 18) & 0xFFFFFFFF)
            ^ ((c << 28) & 0xFFFFFFFF)
        ) & 0xFFFFFFFF
        return state[index]

    return [next() % (m + 1) for _ in range(n)]


def splitmix64(m: int, n: int, _: int, seed: int = 42):
    mask = (1 << 64) - 1
    state = seed & mask

    def next():
        nonlocal state
        state = (state + 0x9E3779B97F4A7C15) & mask
        result = state
        result = (result ^ (result >> 30)) * 0xBF58476D1CE4E5B9
        result &= mask
        result = (result ^ (result >> 27)) * 0x94D049BB133111EB
        result &= mask
        return result ^ (result >> 31)

    return [next() % (m + 1) for _ in range(n)]


def tent_hybrid_3(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    t = (x % 1_000_000) / 1_000_000
    l = t
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        t = mp.tent(t, 2)
        l = mp.logistic(l, r=3.99)
        mix = int(t * 1_000_000) ^ int(l * 1_000_000)
        mix = rotl(mix, int(t * 64)) ^ rotl(x, int(l * 64))
        x = (mix ^ (x * a)) % (m + 1)
        random_numbers.append(x)
    return random_numbers


def chaos_hprng(m: int, n: int, a: int, w: float = 0.01):
    x = time.time_ns()
    worst_case_period = round(w * m)
    t = (x % 1_000_000) / 1_000_000
    l = t
    random_numbers = []
    for i in range(n):
        if i % worst_case_period == 0:
            x = time.time_ns()
        t = mp.tent(t, 2)
        l = mp.logistic(l, r=3.99)
        mix = int(t * 1_000_000) ^ int(l * 1_000_000)
        x = (mix ^ (x * a)) % (m + 1)
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
