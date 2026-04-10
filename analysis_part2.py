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


def print_table():


def save_csv():


def main()