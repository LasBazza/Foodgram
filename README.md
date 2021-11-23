# Foodgram
## Описание

Продуктовый помощник

## Запуск проекта

**1. Склонировать репозиторий**

**2. Запустить docker-compose из папки**

Выполнить в папке _foodgram-project-react/infra_ команду

```
docker-compose up
```
Миграции в проекте применяются автоматически

**3. Импортировать исходные данные с ингредиентами в базу данных**

После того как все контейнеры запустяться в той же папке выполнить команду
```
docker-compose exec backend python manage.py loaddata ingredients.json
```
**4. Создать суперпользователя**

Там же выполнить

```
docker-compose exec backend python manage.py createsuperuser
```

**5. Заполнить файл _.env_ и поместить его в папку, где лежит файл _manage.py_**

```
SECRET_KEY=your_django_secret_key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

