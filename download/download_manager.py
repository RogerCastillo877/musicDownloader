import threading

from concurrent.futures import (
    ThreadPoolExecutor,
    as_completed,
)

from core.models import DownloadStatus
from download.youtube_downloader import (
    YoutubeDownloader,
)

from services.logger_service import LoggerService

from storage.download_repository import (
    DownloadRepository
)

class DownloadManager:

    def __init__(
        self,
        workers=4,
    ):

        self.workers = workers

        self.downloader = (
            YoutubeDownloader()
        )

        self.repository = (
            DownloadRepository()
        )

        self.logger = (
            LoggerService()
        )

    def process(
        self,
        jobs,
    ):
        success = []
        failed = []

        futures = []

        with ThreadPoolExecutor(
            max_workers=self.workers,
        ) as executor:

            for job in jobs:

                futures.append(
                    executor.submit(
                        self.download,
                        job,
                    )
                )

            for future in as_completed(
                futures,
            ):

                try:
                    
                    result = (
                        future.result()
                    )

                    if (
                        result.status
                        ==
                        DownloadStatus.SUCCESS
                    ):

                        success.append(result)

                        self.logger.success(
                            result
                        )

                        self.repository.save(
                            result
                        )

                        print()

                        print(
                            "SUCCESS:"
                        )

                        print(
                            f"{result.song.artist}"
                            f" - "
                            f"{result.song.title}"
                        )

                    elif (
                        result.status
                        ==
                        DownloadStatus.FAILED
                    ):

                        failed.append(result)

                        self.logger.error(
                            result
                        )

                        self.repository.save(
                            result
                        )

                        print()

                        print(
                            "FAILED:"
                        )

                        print(
                            f"{result.song.artist}"
                            f" - "
                            f"{result.song.title}"
                        )

                        print(
                            result.error
                        )

                except Exception as e:

                    print()

                    print(
                        "ERROR:"
                    )

                    print(e)

            self.logger.summary(
                requested=
                    len(success)+len(failed),

                success=
                    len(success),

                failed=
                    len(failed),
            )

            print()

            print("=" * 60)

            print(
                f"REQUESTED: "
                f"{len(success)+len(failed)}"
            )

            print(
                f"SUCCESS: "
                f"{len(success)}"
            )

            print(
                f"FAILED: "
                f"{len(failed)}"
            )

            if failed:

                print()

                print(
                    "FAILED SONGS:"
                )

                for item in failed:

                    print(
                        f"  "
                        f"{item.song.artist}"
                        f" - "
                        f"{item.song.title}"
                    )

            print()

            print("=" * 60)

    def download(
        self,
        job,
    ):

        print(
            f"[{threading.current_thread().name}] "
            f"Downloading: "
            f"{job.song.artist}"
            f" - "
            f"{job.song.title}"
        )

        return (
            self.downloader.download(
                job.song,
                job.candidate,
            )
        )