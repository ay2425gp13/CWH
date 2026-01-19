"""Quick script to add name and role columns to users table"""
import sqlite3
import os

db_path = os.path.join('instance', 'marketplace.db')
if not os.path.exists(db_path):
    print(f"Database not found at {db_path}")
    exit(1)

print(f"Connecting to {db_path}...")
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]
print(f"Current columns: {columns}")

# Add name column
if 'name' not in columns:
    print("Adding 'name' column...")
    cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(100)")
    print("[OK] Added 'name' column")
else:
    print("[OK] 'name' column already exists")

# Add role column
if 'role' not in columns:
    print("Adding 'role' column...")
    cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
    cursor.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    print("[OK] Added 'role' column")
else:
    print("[OK] 'role' column already exists")

conn.commit()

# Verify
cursor.execute("PRAGMA table_info(users)")
columns = [row[1] for row in cursor.fetchall()]
print(f"\nUpdated columns: {columns}")

conn.close()
print("\n[OK] Database updated successfully!")

