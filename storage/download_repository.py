from storage.database import get_connection


class DownloadRepository:
    def exists(self, artist: str, title: str) -> bool:
        with get_connection() as conn:
            row = conn.execute(
                """
                SELECT id
                FROM downloads
                WHERE artist=? AND title=? AND status='success'
                LIMIT 1
                """,
                (artist, title),
            ).fetchone()
        return row is not None

    def save(self, result) -> None:
        with get_connection() as conn:
            conn.execute(
                """
                INSERT INTO downloads (
                    artist,
                    title,
                    downloaded_title,
                    filename,
                    extension,
                    codec,
                    bitrate,
                    duration_seconds,
                    status,
                    error,
                    downloaded_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    result.song.artist,
                    result.song.title,
                    result.downloaded_title,
                    result.filename,
                    result.extension,
                    result.codec,
                    result.bitrate,
                    result.duration_seconds,
                    result.status.value,
                    result.error,
                    result.finished_at,
                ),
            )
            conn.commit()

    def delete_failed(self, artist: str, title: str) -> None:
        with get_connection() as conn:
            conn.execute(
                """
                DELETE FROM downloads
                WHERE artist=? AND title=? AND status='failed'
                """,
                (artist, title),
            )
            conn.commit()

    def get_failed(self):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT DISTINCT artist, title
                FROM downloads
                WHERE status='failed'
                """
            ).fetchall()

    def get_not_found(self):
        with get_connection() as conn:
            return conn.execute(
                """
                SELECT DISTINCT artist, title
                FROM downloads
                WHERE status='not_found'
                """
            ).fetchall()