import re

from unidecode import unidecode


REMOVE_WORDS = {
    "feat",
    "ft",
    "featuring",
    "official",
    "video",
    "lyrics",
    "lyric",
    "hd",
    "4k",
    "audio",
}


class Normalizer:

    @staticmethod
    def normalize(text: str) -> str:
        text = unidecode(text)

        text = text.lower()

        text = re.sub(r"[\(\)\[\]\{\}]", " ", text)

        text = re.sub(r"[^a-z0-9 ]", " ", text)

        words = []

        for word in text.split():
            if word not in REMOVE_WORDS:
                words.append(word)

        return " ".join(words)

    @classmethod
    def normalize_song(cls, song):
        song.normalized_artist = cls.normalize(
            song.artist
        )

        song.normalized_title = cls.normalize(
            song.title
        )

        return song