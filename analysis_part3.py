import sqlite3
import os
import sys
import collections
 
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from scipy import stats
 
DB_FILE = "clinical_trial.db"
OUTPUT_PLOT = "cell_population_boxplot.png"
 
POPS = ["b_cell", "cd4_t_cell", "cd8_t_cell", "nk_cell", "monocyte"]
POP_LABELS = {
    "b_cell":     "B cell",
    "cd4_t_cell": "CD4 T cell",
    "cd8_t_cell": "CD8 T cell",
    "nk_cell":    "NK cell",
    "monocyte":   "Monocyte",
}
COLORS = {"yes": "green", "no": "red"}

# pull data
def load_data():
    if not os.path.exists(DB_FILE):
        sys.exit(f"ERROR: {DB_FILE} not found. Run python load_data.py first.")
 
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
 
    rows = conn.execute("""
        SELECT
            sm.sample_id,
            sm.response,
            p.name AS population,
            ROUND(
                cc.count * 100.0 / SUM(cc.count) OVER (PARTITION BY sm.sample_id),
                4
            ) AS percentage
        FROM samples sm
        JOIN subjects sub ON sub.subject_id = sm.subject_id
        JOIN cell_counts cc ON cc.sample_id = sm.sample_id
        JOIN populations p  ON p.population_id = cc.population_id
        WHERE sub.condition   = 'melanoma'
          AND sm.treatment    = 'miraclib'
          AND sm.sample_type  = 'PBMC'
          AND sm.response    IN ('yes', 'no')
        ORDER BY sm.response, p.name
    """).fetchall()
 
    conn.close()
    return [dict(r) for r in rows]


def organize():
    return


def adjust_pvals():
    return


def run_statistics():
    return


def print_results():
    return


def make_boxplot():
    return


def main():
    return