import sqlite3
import csv
import os

DB_FILE = 'clinical_trial.db'
CSV_FILE = 'cell-count.csv'

POPULATIONS = ['b_cell', 'cd8_t_cell', 'cd4_t_cell', 'nk_cell', 'monocyte']

SCHEMA = """

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS projects (
    project_id  TEXT PRIMARY KEY
)

CREATE TABLE IF NOT EXISTS subjects (
    subject_id  TEXT PRIMARY KEY,
    project_id  TEXT NOT NULL REFERENCES projects(project_id),
    condition   TEXT,
    age         INTEGER,
    sex         TEXT,
);

CREATE TABLE IF NOT EXISTS samples (
    sample_id   TEXT PRIMARY KEY,
    subject_id  TEXT NOT NULL REFERENCES subjects(subject_id),
    sample_type TEXT,
    treatment   TEXT,
    response    TEXT,
    time_from_treatment_start INTEGER
)

CREATE TABLE IF NOT EXISTS populations (
    population_id   TEXT PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL
)

CREATE TABLE IF NOT EXISTS cell_counts (
    count_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id   TEXT NOT NULL REFERENCES samples(sample_id),
    population_id   TEXT NOT NULL REFERENCES populations(population_id),
    count       INTEGER NOT NULL,
    UNIQUE (sample_id, population_id)
)

"""