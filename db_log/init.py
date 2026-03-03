# db_log/init.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
import sqlite3
from pathlib import Path

# database file will be createt
DB_FILE = Path(__file__).parent / "open_bot.db"

def init():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # create messages table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)

        conn.commit()
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print("Database initialization error:", e)
        return False

def get_connection():
    return sqlite3.connect(DB_FILE)