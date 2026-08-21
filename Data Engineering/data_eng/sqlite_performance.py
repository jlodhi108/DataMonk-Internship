import sqlite3
import csv
import zipfile
import io
import time

SMALL_CSV = "people-small.csv"
LARGE_ZIP = "people-large.zip"
LARGE_CSV_NAME = "people-2000000.csv"   # file name inside the zip
DB_FILE = "people.db"


def rows_from_plain_csv(path):
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # skip header
        for row in reader:
            yield row


def rows_from_zip_csv(zip_path, inner_name):
    with zipfile.ZipFile(zip_path) as z:
        with z.open(inner_name) as raw:
            text = io.TextIOWrapper(raw, encoding="utf-8")
            reader = csv.reader(text)
            next(reader)  # skip header
            for row in reader:
                yield row


def import_to_sqlite(row_generator, db_file, table_name):
    start = time.time()

    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    cur.execute(f"DROP TABLE IF EXISTS {table_name}")
    cur.execute(f"""
        CREATE TABLE {table_name} (
            id INTEGER,
            user_id TEXT,
            first_name TEXT,
            last_name TEXT,
            sex TEXT,
            email TEXT,
            phone TEXT,
            dob TEXT,
            job_title TEXT
        )
    """)

    cur.executemany(
        f"INSERT INTO {table_name} VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
        row_generator
    )

    conn.commit()
    elapsed = time.time() - start
    print(f"[IMPORT] -> {table_name}: {elapsed:.4f} sec")
    conn.close()
    return elapsed


def run_query(db_file, query, label):
    conn = sqlite3.connect(db_file)
    cur = conn.cursor()

    start = time.time()
    cur.execute(query)
    results = cur.fetchall()
    elapsed = time.time() - start

    print(f"[{label}] took {elapsed:.4f} sec, {len(results)} rows returned")
    conn.close()
    return elapsed


if __name__ == "__main__":
    print("=== IMPORTING DATA ===")
    import_to_sqlite(rows_from_plain_csv(SMALL_CSV), DB_FILE, "people_small")
    import_to_sqlite(rows_from_zip_csv(LARGE_ZIP, LARGE_CSV_NAME), DB_FILE, "people_large")

    queries = {
        "Q1_count":
            "SELECT COUNT(*) FROM {table}",
        "Q2_age_over_50":
            "SELECT * FROM {table} "
            "WHERE (julianday('now') - julianday(dob)) / 365.25 > 50",
        "Q3_avg_age_by_job_title":
            "SELECT job_title, AVG((julianday('now') - julianday(dob)) / 365.25) AS avg_age "
            "FROM {table} GROUP BY job_title",
        "Q4_top5_oldest":
            "SELECT first_name, last_name, dob, "
            "(julianday('now') - julianday(dob)) / 365.25 AS age "
            "FROM {table} ORDER BY age DESC LIMIT 5",
        "Q5_count_by_sex":
            "SELECT sex, COUNT(*) FROM {table} GROUP BY sex",
    }

    print("\n=== RUNNING QUERIES (people_small) ===")
    for label, q in queries.items():
        run_query(DB_FILE, q.format(table="people_small"), f"{label}_small")

    print("\n=== RUNNING QUERIES (people_large) ===")
    for label, q in queries.items():
        run_query(DB_FILE, q.format(table="people_large"), f"{label}_large")

    print("\n=== BACK-TO-BACK QUERY TEST (large table, 5x) ===")
    total = 0
    for i in range(5):
        total += run_query(
            DB_FILE,
            queries["Q3_avg_age_by_job_title"].format(table="people_large"),
            f"repeat_{i+1}"
        )
    print(f"Total time for 5 repeated queries: {total:.4f} sec")

    print("\n=== CREATING SECOND LARGE TABLE FOR JOIN ===")
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS people_large_contact")
    cur.execute("""
        CREATE TABLE people_large_contact (
            id INTEGER,
            email TEXT,
            phone TEXT
        )
    """)
    cur.execute("""
        INSERT INTO people_large_contact (id, email, phone)
        SELECT id, email, phone FROM people_large
    """)
    conn.commit()
    conn.close()
    print("Created people_large_contact table (2M rows)")

    join_query = """
        SELECT p.first_name, p.last_name, p.job_title, c.email
        FROM people_large p
        JOIN people_large_contact c ON p.id = c.id
        WHERE p.sex = 'Female'
    """
    run_query(DB_FILE, join_query, "JOIN_large_tables")

    print("\n=== OBSERVATIONS ===")
    print("Compare timings above between _small and _large query runs.")
    print("COUNT(*) stays fast on both sizes.")
    print("Age filtering (Q2) and GROUP BY (Q3, Q5) slow down the most on")
    print("the 2M-row table because SQLite has no index and must scan every row.")
    print("ORDER BY (Q4) also requires a full sort before LIMIT applies.")
    print("The JOIN across two 2M-row tables is the slowest operation overall")
    print("since there is no index on 'id' in either table.")