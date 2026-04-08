# Проект «pobeda-flask» (backend на FastAPI)

![CI/CD](https://github.com/nikitasardov/pobeda-flask/actions/workflows/ci.yml/badge.svg)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/nikitasardov/fe0cbe35c07ebafcdf77b078040ec799/raw/coverage.json)

> Текущая версия проекта использует **FastAPI** как backend.
> Историческая Flask-версия сохранена в `Flask_old/` (включая `Flask_old/README.md`).

## Что в проекте сейчас

- Backend: FastAPI (`app/main.py`, `app/models.py`, `app/config.py`)
- Frontend: статика в `static/`, раздаётся nginx
- База данных: SQLite (`data/users.db`)
- Тесты: `pytest` (unit + api + smoke), покрытие `pytest-cov`
- CI/CD: GitHub Actions (`.github/workflows/ci.yml`)

## Запуск

**Требования:** Docker + Docker Compose

```bash
docker compose up --build -d
```

Приложение и frontend:
- `http://localhost:5000/`

Документация FastAPI:
- `http://localhost:5000/docs`
- `http://localhost:5000/redoc`
- `http://localhost:5000/openapi.json`

Остановка:

```bash
docker compose down
```

## Тесты и линтинг

Все тесты:

```bash
docker compose run --rm test
```

Покрытие:

```bash
docker compose run --rm test pytest --cov=app tests/
```

Маркерные выборки:

```bash
docker compose run --rm test pytest -m unit tests/
docker compose run --rm test pytest -m api tests/
docker compose run --rm test pytest -m smoke tests/
```

Линтинг фронтенда:

```bash
docker compose run --rm lint
```

## API

| Метод | URL | Описание |
|---|---|---|
| GET | `/users` | Список пользователей |
| GET | `/users/{id}` | Пользователь по id, `404` если не найден |
| POST | `/users` | Создание пользователя, валидация через Pydantic |
| GET | `/health` | Технический health endpoint |

## Структура проекта

```text
pobeda-flask/
├── app/                    # FastAPI backend
│   ├── main.py             # роуты + lifespan
│   ├── models.py           # SQLite слой данных
│   └── config.py
├── run.py                  # запуск uvicorn
├── tests/                  # pytest тесты
│   ├── conftest.py         # TestClient + monkeypatch временной БД
│   ├── test_models.py      # unit
│   ├── test_api_users.py   # api
│   └── test_api_smoke.py   # smoke
├── pytest.ini              # маркеры и конфиг pytest
├── nginx/nginx.conf        # прокси /users + /docs + /redoc + /openapi.json
├── static/                 # фронтенд
├── Flask_old/              # архив Flask-реализации
│   └── README.md
└── docs/
    ├── FASTAPI-MIGRATION-REPORT.md
    └── FASTAPI-MIGRATION-SHORT.md
```

## Дополнительно

- Подробный отчёт миграции: `docs/FASTAPI-MIGRATION-REPORT.md`
- Короткая версия отчёта: `docs/FASTAPI-MIGRATION-SHORT.md`
- Старое описание проекта (Flask): `Flask_old/README.md`
