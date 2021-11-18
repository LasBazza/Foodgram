# Foodgram
## Описание

Продуктовый помощник

## Запуск проекта

1. Склонировать репозиторий

2. Запустить docker-compose из папки

Выполнить в папке _foodgram-project-react/infra_ команду

```
docker-compose up
```
Миграции в проекте применяются автоматически

3. Импортировать исходные данные с ингредиентами в базу данных

После того как все контейнеры запустяться в той же папке выполнить команду
```
docker-compose exec backend python manage.py loaddata ingredients.json
```
4. Создать суперпользователя

Там же выполнить

```
docker-compose exec backend python manage.py createsuperuser
```

Файл _.env_ с переменными окружения находится в репозитории для ускорения проверки :)

