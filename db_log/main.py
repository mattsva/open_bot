# db_log/main.py
# Copyright (c) 2026 mattisva
# Licensed under the MIT License - see the LICENSE file in the project root for details.
from db_log.init import init, get_connection

# init db once
if not init():
    raise RuntimeError("Failed to initialize database.")


def db_add_message(author, content):
    conn = get_connection()
    cursor = conn.cursor()

    # convert author to str
    if not isinstance(author, str):
        author = str(author)

    cursor.execute(
        "INSERT INTO messages (author, content) VALUES (?, ?)",
        (author, content)
    )
    conn.commit()
    cursor.close()
    conn.close()


def db_show_messages():
    messages = []
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT author, content FROM messages")  # get messages from DB
    for author, content in cursor.fetchall():
        messages.append({"author": author, "content": content})
    cursor.close()
    conn.close()
    return messages