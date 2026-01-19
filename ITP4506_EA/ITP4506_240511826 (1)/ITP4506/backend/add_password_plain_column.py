"""
Script to update the database schema by adding password_plain column to users table.
Run this script once to update the existing database.
"""
import sqlite3
import os

# Get the database path - check both possible locations
db_paths = [
    os.path.join(os.path.dirname(__file__), 'instance', 'marketplace.db'),
    os.path.join(os.path.dirname(__file__), 'marketplace.db'),
    os.path.join(os.path.dirname(__file__), 'secondhand_market.db')
]

db_path = None
for path in db_paths:
    if os.path.exists(path):
        db_path = path
        break

if not db_path:
    print("Database file not found. Please run the app first to create the database.")
    exit(0)

print(f"Connecting to database: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if column already exists
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Add password_plain column if it doesn't exist
    if 'password_plain' not in columns:
        print("Adding 'password_plain' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN password_plain VARCHAR(255)")
        conn.commit()
        print("✓ Added 'password_plain' column")
    else:
        print("✓ 'password_plain' column already exists")
    
    conn.commit()
    print("\n✓ Database schema updated successfully!")
    
except sqlite3.Error as e:
    print(f"✗ Error updating database: {e}")
    if conn:
        conn.rollback()
finally:
    if conn:
        conn.close()
        print("Database connection closed.")

