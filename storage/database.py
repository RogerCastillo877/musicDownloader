import sqlite3
from pathlib import Path


DB_FILE = Path(
    "music_downloader.db"
)


def get_connection():

    conn = sqlite3.connect(
        DB_FILE
    )

    conn.row_factory = (
        sqlite3.Row
    )

    return conn


def initialize():

    conn = get_connection()

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS downloads
        (
            id INTEGER PRIMARY KEY,

            artist TEXT NOT NULL,

            title TEXT NOT NULL,

            downloaded_title TEXT,

            filename TEXT,

            extension TEXT,

            codec TEXT,

            bitrate REAL,

            duration_seconds REAL,

            status TEXT,

            error TEXT,

            downloaded_at TEXT
        )
        """
    )

    conn.commit()

    conn.close()