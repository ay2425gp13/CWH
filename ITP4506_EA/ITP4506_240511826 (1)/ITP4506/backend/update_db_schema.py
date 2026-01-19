"""
Script to update the database schema by adding name and role columns to users table.
Run this script once to update the existing database.
"""
import sqlite3
import os

# Get the database path
db_path = os.path.join(os.path.dirname(__file__), 'marketplace.db')

if not os.path.exists(db_path):
    print(f"Database file not found at {db_path}")
    print("The database will be created automatically when you run the app.")
    exit(0)

print(f"Connecting to database: {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if columns already exist
    cursor.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cursor.fetchall()]
    
    # Add name column if it doesn't exist
    if 'name' not in columns:
        print("Adding 'name' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN name VARCHAR(100)")
        print("✓ Added 'name' column")
    else:
        print("✓ 'name' column already exists")
    
    # Add role column if it doesn't exist
    if 'role' not in columns:
        print("Adding 'role' column to users table...")
        cursor.execute("ALTER TABLE users ADD COLUMN role VARCHAR(20) DEFAULT 'user'")
        print("✓ Added 'role' column")
    else:
        print("✓ 'role' column already exists")
    
    # Update existing users to have role='user' if role is NULL
    cursor.execute("UPDATE users SET role = 'user' WHERE role IS NULL")
    affected = cursor.rowcount
    if affected > 0:
        print(f"✓ Updated {affected} existing user(s) with default role='user'")
    
    conn.commit()
    print("\n✓ Database schema updated successfully!")
    
except sqlite3.Error as e:
    print(f"✗ Error updating database: {e}")
    conn.rollback()
finally:
    if conn:
        conn.close()
        print("Database connection closed.")




