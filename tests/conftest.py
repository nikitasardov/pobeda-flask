import pytest


@pytest.fixture(autouse=True)
def _tmp_db(tmp_path, monkeypatch):
    """Перенаправляет БД во временный файл — каждый тест получает чистую базу."""
    monkeypatch.setattr('app.models.DATA_DIR', str(tmp_path))
    monkeypatch.setattr('app.models.DATABASE', str(tmp_path / 'test.db'))
