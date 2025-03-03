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
import binaryGen as gen  # Binary file generation
import compilattion as cmp  # Compilattion
import extern.collect as clct  # External Library tests

# Load environment variables for configuration
config = dotenv_values("env.config")

# Parameters loaded from environment variables
M_MULTIPLIER = int(config["M_MULTIPLIER"] or 1)
M_INITIAL = int(config["M_INITIAL"] or 1)
M_LIMIT = int(config["M_LIMIT"] or 1)
ALPHA = float(config["ALPHA"] or 0.05)
N = int(config["N"] or 1000)
RESULTS_DIR = config["RESULTS_DIR"] or "./results"
BIN_DIR = config["BIN_DIR"] or "/bin"
DB_DIR = config["DB_DIR"] or "/db"

# Create test result directory:
Path(RESULTS_DIR + DB_DIR).mkdir(parents=True, exist_ok=True)
Path(RESULTS_DIR + BIN_DIR).mkdir(parents=True, exist_ok=True)

# Dictionary of algorithms with their respective functions
algo_list = {
    "hybrid": alg.hybrid_prng,  # Hybrid PRNG
    # "switch": alg.switch_prng,    # Switch-based PRNG
    # "chprng": alg.tent_hybrid_3,  # Tent-based PRNG version 03
    # "tent 4": alg.tent_hybrid_4,  # Tent-based PRNG version 04
    # "tent 5": alg.tent_hybrid_5,  # Tent-based PRNG version 05
    # "mt19937": alg.mt19937,  # Mersenne Twister
    # "pcg": alg.pcg,  # PCG
    # "xorshift128plus": alg.xorshift128plus,  # Xorshift128+
    # "well512a": alg.well512a,  # Well512a
    # "splitmix64": alg.splitmix64,  # Splitmix64
}


# Normalize random numbers to [0, 1] range
def normalize(random_nums: list, m: int) -> list:
    return [num / (m + 1) for num in random_nums]


# Perform Kolmogorov-Smirnov (K-S) test on a dataset
def ks(numbers: list[float]) -> tuple:
    D, p_value = kstest(numbers, "uniform")
    # Return test statistic, p-value, and rejection status
    return D, p_value, int(p_value < ALPHA)


# Perform Chi-Square test on a dataset
def chi(numbers: list[float]) -> tuple:
    k = 10  # Number of bins
    bins = np.linspace(0, 1, k + 1)  # Define bin edges
    observed, _ = np.histogram(numbers, bins)  # Observed frequencies
    expected = [N / k] * k  # Expected frequencies

    # Perform the Chi-Square test
    chi2_stat, p_value = chisquare(observed, expected)
    # Return test statistic, p-value, and rejection status
    return chi2_stat, p_value, int(p_value < ALPHA)


# Conduct tests (K-S and Chi-Square) for a specific algorithm
def conduct_test(m: int, a: int, algorithm) -> dict:
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


# Conduct tests for external libraries
def conduct_external_test() -> dict[str, dict]:
    extern_dir = Path("./extern")
    data = clct.main(
        N,
        {
            "C": f"gcc {extern_dir}/gcc/rand.c -o {extern_dir}/gcc/rand.out && {extern_dir}/gcc/rand.out",
            "C++": f"g++ {extern_dir}/gcc/rand.cpp -o {extern_dir}/gcc/rand.out && {extern_dir}/gcc/rand.out",
            "Rust": f"cd {extern_dir}/rust && cargo run --release --",
            "JS": f"node {extern_dir}/rand.js",
            "Java": f"javac {extern_dir}/java/Rand.java && java -cp {extern_dir}/java Rand",
            "PHP": f"php {extern_dir}/rand.php",
        },
    )

    results = {}

    for key, value in data.items():
        results[key] = {
            "ks": ks(value),
            "chi": chi(value),
            "numbers": value,
            "time": 0,
        }

    return results


# Run tests for all algorithms and store results in the database
def start_tests(
    algo_list: dict, index: int, conn: sq.Connection, generate_binary: bool
) -> None:
    th = f"[THREAD {index:03}]\t"
    for key, value in algo_list.items():
        m = M_INITIAL  # Start with the initial value of 'm'
        while m <= M_LIMIT:
            print(th + "=" * 50)
            print(f"{th}Testing {key} with m = {m}")

            # Conduct tests and generate database entry
            stats = conduct_test(m, index, value)

            # Generate binary file
            if generate_binary:
                print(f"{th}Generating Binary Files")
                gen.generate_binary_file(
                    f"{RESULTS_DIR + BIN_DIR}/test_{index}_{key}_{m}.bin",
                    stats["numbers"],
                )
                print(f"{th}Generated Binary Files for {key} with m = {m}")

            # Generate database entry
            stats = db.generate_entry(stats, key, m, N, ALPHA)

            # Insert test results into the database
            print(f"{th}Entering values into database for {key} with m = {m}")
            db.enter_values(stats, conn)
            print(f"{th}Values entered successfully")

            m *= M_MULTIPLIER  # Increment 'm' by the multiplier
            print(f"[THREAD {index:03}]\t" + "=" * 50)

    m = M_INITIAL  # Start with the initial value of 'm'
    while m <= M_LIMIT:
        # Conduct tests for external libraries
        print(f"{th}Conducting Tests for External Libraries")
        result = conduct_external_test()
        for key, stats in result.items():
            # Generate database entry
            stats = db.generate_entry(stats, key, m, N, ALPHA)
            print(f"{th}Entering values into database for {key}")
            db.enter_values(stats, conn)
            print(f"{th}Values entered successfully")
        m *= M_MULTIPLIER  # Increment 'm' by the multiplier


# Main function to initialize the database and run tests
def tester(index: int = 0, generate_binary: bool = False) -> None:
    # Remove existing database if it exists
    if os.path.exists(f"{RESULTS_DIR + DB_DIR}/test_{index}.db"):
        os.remove(f"{RESULTS_DIR + DB_DIR}/test_{index}.db")

    # Connect to a new SQLite database
    conn = sq.connect(f"{RESULTS_DIR + DB_DIR}/test_{index}.db")
    print(f"[THREAD {index:03}]\tOpened database successfully")

    # Setup database tables and start tests
    db.setup_table(conn)
    start_tests(algo_list, index, conn, generate_binary)

    conn.close()


def main() -> None:
    # Get the number of threads from the user
    threads = int(input("Number of Threads: "))
    generate_binary = input("Generate Binary Files? (y/n): ").lower() == "y"
    t = []

    # Create and start threads for parallel testing
    for i in range(threads):
        thread = threading.Thread(
            target=tester,
            args=(
                i,
                generate_binary,
            ),
        )
        thread.start()
        t.append(thread)

    # Wait for all threads to complete
    for thread in t:
        thread.join()

    algs = list(algo_list.keys()) + ["C", "C++", "Rust", "JS", "Java", "PHP"]

    cmp.main(threads, algs, RESULTS_DIR + DB_DIR)

    selected = vis.get_selection()

    # Visualize results for each thread's data
    for i in range(threads):
        vis.main(algs, f"{RESULTS_DIR + DB_DIR}/test_{i}.db", selected)


# Entry point for the program
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting tests...")
