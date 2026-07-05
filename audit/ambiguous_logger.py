from pathlib import Path
from datetime import datetime


class AmbiguousLogger:
    LOG_DIR = Path("logs")

    @classmethod
    def log(cls, song, winner, second):
        cls.LOG_DIR.mkdir(exist_ok=True)
        path = cls.LOG_DIR / "ambiguous.log"
        with open(path, "a", encoding="utf-8") as f:
            f.write(
                f"""
[{datetime.now().isoformat()}]

REQUEST:
{song.artist} - {song.title}

WINNER:
{winner.score:.2f}
{winner.title}

SECOND:
{second.score:.2f}
{second.title}

DIFFERENCE:
{winner.score - second.score:.2f}

STATUS:
AMBIGUOUS

------------------------------------

"""
            )
