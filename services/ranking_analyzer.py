class RankingAnalyzer:
    @staticmethod
    def print_analysis(song, candidates):
        print("\n" + "=" * 80)
        print(f"REQUEST:\n{song.artist} - {song.title}")

        if not candidates:
            print("\nNO RESULTS")
            return

        winner = candidates[0]
        print("\nWINNER:")
        print(f"  {winner.score:6.2f}  {winner.title}")

        if len(candidates) > 1:
            print("\nREJECTED:")
            for candidate in candidates[1:5]:
                diff = winner.score - candidate.score
                print(f"  {candidate.score:6.2f}  (-{diff:.2f})  {candidate.title}  {candidate.flags}")

        print("=" * 80)
