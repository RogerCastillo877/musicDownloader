from yt_dlp import YoutubeDL

from core.models import SearchCandidate
from core.flags import extract_flags


class YoutubeProvider:

    def search(
        self,
        artist: str,
        title: str,
        limit: int = 10,
    ) -> list[SearchCandidate]:

        query = (
            f'"{artist}" '
            f'"{title}" '
            f'audio'
        )

        opts = {
            "quiet": True,
            "extract_flat": True,
        }

        results = []

        with YoutubeDL(opts) as ydl:

            data = ydl.extract_info(
                f"ytsearch{limit}:{query}",
                download=False,
            )

            from core.flags import extract_flags

            ...

            for entry in data["entries"]:

                candidate = SearchCandidate(
                    provider="youtube",

                    title=entry.get(
                        "title",
                        "",
                    ),

                    artist="",

                    url=f"https://youtube.com/watch?v={entry['id']}",

                    provider_id=entry["id"],

                    duration=entry.get(
                        "duration",
                        0,
                    ),
                )

                candidate.flags = extract_flags(
                    candidate.title
                )

                results.append(candidate)
        
        return results