class MusicDLException(Exception):
    pass


class SongNotFoundError(MusicDLException):
    pass


class DownloadError(MusicDLException):
    pass


class ConversionError(MusicDLException):
    pass