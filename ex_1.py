#!/usr/bin/env python3

# Since python 3.12, sqlite's internal default adapter/converter for
# python's datetime handling is depricated. The new correct way is to
# implement your own on a case by case basis. The following is an
# example of the most common adapter/converter use case.

# Imports for simple datetime sqlite handling
import sqlite3
from datetime import datetime, UTC


# ---- Register adapter and converter ----
def adapt_datetime(dt: datetime) -> str:
    '''
    Adapter for python datetime objects so they can be
    automagically stored in sqlite.
    '''
    if dt.tzinfo is None:
        raise ValueError("Naive datetime not allowed; must be timezone-aware (UTC).")
    return dt.isoformat()

def convert_datetime(b: bytes) -> datetime:
    '''
    Converter for data coming from an sqlite TIMESTAMP column
    so it can be automagically converted into a python datetime object.
    '''
    return datetime.fromisoformat(b.decode())

sqlite3.register_adapter(datetime, adapt_datetime)
sqlite3.register_converter("timestamp", convert_datetime)

# ---- Connect ----
conn = sqlite3.connect(
    "example.sqlite",
    detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
)
cursor = conn.cursor()

# ---- Create table ----
cursor.execute("""
CREATE TABLE IF NOT EXISTS ex_1_table (
    id INT PRIMARY KEY,
    time TIMESTAMP
)
""")

# ---- Find existing max id in case the script has previously been run ----
max_id: int = 0
cursor.execute("SELECT MAX(id) from ex_1_table")
result = cursor.fetchone()[0]
if result is not None:
    max_id = result
    print("max_id is: ", max_id)

# ---- Insert (uses adapter) ----
now = datetime.now(UTC)
cursor.execute("INSERT INTO ex_1_table (id, time) VALUES (?, ?)", (max_id + 1, now))
conn.commit()

# ---- Select (uses custom converter) ----
cursor.execute('SELECT id, time FROM ex_1_table')
print("example 1 output:")
for row in cursor.fetchall():
    print(row)
    print(type(row[1]))  # <class 'datetime.datetime'>
print("---------")
