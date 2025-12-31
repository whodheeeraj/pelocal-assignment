import sqlite3
import os

DATABASE = 'todo.db'

def get_db_connection():
    """Establishes a connection to the database."""
    conn = sqlite3.connect(DATABASE)
    # Allows accessing columns by name (row['title'])
    conn.row_factory = sqlite3.Row 
    return conn

def init_db():
    """Initializes the database with the tasks table."""
    conn = get_db_connection()
    try:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    due_date TEXT,
                    status TEXT DEFAULT 'Pending'
                );
            ''')
        print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error initializing database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    init_db()