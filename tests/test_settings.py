from pathlib import Path

from config.settings import load_settings


def test_load_settings_uses_project_relative_path(monkeypatch, tmp_path):
    monkeypatch.chdir(tmp_path)

    settings = load_settings()

    assert settings.workers == 4
    assert settings.download.format == "mp3"
    assert settings.paths.downloads == "./downloads"
