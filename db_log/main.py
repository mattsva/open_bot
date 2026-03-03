# db_log/main.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License
from db_log.init import init, get_connection

# initialize database once
if not init():
    raise RuntimeError("Failed to initialize database.")

def db_add_message(author, content):

    conn = get_connection()
    cursor = conn.cursor()

    # convert author to string
    if not isinstance(author, str):
        author = str(author)  # or use author.name for just the username

    cursor.execute(
        "INSERT INTO messages (author, content) VALUES (?, ?)",
        (author, content)
    )
    conn.commit()
    cursor.close()
    conn.close()

def db_show_messages():
    ret = ""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author, content FROM messages") # get messages from DB
    for author, content in cursor.fetchall():
        ret += (f"{author}: {content}")
    cursor.close()
    conn.close()
    return ret