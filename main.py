from cli.commands import app
from storage.database import (
    initialize,
)

if __name__ == "__main__":
    initialize()
    app()