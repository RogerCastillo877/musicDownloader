from dataclasses import dataclass, field
from dataclasses import dataclass
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from enum import Enum

@dataclass(slots=True)
class SongRequest:
    artist: str
    title: str

    normalized_artist: str = ""
    normalized_title: str = ""

    allow_live: bool = False
    allow_cover: bool = False
    allow_remaster: bool = False


@dataclass(slots=True)
class SearchCandidate:
    provider: str

    title: str
    artist: str

    url: str
    provider_id: str

    duration: int = 0
    score: float = 0.0
    is_ambiguous: bool = False

    flags: list[str] = field(
        default_factory=list
    )


@dataclass(slots=True)
class DownloadJob:
    request: SongRequest
    candidate: SearchCandidate

    retry_count: int = 0
    status: str = "NEW"

@dataclass(slots=True)
class Song:
    artist: str
    title: str


@dataclass(slots=True)
class DownloadJob:

    song: Song

    candidate: SearchCandidate

    retries: int = 0

    status: str = "pending"

class DownloadStatus(
    Enum,
):

    SUCCESS = "success"

    FAILED = "failed"

    NOT_FOUND = "not_found"

    SKIPPED = "skipped"

    AMBIGUOUS = "ambiguous"

@dataclass(slots=True)
class DownloadResult:

    song: Song

    status: DownloadStatus

    filename: str | None = None

    downloaded_title: str | None = None

    extension: str | None = None

    codec: str | None = None

    bitrate: float | None = None

    error: str | None = None

    finished_at: str | None = None

    duration_seconds: float | None = None
