class ScoringDebugger:
    @staticmethod
    def explain(song, candidate, artist_score, title_score, full_score, bonuses, penalties, final):
        print()
        print(candidate.title)
        print(f"artist     : {artist_score}")
        print(f"title      : {title_score}")
        print(f"full       : {full_score}")
        print(f"bonus      : {bonuses}")
        print(f"penalties  : {penalties}")
        print(f"final      : {final}")
