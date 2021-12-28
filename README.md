# Foodgram
## Описание

Продуктовый помощник, блог кулинарных рецептов. Зарегистрированные пользователи могут публиковать свои рецепты, подписываться на других пользователей, добавлять рецепты в _Избранное_ и в список покупок. На основе рецептов, добавленных в список покупок, можно сформировать список необходимых продуктов и выгрузить его в PDF.


* Python 3.8
* Django 2.2.8
* Django Rest Framework
* [Djoser](https://djoser.readthedocs.io/en/latest/)
* [Django-filter](https://django-filter.readthedocs.io/en/stable/index.html)
* [ReportLab](https://www.reportlab.com/dev/docs/)
* Gunicorn
* PostgreSQL
* Docker
* Nginx

## Запуск проекта

**1. Склонировать репозиторий**

```
git clone https://github.com/LasBazza/Foodgram
```

**2. Заполнить файл _.env_ и поместить его в папку _Foodgram/backend/foodgram/_**

```
SECRET_KEY=django_secret_key
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
DB_HOST=db
DB_PORT=5432
```

**3. Запустить docker-compose**

Выполнить в папке _Foodgram/infra/_ команду

```
docker-compose up
```

Миграции в проекте применяются автоматически

**4. Импортировать исходные данные с ингредиентами в базу данных**

После запуска всех контейнеров в той же папке выполнить команду
```
docker-compose exec backend python manage.py loaddata ingredients.json
```

**4. Создать суперпользователя**

Там же выполнить

```
docker-compose exec backend python manage.py createsuperuser
```

Проект доступен на http://127.0.0.1/. Ингредиенты и тэги можно добавить через админ-панель django http://127.0.0.1/admin/.
