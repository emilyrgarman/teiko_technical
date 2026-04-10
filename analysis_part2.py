import sqlite3
import argparse
import csv
import sys
import os

DB_FILE = "clinical_trial.db"

QUERY = """
SELECT
    sm.sample_id                                                AS sample,
    SUM(cc.count) OVER (PARTITION BY sm.sample_id)             AS total_count,
    p.name                                                      AS population,
    cc.count,
    ROUND(
        cc.count * 100.0 / SUM(cc.count) OVER (PARTITION BY sm.sample_id),
        2
    )                                                           AS percentage
FROM samples sm
JOIN cell_counts cc ON cc.sample_id = sm.sample_id
JOIN populations p  ON p.population_id = cc.population_id
{where_clause}
ORDER BY sm.sample_id, p.name
"""

def get_frequencies(sample_filter=None):
    if not os.path.exists(DB_FILE):
        sys.exit(
            f"ERROR: {DB_FILE} not found.\n"
            "Run python load_data.py first to create the database."
        )
 
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
 
    where = "WHERE sm.sample_id = ?" if sample_filter else ""
    params = (sample_filter,) if sample_filter else ()
 
    rows = conn.execute(QUERY.format(where_clause=where), params).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def print_table(rows):
    if not rows:
        print("No rows returned")
        return
    
    headers = ["sample", "total_count", "population", "count", "percentage"]
    col_widths = {
        "sample": max(len("sample"), max(len(r["sample"]) for r in rows)),
        "total_count": max(len("total_count"), max(len(str(r["total_count"])) for r in rows)),
        "population": max(len("population"), max(len(str(r["population"])) for r in rows)),
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


def save_csv(rows, path="cell_frequencies.csv"):
    if not rows:
        return
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=["sample", "total_count", "population", "count", "percentage"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} rows to {path}")


def main():
    parser = argparse.ArgumentParser(description="Part 2: cell population frequencies")
    parser.add_argument("--csv", action="store_true", help="Save results to cell_frequencies.csv")
    parser.add_argument("--sample", default=None, help="Filter by sample ID")
    args = parser.parse_args()

    rows = get_frequencies(sample_filter=args.sample)
    print_table(rows)

    if args.csv:
        save_csv(rows)


if __name__ == "__main__":
    main()