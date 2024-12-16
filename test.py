import os
import sys

sys.path.append("./algos")

import numpy as np
import sqlite3 as sq
from scipy.stats import kstest, chisquare

import dbconn as db
import visualize as vis
import algos.hprng as alg

ALPHA = 0.05
N = 1000

algo_list = {
    "hybrid": alg.hybrid_prng,
    "mask": alg.mask_prng,
    "mask_shift": alg.mask_shift_prng,
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


def conduct_test(m: int, algorithm):
    numbers = algorithm(m, N)
    return {
        "ks": ks(numbers),
        "chi": chi(numbers),
        "numbers": numbers,
    }


def start_tests(algo_list: dict, conn: sq.Connection):
    for key, value in algo_list.items():
        m = 100
        while m < 1000000000000:
            print("=" * 50)
            print(f"Testing {key} with m = {m}")
            stats = conduct_test(m, value)
            stats = db.generate_entry(stats, key, m, N, ALPHA)
            print("Entering values")
            db.enter_values(stats, conn)
            m *= 10
            print("=" * 50)


def main():
    if os.path.exists("test.db"):
        os.remove("test.db")

    conn = sq.connect("test.db")
    print("Opened database successfully")

    db.setup_table(conn)
    start_tests(algo_list, conn)

    conn.close()


if __name__ == "__main__":
    main()
    vis.main(algo_list)
