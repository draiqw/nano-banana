from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Iterator

# Database file lives at project root
DB_PATH = Path(__file__).resolve().parent.parent / "app.db"


def get_db() -> Iterator[sqlite3.Connection]:
    """Yield a sqlite3 connection per request and ensure it's closed."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_db() -> None:
    """Create tables if they don't exist."""
    # Ensure the parent directory exists (project root should exist already)
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            )
            """
        )
        conn.commit()
    finally:
        conn.close()

