from storage.database import (
    get_connection,
)


class DownloadRepository:

    def exists(
        self,
        artist,
        title,
    ):

        conn = get_connection()

        row = conn.execute(
            """
            SELECT id
            FROM downloads
            WHERE
                artist=?
            AND
                title=?
            AND
                success=1
            LIMIT 1
            """,
            (
                artist,
                title,
            ),
        ).fetchone()

        conn.close()

        return row is not None

    def save(
        self,
        result,
    ):

        conn = get_connection()

        conn.execute(
            """
            INSERT INTO downloads
            (
                artist,
                title,
                downloaded_title,
                filename,
                extension,
                codec,
                bitrate,
                duration_seconds,
                success,
                error,
                downloaded_at
            )
            VALUES
            (
                ?,?,?,?,?,?,?,?,?,?,?
            )
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
                int(result.success),
                result.error,
                result.finished_at,
            ),
        )

        conn.commit()

        conn.close()