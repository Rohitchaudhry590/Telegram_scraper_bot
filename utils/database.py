# ============================================================
#  utils/database.py  —  SQLite se track karo posted URLs
# ============================================================
import sqlite3
from config.settings import DB_FILE


def init_db():
    """Database aur table banao agar exist nahi karta."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS posted_urls (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            url     TEXT    UNIQUE NOT NULL,
            title   TEXT,
            posted_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def is_already_posted(url: str) -> bool:
    """Check karo kya ye URL pehle post ho chuki hai."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM posted_urls WHERE url = ?", (url,))
    result = c.fetchone()
    conn.close()
    return result is not None


def mark_as_posted(url: str, title: str = ""):
    """URL ko database mein save karo."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO posted_urls (url, title) VALUES (?, ?)", (url, title))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # already exists
    finally:
        conn.close()


def get_total_posted() -> int:
    """Total kitne posts ho chuke hain."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM posted_urls")
    count = c.fetchone()[0]
    conn.close()
    return count