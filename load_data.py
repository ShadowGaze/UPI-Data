import csv
import os
import sqlite3
from database import init_db, DATABASE

BOOL_COLS = {
    "is_weekend", "is_night_transaction", "new_device_flag",
    "ip_location_mismatch", "is_fraud", "recurring_payment_flag",
    "is_high_risk_user", "is_registered"
}


def cast_value(col, val):
    if val is None or str(val).strip() == "":
        return None
    v = str(val).strip()
    if col in BOOL_COLS:
        return 1 if v.lower() in {"true", "1", "yes"} else 0
    try:
        return float(v) if "." in v else int(v)
    except ValueError:
        return v


def load_csv(conn, table, filepath, limit=7000):
    if not os.path.exists(filepath):
        print(f"  [SKIP] {filepath} not found")
        return 0
    loaded = 0
    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= limit:
                break
            cols = list(row.keys())
            vals = [cast_value(col, row[col]) for col in cols]
            placeholders = ",".join(["?"] * len(cols))
            try:
                conn.execute(
                    f"INSERT OR IGNORE INTO {table} ({','.join(cols)}) VALUES ({placeholders})",
                    vals
                )
                loaded += 1
            except sqlite3.Error as e:
                print(f"  Row {i} skipped: {e}")
    conn.commit()
    return loaded


def already_loaded(conn):
    try:
        return conn.execute("SELECT COUNT(*) FROM transactions").fetchone()[0] > 100
    except Exception:
        return False


def load_all():
    print("Initialising database...")
    conn = init_db()
    if already_loaded(conn):
        print("Data already loaded, skipping.")
        conn.close()
        return
    data_dir = os.environ.get("DATA_DIR", "data")
    for table, filename, limit in [
        ("users",        "users.csv",        10000),
        ("merchants",    "merchants.csv",    10000),
        ("transactions", "transactions.csv", 7000),
    ]:
        print(f"Loading {table}...")
        n = load_csv(conn, table, os.path.join(data_dir, filename), limit)
        print(f"  {n} rows loaded")
    conn.close()
    print("Done.")


if __name__ == "__main__":
    load_all()
