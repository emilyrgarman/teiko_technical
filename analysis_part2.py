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

def get_frequencies():


def print_table():


def save_csv():


def main()