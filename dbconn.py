import json
import sqlite3 as sq


def generate_entry(stats: dict, algo: str, m: int, n: int, alpha: float):
    return [
        {
            "ALGO": algo,
            "TEST": "Kolmogorov-Smirnov",
            "M": m,
            "N": n,
            "ALPHA": alpha,
            "RAND_NUMS": json.dumps(stats["numbers"]),
            "D_STAT": stats["ks"][0],
            "P_VALUE": stats["ks"][1],
            "REJECTED": stats["ks"][2],
        },
        {
            "ALGO": algo,
            "TEST": "Chi-Square",
            "M": m,
            "N": n,
            "ALPHA": alpha,
            "RAND_NUMS": json.dumps(stats["numbers"]),
            "CHI_2_STAT": stats["chi"][0],
            "P_VALUE": stats["chi"][1],
            "REJECTED": stats["chi"][2],
        },
    ]


def enter_values(stats: list, conn: sq.Connection):
    for stat in stats:
        conn.execute(
            "INSERT INTO RandomnessTests (ALGO, TEST, M, N, ALPHA, RAND_NUMS, D_STAT, CHI_2_STAT, P_VALUE, REJECTED) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                stat["ALGO"],
                stat["TEST"],
                stat["M"],
                stat["N"],
                stat["ALPHA"],
                stat["RAND_NUMS"],
                stat["D_STAT"] if "D_STAT" in stat else None,
                stat["CHI_2_STAT"] if "CHI_2_STAT" in stat else None,
                stat["P_VALUE"],
                stat["REJECTED"],
            ),
        )
    conn.commit()
    print("Values entered successfully")


def setup_table(conn: sq.Connection):
    conn.execute("""CREATE TABLE RandomnessTests (
        ALGO CHAR(50)       NOT NULL,        -- Algorithm name
        TEST CHAR(50)       NOT NULL,        -- Test name (e.g., K-S or Chi-Square)
        M INT               NOT NULL,        -- Parameter m (integer)
        N INT               NOT NULL,        -- Parameter n (integer)
        ALPHA FLOAT         NOT NULL,        -- Alpha value (significance level)
        RAND_NUMS TEXT      NOT NULL,        -- Generated random numbers (stored as a JSON array)
        D_STAT FLOAT,                        -- K-S Test D statistic (nullable)
        CHI_2_STAT FLOAT,                    -- Chi-Square Test statistic (nullable)
        P_VALUE FLOAT       NOT NULL,        -- p-value of the test
        REJECTED  INT       NOT NULL,        -- Whether the null hypothesis was rejected
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp on row creation
    );""")
    print("Table created successfully")
