import pytest  # Подключаем pytest для создания фикстур
from fastapi.testclient import TestClient  # Импортируем тестовый клиент FastAPI
from app.main import app
import app.models as models


@pytest.fixture(autouse=True)
def _tmp_db(tmp_path, monkeypatch):
    """
    Фикстура pytest для автоматической инициализации временной базы данных перед каждым тестом.
    """

    # Используем monkeypatch для подмены пути к директории данных в app.models на временную папку tmp_path,
    # предоставляемую pytest (уникальна для каждого теста).
    # DATA_DIR теперь указывает на tmp_path
    monkeypatch.setattr(models, 'DATA_DIR', str(tmp_path))
    # DATABASE указывает на test.db в tmp_path
    monkeypatch.setattr(models, 'DATABASE', str(tmp_path / 'test.db'))

    # Инициализируем базу данных: создаём схему и загружаем тестовые данные.
    # models.init_db()

    yield


@pytest.fixture  # Создаем фикстуру test client
def client():  # Возвращает HTTP клиент для вызова API
    with TestClient(app) as c:  # Создаем тестовый клиент в контекстном менеджере
        # Возвращаем тестовый клиент в тест. После завершения теста, клиент будет закрыт автоматически.
        yield c
