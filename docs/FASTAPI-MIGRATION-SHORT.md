# Миграция с Flask на FastAPI

> Текущее состояние проекта: backend в корне репозитория уже переведён на FastAPI и является основной версией.

Выполнил учебную миграцию бэкенда проекта с Flask на FastAPI в отдельной директории `FastAPIApp`, не затрагивая фронтенд-часть.

## Что сделал

- Создал новый FastAPI-каркас (`app/main.py`, `app/config.py`, `run.py`).
- Добавил Pydantic-схемы:
  - `UserCreate` для валидации входного body;
  - `UserOut` для формирования ответа.
- Перенёс API-эндпоинты:
  - `GET /health`
  - `GET /users`
  - `GET /users/{user_id}`
  - `POST /users`
- Перенёс слой данных в `app/models.py`:
  - `get_connection`, `init_db`, `seed_db`,
  - `get_all_users`, `get_user_by_id`, `create_user`.
- Настроил инициализацию БД при старте приложения через `lifespan` (актуальный подход FastAPI).

## Что сделал по тестам

- Настроил `pytest`-инфраструктуру в `FastAPIApp/tests`.
- Подключил `TestClient` для API-тестов.
- Изолировал тестовую БД через `tmp_path + monkeypatch` (реальная БД не затрагивается).
- Реализовал и прогнал:
  - API-тесты (`test_api_users.py`, `test_api_smoke.py`);
  - unit-тесты слоя моделей (`test_models.py`).
- Добавил `pytest.ini` и маркеры для группового запуска:
  - `[TYPE]`: `unit`, `api`
  - `[AREA/PURPOSE]`: `users`, `db`, `smoke`

## Результат

- Полный тестовый прогон проходит стабильно.
- Покрытие `app/*`:
  - `app/config.py` — 100%
  - `app/main.py` — 100%
  - `app/models.py` — 100%
  - `TOTAL` — 100%

## Практический эффект

В результате закрепил практические навыки:
- перенос API с Flask на FastAPI с сохранением функциональности;
- использование Pydantic-валидации и OpenAPI/Swagger;
- построение и изоляцию backend-тестов (unit + API) на `pytest`;
- организацию тестового набора через маркеры для выборочного запуска.
