import pytest

from app import create_app


@pytest.fixture(autouse=True)
def _tmp_db(tmp_path, monkeypatch):
    """Перенаправляет БД во временный файл — каждый тест получает чистую базу."""
    monkeypatch.setattr('app.models.DATA_DIR', str(tmp_path))
    monkeypatch.setattr('app.models.DATABASE', str(tmp_path / 'test.db'))


@pytest.fixture
def client(_tmp_db):
    """Flask test client с временной БД."""
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c
