# turbo-parakeet

# itk_academy_test_piravky

Тестовое задание на роль Python разработчик
[by piravky](https://github.com/piravky)


## id и начальный баланс тестовых кошельков
___

**id:** `d70d0d78-f789-48b4-9ba0-d939cbf9d9f8`
**balance:** `1000.50`

**id:** `f726345e-abef-4e79-8788-d19a92825700`
**balance:** `250.75`

**id:** `d3576d28-3179-4821-bd5f-8899c722f876`
**balance:** `5000.00`

**id:** `418694b1-fec9-436e-b975-951830e13b59`
**balance:** `100.00`


## Преподготовка
в директории создать файл `.env` для хранения переменных окружения
### Пример файла `.env`

Поменять значения по своему усмотрению
```
 DB_HOST=postgres
 DB_USER=postgres
 DB_PORT=5432
 DB_PASSWORD=1qwerty
 DB_DATABASE=postgres
```

## Запуск с помощью `Docker compose`

Для запуска docker compose необходимо создать файл `.env_db` для хранения переменных контейнеров

### Пример файла `.env_db`
Поменять значения по своему усмотрению
```
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1qwerty
POSTGRES_DB=postgres
```
выполнить команду `docker compose up -d`

## Запуск без `Docker compose`

- `pip install poetry`
- `poetry install`
- `poetry run alembic upgrade head && poetry run python3 src/main.py`