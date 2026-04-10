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
);

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
);

CREATE TABLE IF NOT EXISTS populations (
    population_id   TEXT PRIMARY KEY,
    name            TEXT UNIQUE NOT NULL
);

CREATE TABLE IF NOT EXISTS cell_counts (
    count_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id   TEXT NOT NULL REFERENCES samples(sample_id),
    population_id   TEXT NOT NULL REFERENCES populations(population_id),
    count       INTEGER NOT NULL,
    UNIQUE (sample_id, population_id)
);

"""


def init_db(conn):
    conn.execute(SCHEMA)
    conn.executemany(
        "INSERT OR IGNORE INTO populations (name) VALUES (?)",
        [(p,) for p in POPULATIONS],
    )
    conn.commit()


def load_csv(conn, csv_path):
    with open(csv_path, newline="") as fh:
        reader = csv.DictReader(fh)

        projects, subjects, samples, counts = set(), {}, {}, []

        for row in reader:
            proj = row["project"]
            subj = row["subject"]
            sample = row["sample"]

            projects.add((proj,))

            subjects[subj] = (
                subj,
                proj,
                row["condition"],
                int(row["age"]) if row["age"] else None,
                row["sex"],
            )

            samples[sample] = (
                sample,
                subj,
                row["sample_type"],
                row["treatment"],
                row["response"] if row["response"] else None,
                int(row["time_from_treatment_start"]) if row["time_from_treatment_start"] else None,
            )

            for p in POPULATIONS:
                counts.append((sample, p, int(row[p])))

    conn.executemany(
        "INSERT OR IGNORE INTO projects (project_id) VALUES (?)",
        projects,
    )
    conn.executemany(
        "INSERT OR IGNORE INTO subjects "
        "(subject_id, project_id, condition, age, sex) VALUES (?, ?, ?, ?, ?)",
        subjects.values(),
    )
    conn.executemany(
        "INSERT OR IGNORE INTO samples "
        "(sample_id, subject_id, sample_type, treatment, response, time_from_treatment_start) VALUES (?, ?, ?, ?, ?, ?)",
        subjects.values(),
    )
    conn.executemany(
        """
        INSERT OR IGNORE INTO cell_counts (sample_id, population_id, count)
        SELECT ?, population_id, ?
        FROM populations WHERE name = ?
        """,
        [(s,c,p) for s, p, c in counts],
    )
    conn.commit()
    return len(samples), len(counts)