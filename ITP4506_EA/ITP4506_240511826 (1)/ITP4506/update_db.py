import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'backend', 'instance', 'marketplace.db')
print(f"Updating database: {db_path}")

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("PRAGMA table_info(users)")
cols = [r[1] for r in c.fetchall()]
print(f"Current columns: {cols}")

if 'name' not in cols:
    print("Adding name column...")
    c.execute("ALTER TABLE users ADD COLUMN name VARCHAR(100)")
    
if 'role' not in cols:
    print("Adding role column...")
    c.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
    c.execute("UPDATE users SET role = 'user' WHERE role IS NULL")

conn.commit()

c.execute("PRAGMA table_info(users)")
cols = [r[1] for r in c.fetchall()]
print(f"Updated columns: {cols}")
print("Done!")

conn.close()

