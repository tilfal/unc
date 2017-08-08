import sqlite3
from myconst import DBPATH

db_path = DBPATH
conn = sqlite3.connect(db_path)
cursor = conn.execute('select f0, f1 from fund_info')
print(len(cursor.fetchall()))
cursor = conn.execute('select max(f1) from fund_info')
print(cursor.fetchone()[0])
conn.close()