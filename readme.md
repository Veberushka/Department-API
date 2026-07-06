### Тестовое задание Department

REST API для управления департаментами, их структурой и сотрудниками этих подразделений. Реализована древовидная структура,
каскадное удаление и перемещение сотрудников.

### Технологический стек:
- **Python** -3.12-slim
- **Docker & Docker Compose**
- **PostgreSQL** - 17.4 База данных
- **FastAPI**   - веб-фреймворк
- **SQLAlchemy** -ORM
- **Alembic** - миграция
- **Pytest** - тестирование

### Необходимые требования:
- Python 3.12-slim
- Docker & Docker Compose
- PostgreSQL 17.4
- 300Мб свободной оперативной памяти

### Запуск:
# 1.Клонировать репозиторий
    git clone <url>
    cd <project-name>

# 2. Создание .env и .env.container в корне проекта
    пример
    .env
    DB_HOST = 'localhost'
    DB_PORT = '5433'
    DB_NAME = 'postgres__dep_empl'
    DB_USER = 'amin'
    DB_PASSWORD = 'its_my_password'

    .env.container
    DB_HOST = 'postgres'
    DB_PORT = '5432'
    DB_NAME = 'postgres__dep_empl'
    DB_USER = 'amin'
    DB_PASSWORD = 'its_my_password'

# 3.Создать образ,создать контейнер и запустить его
    docker-compose up -d

# 4.Приложение будет доступно по адресу: http://localhost:8000

###Для доработки, тестирования проект можно запустить локально, после создания контейнера:

# 1.Создать виртуальное окружение
    python -m venv venv
    venv\Scripts\activate

# 2.Установка зависимостей
    pip install -r req.txt

# 3. Запуск
    Запуск проекта происходит из файла app.main.py

### API Эндпоинты
|   Метод     |      URL    |   Описание  |
|:-----------:|:-----------:|:-----------:|
| POST   | /departments/   | Создать департамент    |
| POST    | /departments/{id}/employees/    | Создать сотрудника   |
| GET    | /departments/{id}   | Получить департамент с деревом    |
| PATCH    | /departments/{id}    | Переместить/обновить подразделение    |
| DELETE    | /departments/{id}    | Удалить департамент    |


### Тестирование
# 1.Запустить тест
    pytest tests/test_validation.py -v

### Логирование
Логи имеют 3 уровня: 
**INFO**- успешные операции
**WARNING**-ошибки валидации
**ERROR**- критические ошибки

Просмотреть логи можно в файле /logs/app.log

### Документация API

После запуска docker: http://localhost:8000/docs
После локального запуска: http://127.0.0.1:8000/docs

###Roadmap
##Ближайшие улучшения:
Улучшение логирования 

##Долгосрочные планы
Добавление аутентификации и авторизации (JWT)
Реализация кэширования (Redis)
Настройка CI/CD (GitHub Actions)


