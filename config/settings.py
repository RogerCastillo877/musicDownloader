from pathlib import Path

import yaml
from pydantic import BaseModel


class DownloadSettings(BaseModel):
    format: str
    bitrate: int


class DuplicateSettings(BaseModel):
    threshold: int


class RetrySettings(BaseModel):
    max_attempts: int


class SearchSettings(BaseModel):
    skip_live: bool
    skip_cover: bool
    skip_remaster: bool


class PathSettings(BaseModel):
    downloads: str
    logs: str


class DatabaseSettings(BaseModel):
    url: str


class Settings(BaseModel):
    workers: int
    download: DownloadSettings
    duplicates: DuplicateSettings
    retries: RetrySettings
    search: SearchSettings
    paths: PathSettings
    database: DatabaseSettings


def load_settings() -> Settings:
    path = Path(__file__).resolve().parent / "settings.yaml"

    if not path.exists():
        raise FileNotFoundError(f"No se encontró el archivo de configuración: {path}")

    with path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    if not isinstance(data, dict):
        raise ValueError("El contenido del archivo de configuración debe ser un objeto YAML")

    return Settings.model_validate(data)