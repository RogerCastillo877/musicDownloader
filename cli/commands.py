from download.download_manager import DownloadManager
import typer

from cli.ui import info
from config.settings import load_settings
from core.parser import SongParser
from core.normalizer import Normalizer
from core.duplicate_detector import DuplicateDetector
from providers.youtube_provider import YoutubeProvider
from core.scorer import Scorer
from core.parser import SongParser
from core.ranking_analyzer import RankingAnalyzer
from download.youtube_downloader import (
    YoutubeDownloader
)
from core.models import DownloadJob, Song

song = Song(
    artist="Metallica",
    title="One",
)

app = typer.Typer()


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

        from core.ambiguous_logger import (
            AmbiguousLogger,
        )

        if len(scored) > 1:

            winner = scored[0]
            second = scored[1]

            difference = (
                winner.score
                - second.score
            )

            if difference < 10:
                winner.is_ambiguous = True

                AmbiguousLogger.log(
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

    provider = YoutubeProvider()
    manager = DownloadManager(workers=4)
    jobs = []

    for song in songs:
        try:
            print(f"Creating job: {song.artist} - {song.title}")

            candidates = provider.search(song.artist, song.title)

            if not candidates:
                print(f"NO RESULTS: {song.artist}")
                continue

            for candidate in candidates:
                candidate.score = Scorer.score(song, candidate)

            candidates.sort(key=lambda c: c.score, reverse=True)

            jobs.append(
                DownloadJob(
                    song=song,
                    candidate=candidates[0],
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