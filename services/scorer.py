from rapidfuzz import fuzz


PREFERRED = [
    "official audio",
    "topic",
    "auto-generated",
]

PENALTIES = {
    "live": 50,
    "cover": 60,
    "tribute": 60,
    "karaoke": 60,
    "remaster": 20,
    "remastered": 20,
    "lyrics": 20,
    "without movie inserts": 25,
    "432 hz": 20,
    "8d": 30,
    "12d": 30,
    "binaural": 30,
    "visualizer": 10,
    "remaster": 40,
    "remastered": 40,
}

BONUS = {
    "official audio": 30,
    "lossless": 20,
    "hq audio": 15,
    "audio": 10,
    "studio version": 15,
    "extended mix": 10,
    "original mix": 15,
    "club mix": 10,
    "radio edit": 5,
    "hq": 10,
    "320kbps": 15,
    "flac": 20,
}

NEGATIVE_PHRASES = {
    "subtitulado": 30,
    "subtitle": 30,
    "sub español": 30,
    "lirik": 40,
    "terjemahan": 40,
    "indo": 40,
}


class Scorer:
    @staticmethod
    def score(song, candidate):
        candidate_text = candidate.title.lower()

        artist_score = fuzz.ratio(song.artist.lower(), candidate.title.lower())
        title_score = fuzz.token_sort_ratio(song.title.lower(), candidate.title.lower())
        full_score = fuzz.token_set_ratio(f"{song.artist} {song.title}".lower(), candidate.title.lower())

        score = (
            artist_score * 0.40
            + title_score * 0.35
            + full_score * 0.25
        )

        for flag in candidate.flags:
            if flag in BONUS:
                score += BONUS[flag]
            if flag in PENALTIES:
                score -= PENALTIES[flag]

        requested = f"{song.artist} {song.title}".lower()
        candidate_name = candidate.title.lower()

        if fuzz.partial_ratio(requested, candidate_name) >= 95:
            score += 10

        artist_name = song.artist.lower()
        if artist_name not in candidate_text:
            score -= 25
        if song.artist.lower() in candidate_text:
            score += 15

        return round(score, 2)
