# Чеклист: CI/CD (GitHub Actions)

## Справка

### Архитектура пайплайна

| Фаза | Что делает | Когда |
|---|---|---|
| 1. Тесты | pytest + ESLint + html-validate | PR и push в master |
| 2. Сборка и доставка | docker build → save → scp на сервер | Только push в master |
| 3. Деплой | git pull → docker load → compose up → очистка | Только push в master |

### GitHub Secrets

| Секрет | Назначение |
|---|---|
| `SSH_KEY` | Приватный SSH-ключ для доступа к серверу |
| `SSH_HOST` | IP или hostname сервера |
| `SSH_USER` | SSH-пользователь |
| `SSH_PORT` | SSH-порт (если не 22) |
| `DEPLOY_PATH` | Путь к проекту на сервере |
| `GIST_ID` | ID гиста для badge покрытия |
| `GIST_TOKEN` | GitHub PAT с правом `gist` |

### Badge покрытия

Shields.io + GitHub Gist: CI парсит вывод pytest-cov, обновляет JSON в Gist,
README ссылается на shields.io endpoint.

---

## Подготовка

- [x] Создать GitHub Gist с файлом `coverage.json`
- [x] Создать GitHub PAT с правом `gist`
- [x] Сгенерировать SSH-ключ для деплоя (или использовать существующий)
- [x] Заполнить секреты в Settings → Secrets and variables → Actions
- [ ] Клонировать репо на сервер, создать `data/`

## Воркфлоу (.github/workflows/ci.yml)

- [x] Джоб `test`: pytest в Docker + парсинг покрытия + обновление badge
- [x] Джоб `lint`: ESLint + html-validate в Docker
- [x] Джоб `build`: сборка образа, сохранение, SCP на сервер (только push в master)
- [x] Джоб `deploy`: SSH — git pull, docker load, compose up, очистка (только push в master)
- [x] Условие: build только после успешных test + lint; deploy после build

## Фаза 2. Сборка и доставка (джоб `build`)

- [x] Сборка образа на раннере: `docker compose build api`
- [x] Сохранение: `docker save | gzip`
- [x] Доставка: `scp` на сервер

## Фаза 3. Деплой (джоб `deploy`)

- [x] SSH: `git pull origin master`
- [x] SSH: `docker load -i image.tar.gz`
- [x] SSH: `docker compose up -d`
- [x] SSH: `rm image.tar.gz`

## Документация

- [x] Badge покрытия в README.md
- [x] Ссылка на CHECKLIST-CICD.md в README.md
- [x] DEVLOG.md — этап 11
- [x] CHECKLIST-TESTS.md — отмечены пункты CI

## Проверка

- [ ] Push в master → тесты проходят
- [ ] Push в master → образ доставлен и развёрнут на сервере
- [x] Badge покрытия отображается в README
- [ ] PR → запускаются только тесты (без деплоя)
