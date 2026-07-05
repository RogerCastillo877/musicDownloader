FLAGS = [
    "official",
    "official audio",
    "official music video",
    "topic",
    "live",
    "cover",
    "remaster",
    "remastered",
    "lyrics",
    "karaoke",
    "tribute",
    "studio version",
]


def extract_flags(text: str):

    text = text.lower()

    found = []

    for flag in FLAGS:
        if flag in text:
            found.append(flag)

    return found