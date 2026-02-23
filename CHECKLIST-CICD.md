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

- [ ] Создать GitHub Gist с файлом `coverage.json`
- [ ] Создать GitHub PAT с правом `gist`
- [ ] Сгенерировать SSH-ключ для деплоя (или использовать существующий)
- [ ] Заполнить секреты в Settings → Secrets and variables → Actions
- [ ] Клонировать репо на сервер, создать `data/`

## Воркфлоу (.github/workflows/ci.yml)

- [ ] Джоб `test`: pytest в Docker (`docker compose run --rm test`)
- [ ] Джоб `lint`: ESLint + html-validate в Docker (`docker compose run --rm lint`)
- [ ] Джоб `badge`: парсинг покрытия, обновление Gist (только push в master)
- [ ] Джоб `deploy`: сборка образа, SCP, SSH-деплой (только push в master)
- [ ] Условие: deploy только после успешных test + lint

## Деплой (фаза 2 + 3)

- [ ] Сборка образа на раннере: `docker compose build api`
- [ ] Сохранение: `docker save | gzip`
- [ ] Доставка: `scp` на сервер
- [ ] SSH: `git pull origin master`
- [ ] SSH: `docker load -i image.tar.gz`
- [ ] SSH: `docker compose up -d`
- [ ] SSH: `rm image.tar.gz`

## Документация

- [ ] Badge покрытия в README.md
- [ ] Ссылка на CHECKLIST-CICD.md в README.md
- [ ] DEVLOG.md — этап 11
- [ ] CHECKLIST-TESTS.md — отметить пункты CI

## Проверка

- [ ] Push в master → тесты проходят
- [ ] Push в master → образ доставлен и развёрнут на сервере
- [ ] Badge покрытия отображается в README
- [ ] PR → запускаются только тесты (без деплоя)
