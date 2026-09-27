import sqlite3

DB_NAME = "database.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS preferences (
            key TEXT PRIMARY KEY,
            value TEXT
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            agent_response TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_preference(key, value):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT OR REPLACE INTO preferences (key, value) VALUES (?, ?)",
        (key, value)
    )

    conn.commit()
    conn.close()


def get_preference(key):
    conn = sqlite3.connect(DB_NAME)

    result = conn.execute(
        "SELECT value FROM preferences WHERE key = ?",
        (key,)
    ).fetchone()

    conn.close()

    return result[0] if result else None


def save_interaction(user_message, agent_response):
    conn = sqlite3.connect(DB_NAME)

    conn.execute(
        "INSERT INTO interactions (user_message, agent_response) VALUES (?, ?)",
        (user_message, agent_response)
    )

    conn.commit()
    conn.close()