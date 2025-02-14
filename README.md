# TODO FastAPI Application

**Описание:**

Это простое TODO приложение, разработанное с использованием FastAPI. Оно позволяет создавать, просматривать, обновлять и удалять задачи. Приложение использует [SQLAlchemy](https://www.sqlalchemy.org/) для работы с базой данных и [Alembic](https://alembic.sqlalchemy.org/en/latest/) для миграций базы данных.

**Содержание**

- [Запуск без Docker](#запуск-без-docker)
  - [Предварительные требования](#предварительные-требования-без-docker)
  - [Установка](#установка-без-docker)
  - [Запуск приложения](#запуск-приложения-без-docker)
- [Запуск с Docker](#запуск-с-docker)
  - [Предварительные требования](#предварительные-требования-с-docker)
  - [Сборка Docker образа](#сборка-docker-образа)
  - [Запуск Docker контейнера](#запуск-docker-контейнера)
- [Дополнительные инструкции](#дополнительные-инструкции-опционально)
  - [Миграции базы данных](#миграции-базы-данных)
  - [Тестирование](#тестирование)

## Запуск без Docker

### Предварительные требования (без Docker)

- **Python 3.12+**
- **pip**
- **Виртуальное окружение**

### Установка (без Docker)

1. **Клонируйте репозиторий:**

   ```bash
   git clone <ссылка_на_репозиторий>
   cd <папка_проекта>
   ```

2. **Создайте и активируйте виртуальное окружение:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # для Linux/macOS
   venv\Scripts\activate  # для Windows
   ```

3. **Установите зависимости:**

   ```bash
   pip install -r requirements.txt
   ```

### Запуск приложения (без Docker)

1. **Запустите сервер:**

   ```bash
   uvicorn server:app --reload
   ```

2. **Откройте браузер и перейдите по адресу:** `http://127.0.0.1:8000` или `http://localhost:8000`.

## Запуск с Docker

### Предварительные требования (с Docker)

- **Docker**

### Сборка Docker образа

1. **Перейдите в корень проекта, где находится `Dockerfile`.**

2. **Соберите Docker образ:**

   ```bash
   docker build -t todo-fastapi .
   ```

### Запуск Docker контейнера

1. **Запустите Docker контейнер:**

   ```bash
   docker run todo-fastapi
   ```

2. **Откройте браузер и перейдите по адресу:** `http://127.0.0.1:8000` или `http://localhost:8000`.

## Дополнительные инструкции

### Миграции базы данных

1. **Запуск миграций (без Docker):**

   ```bash
   alembic upgrade head
   ```

2. **Миграции в Docker:**

   ```bash
   docker exec -it todo-fastapi alembic upgrade head
   ```

### Тестирование

1. **Тестирование (без Docker):**

```bash
pytest
```

2. **Тестирование в Docker:**

```bach
docker exec -it todo-fastapi pytest
```