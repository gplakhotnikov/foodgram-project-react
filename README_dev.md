# Foodgram

--- Сборка и пуш контейнера backend:

docker build -t foodgram_backend .
docker tag foodgram_backend gplakhotnikov/foodgram_backend
docker push gplakhotnikov/foodgram_backend


---Сборка через compose:

docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py collectstatic --no-input

docker-compose exec backend python manage.py createsuperuser


--- Импорт ингридиентов и тэгов:

docker-compose exec backend python manage.py load_ingredients
docker-compose exec backend python manage.py load_tags


--  Копирование на сервер из папки infra:

scp -p docker-compose.yml gplakhotnikov@84.201.154.199:/home/gplakhotnikov/foodgram/infra/docker-compose.yml
scp -p nginx.conf gplakhotnikov@84.201.154.199:/home/gplakhotnikov/foodgram/infra/nginx.conf
touch .env
nano .env

--- API документация:
http://localhost/api/docs/redoc.html


--- Просмотр баз данных postgres:
docker exec -it infra_db_1 psql -U postgres postgres
\dt
\q