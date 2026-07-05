from pathlib import Path
from datetime import datetime


class AuditLogger:
    LOG_DIR = Path("logs")

    @classmethod
    def _write(cls, filename: str, message: str):
        cls.LOG_DIR.mkdir(exist_ok=True)
        filepath = cls.LOG_DIR / filename
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(message)
            f.write("\n")

    @classmethod
    def duplicate(cls, original, duplicate, similarity):
        timestamp = datetime.now().isoformat()
        message = f"""
[{timestamp}]
SKIPPED_DUPLICATE

ORIGINAL:
{original.artist} - {original.title}

DUPLICATE:
{duplicate.artist} - {duplicate.title}

SIMILARITY:
{similarity}

--------------------------------
"""
        cls._write("duplicates.log", message)
