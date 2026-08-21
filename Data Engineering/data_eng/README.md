# SQLite Performance Experiment (Small vs Large Dataset)

A small data engineering experiment comparing SQLite import and query
performance on a small dataset versus a large dataset, to see how table
size affects query speed when no indexes are used.

## Datasets

| File | Records | Notes |
|---|---|---|
| `people-small.csv` | 100 | Plain CSV. [Download](https://drive.google.com/uc?id=1phaHg9objxK2MwaZmSUZAKQ8kVqlgng4&export=download) |
| `people-large.zip` | 2,000,000 | Zipped CSV (`people-2000000.csv`), kept out of git to keep repo size down. [Download](https://drive.google.com/uc?id=1fveqbEJIr4o4oMqswF03NA2Qrk1zF7v4&export=download) |

Both datasets share the same schema:

```
Index, User Id, First Name, Last Name, Sex, Email, Phone, Date of birth, Job Title
```

## What the script does

`sqlite_performance.py`:

1. **Imports** both CSVs into a local SQLite database (`people.db`):
   - `people-small.csv` -> `people_small` table (100 rows)
   - `people-large.zip` (read directly from the zip, no need to extract) -> `people_large` table (2,000,000 rows)
2. **Runs the same 5 benchmark queries** against both tables so timings can
   be compared directly:
   - `Q1` row count
   - `Q2` filter: people over age 50
   - `Q3` average age grouped by job title
   - `Q4` top 5 oldest people
   - `Q5` count grouped by sex
3. **Repeats** the `Q3` group-by query 5 times back-to-back on the large
   table to check whether repeated identical queries get any faster.
4. **Joins** two 2-million-row tables (`people_large` and a derived
   `people_large_contact` table) on an unindexed `id` column to measure
   worst-case query cost.

## Running it

```bash
cd data_eng
python sqlite_performance.py
```

This regenerates `people.db` and prints timing for every step (see
`terminal_log.txt` for an example run).

## Results summary

- Import: ~0.003s for 100 rows vs ~6.3s for 2,000,000 rows.
- `COUNT(*)` stays fast regardless of table size.
- Filtering (`Q2`), `GROUP BY` (`Q3`, `Q5`), and `ORDER BY` (`Q4`) all slow
  down significantly on the large table because SQLite has no index and
  must scan every row.
- Re-running the same query does not get meaningfully faster — SQLite
  doesn't cache query results, so it re-scans and re-aggregates every time.
- The unindexed `JOIN` across two 2-million-row tables is the slowest
  operation overall.

**Takeaway:** without indexes, SQLite query cost scales linearly with
table size for filters, aggregates, and joins — only simple `COUNT(*)`
queries stay cheap regardless of size.
