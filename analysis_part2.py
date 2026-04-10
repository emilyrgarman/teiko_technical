import sqlite3
import argparse
import csv
import sys
import os

DB_FILE = "clinical_trial.db"

QUERY = """
SELECT
    sm.sample_id AS sample,
    SUM(cc.count) OVER (PARTITION BY sm.sample_id) AS total_count,
    p.name AS population,
    cc.count,
    ROUND(
        cc.count * 100.0 / SUM(cc.count) OVER (PARTITION BY sm.sample_id),
        2
    ) AS percentage
FROM samples AS sm
JOIN counts AS cc ON sm.sample_id = sm.sample_id
JOIN populations AS p ON p.population_id = cc.population_id
{where clause}
ORDER BY
    sm.sample_id,
    p.name
"""

def get_frequencies(sample_filter=None):
    if not os.path.exists(DB_FILE):
        sys.exit(
            f"ERROR: {DB_FILE} not found.\n"
            "Run python load_data.py first to create database."
        )

    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row

    where = "WHERE sm.sample_id = ?" if sample_filter else ""
    params = (sample_filter,) if sample_filter else ()

    rows = conn.execute(QUERY.format(where=where), params).fetchall()
    conn.close()

    return [dict(r) for r in rows]


def print_table(rows):
    if not rows:
        print("No rows returned")
        return
    
    headers = ["sample", "total_count", "population", "count", "percentage"]
    col_widths = {
        "sample": max(len("sample"), max(len(r["sample"]) for r in rows)),
        "total_count": max(len("total_count"), max(len(r["total_count"]) for r in rows)),
        "population": max(len("population"), max(len(r["population"]) for r in rows)),
        "count": max(len("count"), max(len(str(r["count"])) for r in rows)),
        "percentage": max(len("percentage"), max(len(str(r["percentage"])) for r in rows)),
    }

    fmt = "  ".join(f"{{:<{col_widths[h]}}}" for h in headers)
    sep = "  ".join("-" * col_widths[h] for h in headers)

    print(fmt.format(*headers))
    print(sep)
    for r in rows:
        print(fmt.format(
            r["sample"],
            r["total_count"],
            r["population"],
            r["count"],
            r["percentage"],
        ))

    print(f"\nTotal rows: {len(rows)} ({len(rows) // 5} unique samples)")


def save_csv():


def main()