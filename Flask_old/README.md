# Проект «pobeda-flask»

![CI/CD](https://github.com/nikitasardov/pobeda-flask/actions/workflows/ci.yml/badge.svg)
![coverage](https://img.shields.io/endpoint?url=https://gist.githubusercontent.com/nikitasardov/fe0cbe35c07ebafcdf77b078040ec799/raw/coverage.json)

## Методология

Проект реализован с использованием AI-ассистированной разработки (Cursor IDE).
Акцент — на управлении процессом, а не ручном написании кода:
формализация требований → анализ и принятие решений → генерация кода → ревью → тестирование.

> **Результат:** три основных задания (бэкенд, фронтенд, интеграция) выполнены
> за ~1,5 часа. С добавлением тестов (unit, интеграционные, линтинг)
> и CI/CD (GitHub Actions, автодеплой) общее чистое время — не более 4 часов.

Подробнее: [этапы, инструменты, требования, решения](docs/METHODOLOGY.md)

---

## Запуск

**Требования:** Docker с поддержкой Compose

```bash
docker compose up --build -d
```

Приложение доступно по адресу: **http://localhost:5000/**

Файл `.env` создавать не нужно — приложение работает с разумными значениями по умолчанию.
Шаблон `.env.example` описывает переменные (`SECRET_KEY`, `FLASK_DEBUG`, `FLASK_HOST`, `FLASK_PORT`),
которые имеет смысл переопределить при развёртывании на production-сервере.

### Остановка

```bash
docker compose down
```

### Что происходит при запуске

1. Собирается образ Flask API (`api`) из `Dockerfile`
2. Поднимается контейнер nginx (`frontend`) на базе `nginx:alpine`
3. При первом запуске создаётся файл `data/users.db` с 5 тестовыми пользователями
4. nginx раздаёт фронтенд на порту 5000 и проксирует API-запросы (`/users`) на Flask

### Тесты

```bash
docker compose run --rm test
```

Unit- и интеграционные тесты (pytest). Каждый тест работает с временной БД —
продакшен-данные не затрагиваются. Результат: exit code 0/1 + отчёт покрытия.

### Линтинг фронтенда

```bash
docker compose run --rm lint
```

ESLint (JavaScript) + html-validate (HTML-структура, доступность).

### Данные

БД хранится в `./data/users.db` (монтируется как volume). Данные сохраняются между перезапусками контейнеров. Для сброса к начальному состоянию:

```bash
docker compose down
rm data/users.db
docker compose up -d
```

---

## Скриншоты

### Таблица пользователей

![Таблица пользователей](docs/screenshots/2026-02-23_15-34.png)

Главная страница: таблица с данными пользователей и форма добавления.

### Детальная информация

![Детальная информация](docs/screenshots/2026-02-23_15-34_1.png)

По клику на строку открывается модальное окно с полной информацией о пользователе.

### Добавление пользователя

![Заполнение формы](docs/screenshots/2026-02-23_15-35.png)

Форма заполнена — имя и email. Отправка по кнопке «Добавить».

### Результат добавления

![Успешное добавление](docs/screenshots/2026-02-23_15-36.png)

После отправки: алерт с подтверждением, новый пользователь появляется в таблице без перезагрузки страницы.

---

## Структура проекта

```
pobeda-flask/
├── app/                  # Flask API (сервис api)
│   ├── __init__.py       # фабрика create_app()
│   ├── config.py
│   ├── models.py
│   └── routes.py
├── run.py                # точка входа Flask
├── static/               # Фронтенд (сервис frontend, nginx)
│   ├── index.html
│   └── js/
│       └── app.js
├── nginx/
│   └── nginx.conf        # конфиг nginx: статика + прокси /users → api
├── tests/                # тесты (pytest)
│   ├── conftest.py       # фикстуры (временная БД)
│   ├── test_models.py    # unit-тесты models.py
│   └── test_api.py       # интеграционные тесты API
├── .github/
│   └── workflows/
│       └── ci.yml        # CI/CD: тесты, линт, badge, деплой
├── data/                 # в .gitignore, монтируется в контейнер api
├── Dockerfile            # multi-stage: base (production) + test
├── Dockerfile.lint       # Node: ESLint + html-validate
├── docker-compose.yml    # сервисы: api, frontend, test и lint (профиль test)
├── requirements.txt
├── requirements-test.txt # тестовые зависимости (pytest, pytest-cov)
├── .env.example
├── .gitignore
├── README.md
└── docs/
    ├── screenshots/      # скриншоты для документации
    ├── METHODOLOGY.md    # методология, требования, решения
    ├── CHECKLIST.md
    ├── CHECKLIST-TESTS.md
    ├── CHECKLIST-CICD.md
    ├── DEVLOG.md
    └── raw_task.txt
```

---

## API

| Метод | URL | Описание |
|---|---|---|
| GET | `/users` | Список всех пользователей (JSON) |
| GET | `/users/<id>` | Пользователь по id (JSON), 404 если не найден |
| POST | `/users` | Создание пользователя (JSON: `name`, `email`), 201 / 400 |

---

## Документы проекта

| Файл | Назначение |
|---|---|
| [METHODOLOGY.md](docs/METHODOLOGY.md) | Методология, требования из задания, принятые решения |
| [CHECKLIST.md](docs/CHECKLIST.md) | Чеклист реализации — отслеживание прогресса |
| [CHECKLIST-TESTS.md](docs/CHECKLIST-TESTS.md) | Чеклист тестов — unit, интеграционные, CI/CD |
| [CHECKLIST-CICD.md](docs/CHECKLIST-CICD.md) | Чеклист CI/CD — GitHub Actions, деплой |
| [DEVLOG.md](docs/DEVLOG.md) | Журнал разработки — что сделано, что скорректировано, какие проблемы |
| [raw_task.txt](docs/raw_task.txt) | Исходное задание (без изменений) |
