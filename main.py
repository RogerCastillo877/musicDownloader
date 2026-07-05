from cli.commands import app
from storage.database import (
    initialize,
)
from storage.download_repository import (
    DownloadRepository,
)

if __name__ == "__main__":
    initialize()
    app()
