from datetime import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    artist: Mapped[str] = mapped_column(String)

    title: Mapped[str] = mapped_column(String)

    normalized_artist: Mapped[str] = mapped_column(
        String,
        index=True,
    )

    normalized_title: Mapped[str] = mapped_column(
        String,
        index=True,
    )

    unique_hash: Mapped[str] = mapped_column(
        String,
        unique=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )