import json
import sqlite3 as sq


def generate_entry(stats: dict, algo: str, m: int, n: int, alpha: float) -> dict:
    return {
        "ALGO": algo,
        "M": m,
        "N": n,
        "ALPHA": alpha,
        "RAND_NUMS": json.dumps(stats["numbers"]),
        "D_STAT": stats["ks"][0],
        "KS_P_VALUE": stats["ks"][1],
        "KS_REJECTED": stats["ks"][2],
        "CHI_2_STAT": stats["chi"][0],
        "CHI_P_VALUE": stats["chi"][1],
        "CHI_REJECTED": stats["chi"][2],
    }


def enter_values(stat: dict, conn: sq.Connection):
    conn.execute(
        "INSERT INTO RandomnessTests (ALGO, M, N, ALPHA, RAND_NUMS, D_STAT, CHI_2_STAT, KS_P_VALUE, KS_REJECTED, CHI_P_VALUE, CHI_REJECTED) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            stat["ALGO"],
            stat["M"],
            stat["N"],
            stat["ALPHA"],
            stat["RAND_NUMS"],
            stat["D_STAT"],
            stat["CHI_2_STAT"],
            stat["KS_P_VALUE"],
            stat["KS_REJECTED"],
            stat["CHI_P_VALUE"],
            stat["CHI_REJECTED"],
        ),
    )
    conn.commit()
    print("Values entered successfully")


def setup_table(conn: sq.Connection):
    conn.execute("""CREATE TABLE RandomnessTests (
        ALGO CHAR(50)       NOT NULL,        -- Algorithm name
        M INT               NOT NULL,        -- Parameter m (integer)
        N INT               NOT NULL,        -- Parameter n (integer)
        ALPHA FLOAT         NOT NULL,        -- Alpha value (significance level)
        RAND_NUMS TEXT      NOT NULL,        -- Generated random numbers (stored as a JSON array)
        D_STAT FLOAT,                        -- K-S Test D statistic (nullable)
        CHI_2_STAT FLOAT,                    -- Chi-Square Test statistic (nullable)
        KS_P_VALUE FLOAT    NOT NULL,        -- p-value of the K-S test
        KS_REJECTED  INT    NOT NULL,        -- Whether the null hypothesis was rejected by the K-S test
        CHI_P_VALUE FLOAT   NOT NULL,        -- p-value of the Chi-Square test
        CHI_REJECTED INT    NOT NULL,        -- Whether the null hypothesis was rejected by the Chi-Square test
        TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP -- Timestamp on row creation
    );""")
    print("Table created successfully")
