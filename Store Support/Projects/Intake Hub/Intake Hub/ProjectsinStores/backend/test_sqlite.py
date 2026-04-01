import sqlite3
import os

# Delete and recreate fresh DB
if os.path.exists('test.db'):
    os.remove('test.db')

conn = sqlite3.connect('test.db')
c = conn.cursor()

# Create table
c.execute("CREATE TABLE test (id INTEGER, value TEXT)")

# Insert data
for i in range(10):
    c.execute("INSERT INTO test VALUES (?, ?)", (i, f"value_{i}"))

print(f"Before commit: {os.path.getsize('test.db')} bytes")

conn.commit()

print(f"After commit: {os.path.getsize('test.db')} bytes")

# Verify
c.execute("SELECT COUNT(*) FROM test")
count = c.fetchone()[0]
print(f"Rows in DB: {count}")

conn.close()

# Verify file is persistent
conn2 = sqlite3.connect('test.db')
c2 = conn2.cursor()
c2.execute("SELECT COUNT(*) FROM test")
count2 = c2.fetchone()[0]
print(f"After reopen: {count2}")
conn2.close()

os.remove('test.db')
