# Pizza-CRM

### Pizza-CRM — пет-проект для освоения и практического применения новых знаний, в котором будут реализованы следующие подходы:

- Монолитная архитектура
- Микросервисная архитектура
- Отказоустойчивость
- Покрытие тестами
- Устойчивость к высокой нагрузке

В ветке `main` находится монолитная архитектура.

Микросервисная архитектура находится в ветке:

`features/microservices`

и содержит полноценную реализацию функционала с разделением приложения на отдельные сервисы.

---

## Технологии

Основные технологии проекта:

- Python
- FastAPI
- Pydantic / Pydantic Settings
- SQLAlchemy
- PostgreSQL
- Redis
- Pytest
- Docker
- Docker Compose
- uv
- GitHub Actions

---

# Как использовать — How to use

## Требования

Перед запуском проекта необходимо установить:

- Python 3.14+
- Docker
- Docker Compose
- uv

Проверить установленные версии:

```bash
python --version
docker --version
docker compose version
uv --version
```

---

## Клонирование репозитория

Склонируйте репозиторий:

```bash
git clone https://github.com/K4DJee/pizza-CRM.git
```

Перейдите в директорию проекта:

```bash
cd pizza-CRM
```

---

## Установка зависимостей

Установите зависимости проекта с помощью `uv`:

```bash
uv sync
```

После этого зависимости будут установлены в виртуальное окружение проекта.

---

## Переменные окружения

Для локального запуска необходимо создать файл `.env`.

Пример тестового окружения:

```env
JWT_ACCESS_SECRET_KEY=test_access_secret_key
JWT_REFRESH_SECRET_KEY=test_refresh_secret_key

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

MAIL_USERNAME=test@example.com
MAIL_PASSWORD=test_password
MAIL_FROM=test@example.com
MAIL_SERVER=localhost

POSTGRES_DATABASE_URL=postgresql://admin:root@pizza-crm-db:5432/pizza_crm

REDIS_HOST=pizza-crm-redis
REDIS_PORT=6379
```

`.test.env` содержит только тестовые значения и не должен содержать реальные пароли, токены или другие секретные данные.

Для удобства можно хранить в репозитории файл `.test.env.example`, а `.test.env` добавить в `.gitignore`.

---

## Запуск PostgreSQL и Redis

Для работы монолитной версии проекта используются два Docker-контейнера:

- `pizza-crm` — PostgreSQL
- `pizza-crm-redis` — Redis

Они запускаются через Docker Compose.

Запустить контейнеры:

```bash
docker compose up -d
```

Проверить состояние контейнеров:

```bash
docker compose ps
```

Ожидаемые контейнеры:

```text
pizza-crm
pizza-crm-redis
```

PostgreSQL будет доступен по адресу:

```text
localhost:5432
```

Redis будет доступен по адресу:

```text
localhost:6379
```

Остановить контейнеры:

```bash
docker compose down
```

Данные PostgreSQL сохраняются в Docker volume, поэтому после `docker compose down` база данных не удаляется.

---

## Запуск приложения

После запуска PostgreSQL и Redis запустите FastAPI:

```bash
uv run fastapi dev
```

После запуска приложение будет доступно по адресу:

http://127.0.0.1:8000

Swagger:

http://127.0.0.1:8000/docs

---

# Тестирование

В проекте используются два вида тестов:

- Unit-тесты
- Интеграционные тесты

---

## Unit-тесты

Запуск:

```bash
uv run pytest -v -s tests/unit
```

Unit-тесты предназначены для проверки отдельных компонентов приложения и не должны требовать запуска всех внешних сервисов.

---

## Интеграционные тесты

Запуск:

```bash
uv run pytest -v -s tests/integration
```

Для интеграционных тестов необходимо, чтобы PostgreSQL и Redis были запущены.

Запустите контейнеры:

```bash
docker compose up -d
```

После этого запустите тесты:

```bash
uv run pytest -v -s tests/integration
```

---

# GitHub Actions

Для автоматического запуска тестов используется GitHub Actions.

Workflow запускается при:

- `push` в ветки `main` и `develop`
- создании `pull request` в ветки `main` и `develop`

В CI запускаются:

- Unit-тесты
- Интеграционные тесты