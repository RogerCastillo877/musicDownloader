from pathlib import Path

from core.models import SongRequest


class SongParser:

    @staticmethod
    def parse_file(path: str) -> list[SongRequest]:
        songs: list[SongRequest] = []

        file_path = Path(path)

        if not file_path.exists():
            raise FileNotFoundError(path)

        with open(file_path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                if " - " not in line:
                    continue

                artist, title = line.split(" - ", 1)

                songs.append(
                    SongRequest(
                        artist=artist.strip(),
                        title=title.strip(),
                    )
                )

        return songs
  