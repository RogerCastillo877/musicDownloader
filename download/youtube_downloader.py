from datetime import datetime
from pathlib import Path
from yt_dlp import YoutubeDL
from core.models import DownloadResult, DownloadStatus
import time


class YoutubeDownloader:
    OUTPUT_DIR = Path("downloads")

    def __init__(self):
        self.OUTPUT_DIR.mkdir(exist_ok=True)

    def download(
      self,
      song,
      candidate,
    ):

        try:
            
            start = time.time()

            filename = (
                f"{song.artist} - "
                f"{song.title}"
            )

            filename = (
                filename
                .replace("/", "-")
                .replace("\\", "-")
                .replace(":", "-")
            )

            output = (
                self.OUTPUT_DIR /
                f"{filename}.%(ext)s"
            )

            opts = {

                "format":
                    "bestaudio[ext=m4a]/"
                    "bestaudio[acodec^=mp4a]/"
                    "bestaudio",

                "outtmpl":
                    str(output),

                "quiet":
                    False,

                "noplaylist":
                    True,
            }

            with YoutubeDL(opts) as ydl:

                info = ydl.extract_info(
                    candidate.url,
                    download=True,
                )

                return DownloadResult(

                    song=song,

                    success=DownloadStatus.SUCCESS,

                    downloaded_title=
                        info.get("title"),

                    filename=
                        filename,

                    extension=
                        info.get("ext"),

                    codec=
                        info.get("acodec"),

                    bitrate=
                        info.get("abr"),
                    
                    finished_at=
                        datetime.now().isoformat(),
                    
                    duration_seconds=
                        round(
                            time.time() - start,
                            2,
                        ),
                )

        except Exception as e:

            return DownloadResult(

                song=song,

                success=DownloadStatus.FAILED,

                error=str(e),

                finished_at=
                    datetime.now().isoformat(),
                
                duration_seconds=
                    round(
                        time.time() - start,
                        2,
                    )
            )
