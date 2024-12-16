import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sq

m_values = np.array([10**i for i in range(2, 12)])


def dict_factory(cursor: sq.Cursor, row: tuple) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def fetch_data(alg, index: int = 0):
    conn = sq.connect(f"test_{index}.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM RandomnessTests WHERE ALGO = ? ORDER BY M ASC",
        (alg,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def stat_plot(algo_list: dict, index: int = 0):
    ks_stats = {}
    chi_stats = {}
    for key, _ in algo_list.items():
        ks_stats[key] = []
        chi_stats[key] = []
        rows = fetch_data(key, index)
        for row in rows:
            ks_stats[key].append(row["D_STAT"])
            chi_stats[key].append(row["CHI_2_STAT"])
        ks_stats[key] = np.array(ks_stats[key])
        chi_stats[key] = np.array(chi_stats[key])

    # Creating subplots
    _, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    for algo in algo_list:
        ax1.scatter(m_values, ks_stats[algo], label=f"{algo}")
        ax1.set_title("Kolmogorov-Smirnov Test Statistics")
        ax1.set_xlabel("Value of m")
        ax1.set_ylabel("K-S Statistic")
        ax1.legend()

    for algo in algo_list:
        ax2.scatter(m_values, chi_stats[algo], label=f"{algo}")
        ax2.set_title("Chi-Square Test Statistics")
        ax2.set_xlabel("Value of m")
        ax2.set_ylabel("Chi-Square Statistic")
        ax2.legend()

    plt.tight_layout()
    plt.show()


def p_plot(algo_list: dict, index: int = 0):
    ks_stats = {}
    chi_stats = {}
    for key, _ in algo_list.items():
        ks_stats[key] = []
        chi_stats[key] = []
        rows = fetch_data(key, index)
        for row in rows:
            ks_stats[key].append(row["KS_P_VALUE"])
            chi_stats[key].append(row["CHI_P_VALUE"])
        ks_stats[key] = np.array(ks_stats[key])
        chi_stats[key] = np.array(chi_stats[key])

    plt.figure(figsize=(10, 6))

    for algo in algo_list:
        plt.plot(m_values, ks_stats[algo], label=f"{algo} - K-S")

    for algo in algo_list:
        plt.plot(
            m_values, chi_stats[algo], label=f"{algo} - Chi-Square", linestyle="--"
        )

    plt.title("Test Statistics (K-S and Chi-Square) Across Different m Values")
    plt.xlabel("Value of m")
    plt.ylabel("Test Statistic")
    plt.legend()
    plt.show()


def rejection_heatmap(algo_list: dict, index: int = 0):
    data = {}
    for key, _ in algo_list.items():
        data[f"{key}_ks"] = []
        data[f"{key}_chi"] = []
        rows = fetch_data(key, index)
        for row in rows:
            data[f"{key}_ks"].append(row["KS_REJECTED"])
            data[f"{key}_chi"].append(row["CHI_REJECTED"])
    df = pd.DataFrame(data, index=[f"M={i}" for i in m_values])

    # Heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        df,
        annot=True,
        cmap="coolwarm",
        cbar_kws={"label": "Rejection (1 = Rejected, 0 = Not Rejected)"},
    )
    plt.title("Test Rejections for Different Algorithms and m Values")
    plt.ylabel("Test m values")
    plt.xticks(rotation=45)  # Rotate x labels for clarity
    plt.show()


def main(algo_list: dict, index: int = 0, only_rejections: bool = False):
    if not only_rejections:
        stat_plot(algo_list, index)
        p_plot(algo_list, index)
    rejection_heatmap(algo_list, index)
