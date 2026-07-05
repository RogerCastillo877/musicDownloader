from pathlib import Path
from datetime import datetime


class LoggerService:

    LOG_DIR = Path("logs")

    def __init__(self):

        self.LOG_DIR.mkdir(
            exist_ok=True
        )

    def _write(
        self,
        filename,
        text,
    ):

        path = (
            self.LOG_DIR /
            filename
        )

        with open(
            path,
            "a",
            encoding="utf-8",
        ) as f:

            f.write(text)
            f.write("\n")

    def success(
        self,
        result,
    ):

        self._write(
            "downloads.log",
            (
                f"{result.finished_at} | "
                f"{result.song.artist} | "
                f"{result.song.title} | "
                f"{result.downloaded_title} | "
                f"{result.codec} | "
                f"{result.bitrate} | "
                f"{result.extension} | "
                f"{result.filename} | "
                f"{result.duration_seconds}"
            ),
        )

    def error(
        self,
        result,
    ):

        self._write(
            "errors.log",
            (
                f"{result.finished_at} | "
                f"{result.song.artist} | "
                f"{result.song.title} | "
                f"{result.error}"
            ),
        )

    def ambiguous(
        self,
        song,
        winner,
        second,
    ):

        self._write(
            "ambiguous.log",
            (
                f"{datetime.now().isoformat()} | "
                f"{song.artist} - "
                f"{song.title} | "
                f"{winner.score:.2f} | "
                f"{second.score:.2f}"
            ),
        )

    def duplicate(
        self,
        original,
        duplicate,
        similarity,
    ):

        self._write(
            "duplicates.log",
            (
                f"{datetime.now().isoformat()} | "
                f"SKIPPED_DUPLICATE | "
                f"{original.artist} - {original.title} | "
                f"{duplicate.artist} - {duplicate.title} | "
                f"{similarity}"
            ),
        )

    def summary(
        self,
        requested,
        success,
        failed,
    ):

        self._write(
            "summary.log",
            (
                f"{datetime.now().isoformat()} | "
                f"REQUESTED={requested} | "
                f"SUCCESS={success} | "
                f"FAILED={failed}"
            ),
        )
    
    def not_found(
        self,
        song,
        candidate,
    ):

        with open(
            "logs/not_found.log",
            "a",
            encoding="utf-8",
        ) as f:

            f.write(
                (
                    f"{datetime.now().isoformat()} | "
                    f"{song.artist} | "
                    f"{song.title} | "
                    f"{candidate.score:.2f} | "
                    f"{candidate.title}\n"
                )
            )