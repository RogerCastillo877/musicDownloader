from rapidfuzz import fuzz


class DuplicateDetector:
    @staticmethod
    def exact_key(song):
        return f"{song.normalized_artist}|{song.normalized_title}"

    @classmethod
    def remove_exact_duplicates(cls, songs):
        seen = set()
        result = []
        for song in songs:
            key = cls.exact_key(song)
            if key in seen:
                continue
            seen.add(key)
            result.append(song)
        return result

    @staticmethod
    def similarity(song1, song2):
        text1 = f"{song1.normalized_artist} {song1.normalized_title}"
        text2 = f"{song2.normalized_artist} {song2.normalized_title}"
        return fuzz.token_set_ratio(text1, text2)

    @classmethod
    def remove_fuzzy_duplicates(cls, songs, threshold=92):
        result = []
        for candidate in songs:
            duplicate = False
            for existing in result:
                score = cls.similarity(candidate, existing)
                if score >= threshold:
                    duplicate = True
                    break
            if not duplicate:
                result.append(candidate)
        return result
