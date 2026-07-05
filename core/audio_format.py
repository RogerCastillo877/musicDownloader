from enum import Enum


class AudioFormat(str, Enum):
    AAC = "m4a"
    OPUS = "opus"
    WEBM = "webm"
    MP3 = "mp3"
    FLAC = "flac"