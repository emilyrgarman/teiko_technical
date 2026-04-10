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
    return


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