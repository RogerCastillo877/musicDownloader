from download.download_manager import DownloadManager
import typer

from cli.ui import info
from config.settings import load_settings
from core.parser import SongParser
from core.normalizer import Normalizer
from services.duplicate_detector import DuplicateDetector
from providers.youtube_provider import YoutubeProvider
from services.scorer import Scorer
from services.ranking_analyzer import RankingAnalyzer
from download.youtube_downloader import (
    YoutubeDownloader,
)
from core.models import DownloadJob, DownloadResult, DownloadStatus, Song
from storage.download_repository import DownloadRepository
from datetime import datetime
from services.logger_service import LoggerService
from config.settings import load_settings, Settings

song = Song(
    artist="Metallica",
    title="One",
)

app = typer.Typer()


def get_settings() -> Settings:
    return load_settings()


@app.command()
def config():
    settings = load_settings()
    info(settings.model_dump_json(indent=2))


@app.command()
def stats():
    info("Statistics not implemented")


@app.command()
def download(file: str):
    info(f"Download requested: {file}")

@app.command()
def parse(file: str):

    songs = SongParser.parse_file(file)

    for song in songs:
        Normalizer.normalize_song(song)

    songs = DuplicateDetector.remove_exact_duplicates(
        songs
    )

    songs = DuplicateDetector.remove_fuzzy_duplicates(
        songs
    )

    info(f"Songs: {len(songs)}")

    for song in songs:
        info(
            f"\nSearching: "
            f"{song.artist} - {song.title}"
            f"audio"
        )

@app.command()
def search(file: str):

    provider = YoutubeProvider()

    songs = SongParser.parse_file(file)

    for song in songs:

        info(
            f"\nSearching: "
            f"{song.artist} - {song.title}"
            f' audio'
        )

        candidates = provider.search(
            song.artist,
            song.title,
        )

        scored = []

        for candidate in candidates:

            candidate.score = Scorer.score(
                song,
                candidate,
            )

            scored.append(candidate)

        scored.sort(
            key=lambda x: x.score,
            reverse=True,
        )

        logger = LoggerService()

        if len(scored) > 1:

            winner = scored[0]
            second = scored[1]

            difference = (
                winner.score
                - second.score
            )

            if difference < settings.scoring.ambiguous_delta:
                winner.is_ambiguous = True

                logger.ambiguous(
                    song,
                    winner,
                    second,
                )

                print(
                    "\n⚠️  AMBIGUOUS RESULT"
                )

                print(
                    f"Difference: "
                    f"{difference:.2f}"
                )

        RankingAnalyzer.print_analysis(
            song,
            scored,
        )

@app.command()
def download_test():

    from providers.youtube_provider import (
        YoutubeProvider
    )

    provider = YoutubeProvider()

    downloader = (
        YoutubeDownloader()
    )

    candidates = provider.search(
        song.artist,
        song.title,
    )

    for candidate in candidates:
        candidate.score = (
            Scorer.score(
                song,
                candidate,
            )
        )

    candidates.sort(
        key=lambda c: c.score,
        reverse=True,
    )

    candidate = candidates[0]

    print()

    print(
        "Downloading:"
    )

    print(
        candidate.title
    )
    print(candidate.url)

    result = downloader.download(
        song,
        candidate,
    )

    print()

    print(
        "Downloaded:"
    )

    print(result)

@app.command()
def download_queue(file: str):
    
    songs = SongParser.parse_file(file)

    settings = load_settings()
    provider = YoutubeProvider()
    manager = DownloadManager(workers=settings.workers)
    repository = DownloadRepository()
    jobs = []
    logger = LoggerService()

    for song in songs:
        try:
            print(f"Checking: {song.artist} - {song.title}")

            candidates = provider.search(song.artist, song.title)

            if not candidates:
                print(f"NO RESULTS: {song.artist}")
                continue

            for candidate in candidates:
                candidate.score = Scorer.score(song, candidate)

            candidates.sort(key=lambda c: c.score, reverse=True)

            winner = candidates[0]

            if winner.score < settings.scoring.min_confidence:

                result = DownloadResult(
                    song=song,

                    status=
                        DownloadStatus.NOT_FOUND,

                    downloaded_title=
                        winner.title,

                    error=
                        (
                            "Low confidence "
                            f"({winner.score:.2f})"
                        ),

                    finished_at=
                        datetime.now()
                        .isoformat(),
                )

                repository.save(
                    result
                )

                logger.not_found(
                    song,
                    winner,
                )

                print()

                print(
                    "NO CONFIDENT MATCH"
                )

                print(
                    f"Best candidate: "
                    f"{winner.score:.2f}"
                    f"  "
                    f"{winner.title}"
                )

                print(
                    "SKIPPING DOWNLOAD"
                )

                continue

            if repository.exists(
                song.artist,
                song.title,
            ):

                print(
                    f"SKIP: "
                    f"{song.artist}"
                    f" - "
                    f"{song.title}"
                )

                continue

            jobs.append(
                DownloadJob(
                    song=song,
                    candidate=winner,
                )
            )

            print(f"Job created: {song.artist} - {song.title}")
        except Exception as exc:
            print(f"JOB FAILED: {song.artist} - {song.title}")
            print(exc)

        print()
        print("TOTAL SONGS:", len(songs))
        print("TOTAL JOBS:", len(jobs))
        print()

    manager.process(jobs)

@app.command()
def retry_errors():

    repository = (
        DownloadRepository()
    )

    rows = (
        repository.get_failed()
    )

    songs = []

    for row in rows:

        songs.append(
            Song(
                artist=row["artist"],
                title=row["title"],
            )
        )

    print()

    print(
        f"FOUND "
        f"{len(songs)} "
        f"FAILED SONGS"
    )

    print()

    manager = (
        DownloadManager()
    )

    manager.process(
        songs
    )