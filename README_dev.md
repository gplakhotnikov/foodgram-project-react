# Foodgram

--- Сборка и пуш контейнера backend:

docker build -t foodgram_backend .
docker tag foodgram_backend gplakhotnikov/foodgram_backend
docker push gplakhotnikov/foodgram_backend


---Сборка через compose:

docker-compose up -d
docker-compose exec backend python manage.py makemigrations
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input

docker-compose exec backend python manage.py createsuperuser


--- Импорт ингридиентов и тэгов:

docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags


--- API документация:
http://localhost/api/docs/redoc.html


--- Просмотр баз данных postgres:
docker exec -it infra_db_1 psql -U postgres postgres
\dt
\q