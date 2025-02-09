import os
import sqlite3 as sq
import sys
import threading
import timeit
from pathlib import Path

import numpy as np
from dotenv import dotenv_values
from scipy.stats import chisquare, kstest

# Append the directory containing algorithm implementations to the path
sys.path.append("./algos")

import algos.hprng as alg  # Hybrid PRNG algorithms
import dbconn as db  # Database-related operations
import visualize as vis  # Visualization functions

# Create test result directory:
Path("./results").mkdir(parents=True, exist_ok=True)

# Load environment variables for configuration
config = dotenv_values("env.config")

# Parameters loaded from environment variables
M_MULTIPLIER = int(config["M_MULTIPLIER"])
M_INITIAL = int(config["M_INITIAL"])
M_LIMIT = int(config["M_LIMIT"])
ALPHA = float(config["ALPHA"])
N = int(config["N"])

# Dictionary of algorithms with their respective functions
algo_list = {
    "hybrid": alg.hybrid_prng,  # Hybrid PRNG
    "switch": alg.switch_prng,  # Switch-based PRNG
    "switch shift": alg.switch_shift_prng,  # Switch + Shift PRNG
    "switch mask shift": alg.switch_mask_shift_prng,  # Switch + Mask + Shift PRNG
}


# Normalize random numbers to [0, 1] range
def normalize(random_nums: list, m: int):
    return [num / (m + 1) for num in random_nums]


# Perform Kolmogorov-Smirnov (K-S) test on a dataset
def ks(numbers: list):
    D, p_value = kstest(numbers, "uniform")
    # Return test statistic, p-value, and rejection status
    return D, p_value, int(p_value < ALPHA)


# Perform Chi-Square test on a dataset
def chi(numbers):
    k = 10  # Number of bins
    bins = np.linspace(0, 1, k + 1)  # Define bin edges
    observed, _ = np.histogram(numbers, bins)  # Observed frequencies
    expected = [N / k] * k  # Expected frequencies

    # Perform the Chi-Square test
    chi2_stat, p_value = chisquare(observed, expected)
    # Return test statistic, p-value, and rejection status
    return chi2_stat, p_value, int(p_value < ALPHA)


# Conduct tests (K-S and Chi-Square) for a specific algorithm
def conduct_test(m: int, a: int, algorithm):
    a = 5 * (10**a)  # Scale 'a' by a factor
    numbers = algorithm(m, N, a)  # Generate random numbers using the algorithm
    numbers = normalize(numbers, m)  # Normalize the numbers
    total_time = timeit.timeit(
        lambda: algorithm(m, N, a), number=100
    )  # Time the algorithm
    time_per_execution = total_time / 100  # Calculate the average time per execution

    return {
        "ks": ks(numbers),
        "chi": chi(numbers),
        "numbers": numbers,
        "time": time_per_execution,
    }


# Run tests for all algorithms and store results in the database
def start_tests(algo_list: dict, index: int, conn: sq.Connection):
    for key, value in algo_list.items():
        m = M_INITIAL  # Start with the initial value of 'm'
        while m <= M_LIMIT:
            print("=" * 50)
            print(f"Testing {key} with m = {m}")

            # Conduct tests and generate database entry
            stats = conduct_test(m, index, value)
            stats = db.generate_entry(stats, key, m, N, ALPHA)
            print("Entering values")

            # Insert test results into the database
            db.enter_values(stats, conn)
            m *= M_MULTIPLIER  # Increment 'm' by the multiplier
            print("=" * 50)


# Main function to initialize the database and run tests
def tester(index: int = 0):
    # Remove existing database if it exists
    if os.path.exists(f"./results/test_{index}.db"):
        os.remove(f"./results/test_{index}.db")

    # Connect to a new SQLite database
    conn = sq.connect(f"./results/test_{index}.db")
    print("Opened database successfully")

    # Setup database tables and start tests
    db.setup_table(conn)
    start_tests(algo_list, index, conn)

    conn.close()


def main():
    # Get the number of threads from the user
    threads = int(input("Number of Threads: "))
    t = []

    # Create and start threads for parallel testing
    for i in range(threads):
        thread = threading.Thread(target=tester, args=(i,))
        thread.start()
        t.append(thread)

    # Wait for all threads to complete
    for thread in t:
        thread.join()

    # Prompt user for visualization options
    print("Select to Visualize Data: ")
    print("\t[0] All")
    print("\t[1] Statistics")
    print("\t[2] P Values")
    print("\t[3] Rejections Heatmap")
    print("\t[4] Random Numbers Distribution")
    print("\t[5] Execution Time")

    allowed = {0, 1, 2, 3, 4, 5}
    selected = set(map(int, input(">> ").split())).intersection(allowed)

    if 0 in selected:
        selected = allowed - {0}

    # Visualize results for each thread's data
    for i in range(threads):
        vis.main(algo_list, i, selected)


# Entry point for the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting tests...")
