# Чеклист: тесты

## Справка

### Уровни тестирования

| Уровень | Что проверяет | Зависимости | Скорость |
|---|---|---|---|
| Unit | Функции `models.py` изолированно | pytest, временная БД | Быстро |
| Интеграционные | API-эндпоинты через Flask test client | pytest, Flask `test_client()` | Быстро |
| Фронтенд (lint) | Синтаксис и стиль JS | ESLint | Быстро |
| Фронтенд (unit) | JS-функции изолированно | Jest + jsdom | Быстро |
| E2E | UI в браузере (таблица, модалка, форма) | Playwright / Cypress | Медленно |

### Инструменты (бэкенд)

| Компонент | Варианты | Выбор |
|---|---|---|
| Фреймворк тестов | `pytest`, `unittest` | `pytest` |
| Фикстуры БД | `:memory:` SQLite, `tmp_path` | `:memory:` |
| Тест-клиент API | `app.test_client()` (встроен во Flask) | — |
| Покрытие кода | `pytest-cov` | `pytest-cov` |

### Инструменты (фронтенд)

| Компонент | Варианты | Примечание |
|---|---|---|
| Линтер | ESLint | Проверка стиля и ошибок |
| Unit-тесты JS | Jest + jsdom | Тест `loadUsers`, `renderTable` и т.д. без браузера |
| E2E | Playwright, Cypress, Selenium | Полная проверка UI в реальном браузере. Не реализуем |

### Фикстуры

Фикстура — подготовка окружения для теста (setup/teardown).
В pytest — функция с `@pytest.fixture`, которая создаёт ресурс,
отдаёт его тесту через `yield`, и после теста уничтожает.

Фикстура БД — временная SQLite-база в памяти (`:memory:`).
Создаётся заново для каждого теста, не трогает реальную `data/users.db`,
тесты не влияют друг на друга.

### CI/CD

- Тесты должны запускаться одной командой: `pytest --cov=app tests/`
- Результат — exit code 0/1 (для пайплайна) + отчёт покрытия
- CI-конфиг (GitHub Actions / GitLab CI) создаётся отдельным этапом
- Badge покрытия в README — после настройки CI

---

## Unit-тесты (`tests/test_models.py`)

- [x] Фикстура: временная БД `:memory:`, подмена пути к БД через monkeypatch
- [x] `get_connection()` — возвращает соединение с `row_factory = sqlite3.Row`
- [x] `init_db()` — таблица `users` создаётся
- [x] `init_db()` — при пустой таблице автоматически вызывает `seed_db`
- [x] `seed_db()` — после вызова в таблице 5 записей
- [x] `get_all_users()` — возвращает список словарей с ключами `id`, `name`, `email`
- [x] `get_all_users()` — пустая таблица → пустой список
- [x] `get_user_by_id()` — находит существующего пользователя
- [x] `get_user_by_id()` — возвращает `None` для несуществующего
- [x] `create_user()` — создаёт пользователя, возвращает словарь с `id`
- [x] `create_user()` — id автоинкрементируется

## Интеграционные тесты (`tests/test_api.py`)

- [x] Фикстура: Flask `test_client()` с временной БД
- [x] `GET /users` — 200, JSON-массив
- [x] `GET /users/1` — 200, JSON с полями `id`, `name`, `email`
- [x] `GET /users/999` — 404, JSON с `error`
- [x] `POST /users` (валидные данные) — 201, пользователь в ответе
- [x] `POST /users` (пустое имя) — 400
- [x] `POST /users` (некорректный email) — 400
- [x] `POST /users` (без тела) — 400
- [x] Сценарий: POST создаёт → GET возвращает нового пользователя в списке

## Фронтенд

- [x] ESLint: настройка, проверка `static/js/app.js`
- [x] html-validate: проверка структуры `static/index.html`
- [x] Исправлены ошибки доступности: `scope="col"` на `<th>`, убран `aria-hidden` с модалки
- [ ] ~~Jest: unit-тесты JS~~ — не реализуем, моки превышают тестируемый код
- [ ] ~~E2E~~ — не реализуем

## Инфраструктура тестов

- [x] `requirements-test.txt` — pytest, pytest-cov
- [x] `tests/__init__.py`
- [x] `tests/conftest.py` — фикстуры (временная БД, test client)
- [x] `tests/test_models.py` — unit-тесты
- [x] `tests/test_api.py` — интеграционные тесты
- [x] Запуск: `pytest --cov=app tests/`
- [x] Все тесты проходят (25/25)
- [x] CI-конфиг — см. [CHECKLIST-CICD.md](CHECKLIST-CICD.md)
- [x] Badge покрытия в README
