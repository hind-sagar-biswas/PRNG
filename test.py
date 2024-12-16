import os
import sys

sys.path.append("./algos")

import threading
import numpy as np
import sqlite3 as sq
from scipy.stats import kstest, chisquare

import dbconn as db
import visualize as vis
import algos.hprng as alg

ALPHA = 0.05
N = 1000

algo_list = {
    "hybrid": alg.hybrid_prng,  # 2nd
    "switch": alg.switch_prng,  # 1st
    # "mask": alg.mask_prng,  # Worst Performance
    # "alt_mask": alg.mask_alt_prng,  # Worst Performance
    # "mask_shift": alg.mask_shift_prng,  # Performance worse than Alt.
    # "switch_mask_shift": alg.switch_mask_shift_prng,  # Worst Performance
    "alt_mask_shift": alg.mask_shift_alt_prng,
}


def ks(numbers: list):
    D, p_value = kstest(numbers, "uniform")
    return D, p_value, int(p_value < ALPHA)


def chi(numbers):
    k = 10  # Number of bins
    bins = np.linspace(0, 1, k + 1)  # Define bin edges
    observed, _ = np.histogram(numbers, bins)  # Observed frequencies
    expected = [N / k] * k  # Expected frequencies

    # Perform the Chi-Square test
    chi2_stat, p_value = chisquare(observed, expected)
    return chi2_stat, p_value, int(p_value < ALPHA)


def conduct_test(m: int, a: int, algorithm):
    numbers = algorithm(m, N, a)
    return {
        "ks": ks(numbers),
        "chi": chi(numbers),
        "numbers": numbers,
    }


def start_tests(algo_list: dict, index: int, conn: sq.Connection):
    for key, value in algo_list.items():
        m = 100
        while m < 1000000000000:
            print("=" * 50)
            print(f"Testing {key} with m = {m}")
            stats = conduct_test(m, index, value)
            stats = db.generate_entry(stats, key, m, N, ALPHA)
            print("Entering values")
            db.enter_values(stats, conn)
            m *= 10
            print("=" * 50)


def main(index: int = 0):
    if os.path.exists(f"test_{index}.db"):
        os.remove(f"test_{index}.db")

    conn = sq.connect(f"test_{index}.db")
    print("Opened database successfully")

    db.setup_table(conn)
    start_tests(algo_list, index, conn)

    conn.close()


if __name__ == "__main__":
    only_rejections = bool(int(input("Only Rejections (1 = True, 0 = False): ")))
    threads = int(input("Number of Threads: "))
    t = []
    for i in range(threads):
        thread = threading.Thread(target=main, args=(i,))
        thread.start()
        t.append(thread)

    for thread in t:
        thread.join()
    for i in range(threads):
        vis.main(algo_list, i, only_rejections)
