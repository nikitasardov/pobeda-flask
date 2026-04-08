# Отчёт о миграции API: Flask -> FastAPI

В этом документе фиксирую пошаговое выполнение учебной миграции бэкенда с Flask на FastAPI, не изменяя фронтенд-часть проекта.

## 1) Подготовил отдельную зону миграции

Миграцию делаю в отдельной папке `FastAPIApp`, чтобы:
- не ломать рабочую Flask-реализацию;
- сравнивать поведение двух реализаций;
- безопасно экспериментировать с архитектурой и тестами.

Создал базовые файлы:
- `FastAPIApp/requirements.txt` (зависимости FastAPI/uvicorn);
- `FastAPIApp/app/config.py`;
- `FastAPIApp/app/main.py`;
- `FastAPIApp/run.py`.

## 2) Поднял минимальный FastAPI-каркас

В `FastAPIApp/app/main.py` создал приложение:
- `app = FastAPI(...)`

И первый технический endpoint:
- `GET /health` через функцию `healthcheck()`.

Сервис стартует и отвечает.

В `FastAPIApp/run.py` запустил сервер через:
- `uvicorn.run("app.main:app", ...)`

## 3) Добавил Pydantic-схемы и проверил автодокументацию

- `UserCreate` — для входного payload в `POST /users`;
- `UserOut` — для формата ответа.

Через это я закрепил:
- валидацию `name` и `email` на уровне схем;
- использование `response_model` в роуте;
- автоматическую генерацию OpenAPI-документации (`/docs`, `/openapi.json`).

Отдельно проверил, что при невалидном path/body FastAPI возвращает валидационные ошибки (`422`) и что Swagger UI показывает эти ошибки как клиент документации.

## 4) Реализовал API-эндпоинты в FastAPI-версии

На этапе первичного переноса реализовал в `app/main.py`:
- `GET /users` (функция `get_users()`);
- `GET /users/{user_id}` (функция `get_user_by_id(...)`);
- `POST /users` (функция `create_user(...)`).

Сначала логика была in-memory (список `users`) для быстрого старта, затем перевёл её на SQLite-слой.

## 5) Перенёс слой данных в отдельный модуль models

Создал `FastAPIApp/app/models.py` (по смыслу аналог Flask-версии) с функциями:
- `get_connection()` — создаёт SQLite-соединение, настраивает `row_factory = sqlite3.Row`;
- `init_db()` — создаёт таблицу `users`, вызывает seed на пустой таблице;
- `seed_db(conn)` — заполняет 5 тестовыми пользователями;
- `get_all_users()` — возвращает список пользователей как `list[dict]`;
- `get_user_by_id(user_id)` — возвращает пользователя или `None`;
- `create_user(name, email)` — создаёт пользователя и возвращает его.

В `FastAPIApp/app/config.py` добавил переменные:
- `BASE_DIR`, `DATA_DIR`, `DATABASE` — для явного пути к SQLite-файлу.

## 6) Переключил роуты с in-memory на SQLite

В `FastAPIApp/app/main.py` перестал использовать список `users` как хранилище и переключил роуты на функции из `app.models`:

Для инициализации базы при запуске приложения использовал lifecycle-хук FastAPI через `lifespan`:
- вместо `@app.on_event("startup")` перешёл на `lifespan`;
- определил функцию `lifespan(...)` до создания `app = FastAPI(..., lifespan=lifespan)`.

## 7) Поднял pytest-инфраструктуру для FastAPIApp

Добавил:
- `FastAPIApp/requirements-test.txt`;
- `FastAPIApp/tests/`;
- `FastAPIApp/tests/conftest.py`.

В `conftest.py` я настроил:
- фикстуру `client()` на `TestClient(app)`;
- autouse-фикстуру с `tmp_path + monkeypatch` для изоляции БД.

Ключевая идея изоляции:
- подменяю `app.models.DATA_DIR` и `app.models.DATABASE` на временный путь;
- тесты не трогают реальную БД проекта;
- окружение тестов полностью предсказуемо (результаты тестов всегда одинаковы при одинаковых условиях).

## 8) Перенёс и расширил набор API-тестов

Реализовал API-тесты в `FastAPIApp/tests/test_api_users.py` и smoke-тест в `FastAPIApp/tests/test_api_smoke.py`.

Покрыл сценарии:
- `GET /health`;
- `GET /users` (200, список);
- `GET /users/{id}` (200 для существующего, 404 для отсутствующего, 422 для невалидного типа id);
- `POST /users` (201 для валидного payload, 422 для невалидных данных);
- сквозной сценарий `POST -> GET` (новый пользователь появляется в списке).

## 9) Перенёс unit-тесты слоя данных

unit-тесты в `FastAPIApp/tests/test_models.py`:
- `TestGetConnectionDb`:
  - `test_returns_connection`
  - `test_row_factory_is_row`
- `TestInitDb`:
  - `test_creates_users_table`
  - `test_seeds_on_empty_table`
  - `test_no_duplicates_seed`
- `TestSeedDb`:
  - `test_inserts_five_records`
- `TestGetAllUsersDb`:
  - `test_returns_list_of_dicts`
  - `test_dict_keys`
  - `test_empty_table`
- `TestGetUserByIdDb`:
  - `test_existing_user`
  - `test_not_existing_user`
- `TestCreateUserDb`:
  - `test_returns_dict`
  - `test_autoincrement`

Таким образом отдельно валидировал поведение слоя данных, не смешивая с HTTP-уровнем.

## 10) Настроил маркеры и групповой запуск тестов

Создал `FastAPIApp/pytest.ini` и зафиксировал правила:
- `testpaths`, `python_files`, `python_classes`, `python_functions`;
- зарегистрировал маркеры.

Маркерная схема:
- `[TYPE]`: `unit`, `api`;
- `[AREA/PURPOSE]`: `users`, `db`, `smoke`.

Пометил тесты соответствующими декораторами `@pytest.mark...` и проверил запуск выборок:
- `pytest -m unit`
- `pytest -m api`
- `pytest -m smoke`
- `pytest -m "api and not smoke"`
- `pytest -k ...` для фильтрации по именам.

## 11) Финальная проверка качества

Выполнил полный прогон:
- `pytest --cov=app tests/`

Результат:
- все тесты проходят;
- покрытие модулей `app/config.py`, `app/main.py`, `app/models.py` = 100%.

## 12) Что осознанно не менял

В рамках этой миграции не переписывал фронтенд:
- `static/*` и связанная frontend-логика не мигрировались на другой стек.

Фокус миграции был только на API и автотестах для него.

## Итог

Реализовал рабочий FastAPI-аналог Flask-бэкенда:
- с Pydantic-валидацией;
- с SQLite-слоем данных;
- с разделением API- и unit-тестов;
- с изоляцией тестовой БД через `monkeypatch`;
- с маркерами для группового запуска;
- с полным проходом тестов и высоким покрытием.
