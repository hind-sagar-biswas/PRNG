import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import sqlite3 as sq
from visualize import fetch_data

def get_rejections(algo: dict, path: str) -> tuple:
    """Fetch rejection counts for KS and Chi-squared tests."""
    ks_reject, chi_reject, total, exec_time = 0, 0, 0, 0
    rows = fetch_data(algo, path, ["CHI_REJECTED", "KS_REJECTED", "TIME"])
    
    for row in rows:
        ks_reject += row["KS_REJECTED"]
        chi_reject += row["CHI_REJECTED"]
        exec_time += row["TIME"]
        total += 1
    
    return ks_reject, chi_reject, exec_time, total

def main(threads: int, algo_list: dict, base: str) -> None:
    """Calculate rejection rates and visualize results."""
    data = {name: {"chi": 0, "ks": 0, "total": 0, "time": 0} for name in algo_list}
    
    for i in range(threads):
        path = f"{base}/test_{i}.db"
        for name in algo_list:
            try:
                ks, chi, exec_time, total = get_rejections(name, path)
                data[name]['chi'] += chi
                data[name]['ks'] += ks
                data[name]['time'] += exec_time
                data[name]['total'] += total
            except Exception:
                pass
    
    print("Rejection Rates:")
    algo_names, chi_rates, ks_rates = [], [], []
    for name, values in data.items():
        chi_rate = values['chi'] / values['total'] * 100 if values['total'] else 0
        ks_rate = values['ks'] / values['total'] * 100 if values['total'] else 0
        exec_time = values['time'] / values['total'] if values['total'] else 0
        algo_names.append(name)
        chi_rates.append(chi_rate)
        ks_rates.append(ks_rate)
        print(f"{name}\t:\tChi^2 = {chi_rate:03.2f}%;\tKS = {ks_rate:03.2f}%;\t[{values['chi']:04}:{values['ks']:04}:{values['total']}]\tExec. time: {exec_time}")
    
    df = pd.DataFrame({"Algorithm": algo_names, "Chi-squared Rejection Rate": chi_rates, "KS Rejection Rate": ks_rates})
    df_melted = df.melt(id_vars=["Algorithm"], var_name="Test Type", value_name="Rejection Rate")
    
    plt.figure(figsize=(10, 6))
    sns.barplot(x="Algorithm", y="Rejection Rate", hue="Test Type", data=df_melted)
    plt.title("Rejection Rates by Algorithm")
    plt.ylabel("Rejection Rate (%)")
    plt.xlabel("Algorithm")
    plt.xticks(rotation=45)
    plt.legend(title="Test Type")
    plt.show()


# Entry point for the program
if __name__ == "__main__":
    from test import algo_list, RESULTS_DIR, DB_DIR
    threads = int(input("Thread: "))
    try:
        main(threads, algo_list, RESULTS_DIR + DB_DIR)
    except KeyboardInterrupt:
        print("\n\nExiting tests...")