# Foodgram ver. 0.9.0

Проект Foodgram (продуктовый помощник) создан для публикации и хранения пользовательских рецептов. Среди возможностей - подписка на других пользователей, добавление рецептов в избранное, формирование списка покупок и его загрузка в TXT-файл. Foodgram выполнен в качестве дипломного проекта для курса Yandex.Practicum.  Текущая версия: 0.9.0 (22 сентября 2022 года), исправленная после двух ревью.

Доступер по адресу: http://51.250.31.28/


## Особенности / Features
- Все сервисы и страницы доступны для пользователей в соответствии с их правами;
- Рецепты на всех страницах сортируются по дате публикации (новые — выше);
- Работает фильтрация по тегам, в том числе на странице избранного и на странице рецептов одного автора;
- Работает пагинатор;
- Проект работает с СУБД PostgreSQL.

## Стек технологий / Tech
- [Python](https://www.python.org/)
- [Django](https://www.djangoproject.com/)
- [Django REST framework](https://www.django-rest-framework.org/)
- [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) - a JSON Web Token authentication backend for the Django REST Framework
- [PyJWT](https://pyjwt.readthedocs.io/) - a Python library which allows you to encode and decode JSON Web Tokens (JWT)
- [Docker](https://www.docker.com/)
- [GitHub Actions](https://github.com/features/actions)

## Как запустить проект на локальном компьютере/ Installation
Клонировать репозиторий на свой компьютер:
```
git clone git@github.com:gplakhotnikov/foodgram-project-react.git
```
В папке infra создать файл .env и внести туда следущие данные: 
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=***придумайте пароль***
DB_HOST=db
DB_PORT=5432
```
Развернуть проект из папки infra:
```
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input
```
Создать суперпользователя:
```
docker-compose exec backend python manage.py createsuperuser
```
Импортировать ингридиенты и тэги:
```
docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags
```
После этого проект доступен по адресу http://localhost/

## API документация / API docs
http://localhost/api/docs/redoc.html

## Дополнительные сведения / Advanced 
Сборка и пуш контейнера backend:
```
docker build -t foodgram_backend .
docker tag foodgram_backend gplakhotnikov/foodgram_backend
docker push gplakhotnikov/foodgram_backend
```
Доступ к базам данных postgres:
```
docker exec -it infra_db_1 psql -U postgres postgres
```

## О разработчике / Development
Grigory Plakhotnikov