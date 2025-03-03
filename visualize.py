import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sq

# Define m values and their logarithmic equivalents for plotting
m_values = np.array([10**i for i in range(2, 12)])
log_m_values = np.log10(m_values)


# Set SQLite database row factory to return rows as dictionaries
def dict_factory(cursor: sq.Cursor, row: tuple) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# Fetch test data for a given algorithm and database index
def fetch_data(alg: str, path: str, select: list[str] = ["*"]) -> list:
    conn = sq.connect(path)
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {", ".join(select)} FROM RandomnessTests WHERE ALGO = ? ORDER BY M ASC",
        (alg,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


# Plot statistical test results (K-S and Chi-Square) for algorithms
def stat_plot(algo_list: list[str], path: str) -> None:
    ks_stats = {}
    chi_stats = {}

    # Collect test statistics for each algorithm
    for key in algo_list:
        ks_stats[key] = []
        chi_stats[key] = []
        rows = fetch_data(key, path)
        for row in rows:
            ks_stats[key].append(row["D_STAT"])
            chi_stats[key].append(row["CHI_2_STAT"])
        ks_stats[key] = np.array(ks_stats[key])
        chi_stats[key] = np.array(chi_stats[key])

    # Create subplots for the two test statistics
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    for algo in algo_list:
        ax1.plot(log_m_values, ks_stats[algo], label=f"{algo}")
        ax2.plot(log_m_values, chi_stats[algo], label=f"{algo}")

    # Set titles, labels, and legends
    ax1.set_title("Kolmogorov-Smirnov Test Statistics")
    ax1.set_xlabel("Value of m")
    ax1.set_ylabel("K-S Statistic")
    ax1.legend()

    ax2.set_title("Chi-Square Test Statistics")
    ax2.set_xlabel("Value of m")
    ax2.set_ylabel("Chi-Square Statistic")
    ax2.legend()

    plt.tight_layout()
    plt.show()


# Plot p-values for the statistical tests
def p_plot(algo_list: list[str], path: str) -> None:
    ks_p_value = {}
    chi_p_value = {}

    # Collect p-values for each algorithm
    for key in algo_list:
        ks_p_value[key] = []
        chi_p_value[key] = []
        rows = fetch_data(key, path)
        for row in rows:
            ks_p_value[key].append(row["KS_P_VALUE"])
            chi_p_value[key].append(row["CHI_P_VALUE"])
        ks_p_value[key] = np.array(ks_p_value[key])
        chi_p_value[key] = np.array(chi_p_value[key])

    # Create subplots for p-values
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    for algo in algo_list:
        ax1.scatter(log_m_values, ks_p_value[algo], label=f"{algo} - K-S")
        ax2.scatter(log_m_values, chi_p_value[algo], label=f"{algo} - Chi^2")

    ##Plot a line through threshhold of 0.05
    ax1.plot(
        log_m_values,
        np.array([0.05] * 10),
        label="Alpha (0.05)",
        linestyle="dashed",
        color="red",
    )
    ax2.plot(
        log_m_values,
        np.array([0.05] * 10),
        label="Alpha (0.05)",
        linestyle="dashed",
        color="red",
    )

    # Set titles, labels, and legends
    ax1.set_title("Kolmogorov-Smirnov Test Statistics")
    ax1.set_xlabel("Value of m")
    ax1.set_ylabel("P_Value")
    ax1.legend()

    ax2.set_title("Chi-Square Test Statistics")
    ax2.set_xlabel("Value of m")
    ax2.set_ylabel("P_Value")
    ax2.legend()

    plt.tight_layout()
    plt.show()


def ex_time_plot(algo_list: list[str], path: str) -> None:
    for key in algo_list:
        rows = fetch_data(key, path)
        data = []
        for row in rows:
            data.append(row["TIME"])
        data = np.array(data)
        plt.plot(log_m_values, data, label=f"{key}")
    plt.xlabel("Value of m")
    plt.ylabel("Time (s)")
    plt.title("Execution Time for Different Algorithms and m Values")
    plt.legend()
    plt.show()


# Visualize test rejection data using a heatmap
def rejection_heatmap(algo_list: list[str], path: str) -> None:
    data = {}

    # Collect rejection results for each algorithm
    for key in algo_list:
        data[f"{key}_ks"] = []
        data[f"{key}_chi"] = []
        rows = fetch_data(key, path)
        for row in rows:
            data[f"{key}_ks"].append(row["KS_REJECTED"])
            data[f"{key}_chi"].append(row["CHI_REJECTED"])

    # Create a DataFrame for heatmap
    df = pd.DataFrame(data, index=[f"M={i}" for i in m_values])

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df,
        annot=True,
        cmap="coolwarm",
        cbar_kws={"label": "Rejection (1 = Rejected, 0 = Not Rejected)"},
    )
    plt.title("Test Rejections for Different Algorithms and m Values")
    plt.ylabel("Test m values")
    plt.xticks(rotation=45)
    plt.show()


# Visualize random number distributions using boxplots
def random_numbers(algo_list: list[str], path: str) -> None:
    _, ax = plt.subplots(1, len(algo_list), figsize=(12, 6))

    for i, key in enumerate(algo_list):
        rows = fetch_data(key, path)
        data = []  # Collect random numbers for boxplot
        labels = []  # Labels for the boxplot
        for row in rows:
            row["RAND_NUMS"] = np.array(json.loads(row["RAND_NUMS"]))
            data.append(row["RAND_NUMS"])
            labels.append(f"m = {row['M']}")

        # Plot a boxplot
        sns.boxplot(data=data, ax=ax[i])
        ax[i].set_title(f"{key}", fontsize=14)
        ax[i].set_xlabel("m Values", fontsize=12)
        ax[i].set_ylabel("Random Value Distribution", fontsize=12)
        ax[i].grid(alpha=0.3)

        # Set ticks and labels
        ax[i].set_xticks(range(len(labels)))
        ax[i].set_xticklabels(labels, rotation=45, ha="right", fontsize=10)

    plt.tight_layout()
    plt.show()


def get_selection() -> set:
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

    return selected


# Main function to invoke specific visualizations
def main(algo_list: list[str], path: str, selected: set[int] = {1, 2, 3, 4, 5}) -> None:
    if 1 in selected:
        stat_plot(algo_list, path)
    if 2 in selected:
        p_plot(algo_list, path)
    if 3 in selected:
        rejection_heatmap(algo_list, path)
    if 4 in selected:
        random_numbers(algo_list, path)
    if 5 in selected:
        ex_time_plot(algo_list, path)


# Entry point for the program
if __name__ == "__main__":
    from test import algo_list, RESULTS_DIR, DB_DIR

    algs = list(algo_list.keys()) + [
        "C",
        "C++",
        "Rust",
        "JS",
        "Java",
        "PHP",
    ]

    threads = int(input("Thread: "))
    try:
        selected = get_selection()
        for i in range(threads):
            main(algs, f"{RESULTS_DIR + DB_DIR}/test_{i}.db", selected)
    except KeyboardInterrupt:
        print("\n\nExiting tests...")

