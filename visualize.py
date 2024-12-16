import json
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sq


def dict_factory(cursor: sq.Cursor, row: tuple) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def fetch_data(alg):
    conn = sq.connect("test.db")
    conn.row_factory = dict_factory
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM RandomnessTests WHERE ALGO = ? ORDER BY M ASC",
        (alg,),
    )
    rows = cursor.fetchall()
    conn.close()
    return rows


def main(algo_list: dict):
    m_values = np.array([10**i for i in range(2, 12)])
    ks_stats = {}
    chi_stats = {}
    for key, _ in algo_list.items():
        ks_stats[key] = []
        chi_stats[key] = []
        rows = fetch_data(key)
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
